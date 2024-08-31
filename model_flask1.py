from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import pickle
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the entire pipeline (including ColumnTransformer)
model_pipeline = pickle.load(open("predictive_maintenance_model.pkl", "rb"))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def Home():
    return render_template("model.html")

@app.route("/about")
def abt():
    return render_template("about_us.html")

# @app.route("/download")
# def dl():
#     return render_template("download.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the form values
        air_temperature = float(request.form['air_temperature'])
        process_temperature = float(request.form['process_temperature'])
        rotational_speed = int(request.form['rotational_speed'])
        torque = float(request.form['torque'])
        tool_wear = int(request.form['tool_wear'])
        machine_type = request.form['machine_type']

        # Prepare the data as a DataFrame
        data = {
            'Air temperature [K]': [air_temperature],
            'Process temperature [K]': [process_temperature],
            'Rotational speed [rpm]': [rotational_speed],
            'Torque [Nm]': [torque],
            'Tool wear [min]': [tool_wear],
            'Type': [machine_type]
        }

        input_df = pd.DataFrame(data)

        # Use the pipeline to transform and predict
        prediction = model_pipeline.predict(input_df)

        # Convert prediction to a readable format
        prediction_text = "Yes" if prediction[0] == 1 else "No"

    except ValueError as e:
        # Handle conversion error or missing data
        return render_template("model.html", prediction_text="Input error: Please enter valid numeric values for all fields.")

    return render_template("model.html", prediction_text="The need for maintenance is: {}".format(prediction_text))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("Upload Function Reached")
    if request.method == 'POST':
        try:
            # Check if the request has a file part
            if 'file' not in request.files:
                return redirect(request.url)
            
            file = request.files['file']

            # If no file is selected
            if file.filename == '':
                return redirect(request.url)

            # If a file is selected and it's allowed
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Read the CSV file using pandas
                data = pd.read_csv(file_path)

                # Drop 'UID' column if it exists
                if 'UID' in data.columns:
                    data.drop('UID', axis=1, inplace=True)

                # Predict using the model
                prediction = model_pipeline.predict(data)
                print(prediction)

                # Add the predictions to the DataFrame

                word_prediction = []


                failure_types = ["Heat Dissipation", "No Failure", "Over Strain", "Power Failure", "Random Failure", "Tool Wear Failure"]

                for i in prediction:
                    word_prediction.append(failure_types[i])



                print(word_prediction)
    
                data['Predicted_Value'] = word_prediction


                # Save the DataFrame with predictions to a new CSV file
                output_filename = 'output_' + filename
                output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                print(f"Saving file to: {output_filepath}")  # Add this line for debugging
                data.to_csv(output_filepath, index=False)

                # Redirect to the download page
                print(f"Redirecting to download page for file: {output_filename}")
                return redirect(url_for('download_file', filename=output_filename))

        except Exception as e:
            print(e)
            return render_template("upload.html", error="An error occurred while processing the file. Please ensure it's a valid CSV.")

    return render_template("upload.html")

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=100)
