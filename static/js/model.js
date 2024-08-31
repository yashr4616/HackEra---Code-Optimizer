// var dropDown = function()
// {
//   $('.menu-dropdown').on('click', function()
//   {
//     $('.menu-content').toggleClass('hidden');
//     $('.con, .menu-dropdown').toggleClass('menu-active');
    
//     setTimeout(function()
//     {
//       $('.menu-content').toggleClass('opacity')
//     }, 300)
    
//   })
// }

// dropDown();



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

