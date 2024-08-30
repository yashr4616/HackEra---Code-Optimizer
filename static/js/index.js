var dropDown = function()
{
  $('.menu-dropdown').on('click', function()
  {
    $('.menu-content').toggleClass('hidden');
    $('.con, .menu-dropdown').toggleClass('menu-active');
    
    setTimeout(function()
    {
      $('.menu-content').toggleClass('opacity')
    }, 300)
    
  })
}

dropDown();