from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the entire pipeline (including ColumnTransformer)
model_pipeline = pickle.load(open("predictive_maintenance_model.pkl", "rb"))

@app.route("/", methods=["GET"])
def Home():
    return render_template("index.html")

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
        return render_template("index.html", prediction_text="Input error: Please enter valid numeric values for all fields.")

    return render_template("index.html", prediction_text="The need for maintenance is: {}".format(prediction_text))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=100)
