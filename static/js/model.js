

document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('upload_csv');
  const fileNameDisplay = document.getElementById('file_name');

  fileInput.addEventListener('change', function() {
      const file = fileInput.files[0];
      if (file) {
          fileNameDisplay.textContent = file.name;
      } else {
          fileNameDisplay.textContent = 'No file chosen';
      }
  });

  // Handle the label click to trigger the file input click
  const label = document.querySelector('.btn');
  label.addEventListener('click', function() {
      fileInput.click();
  });
});

