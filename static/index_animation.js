var $time = $('.timer_animation_png');
var $win = $(window);

$win.on('scroll', function () {
   var top = $win.scrollTop();
    $time.css('transform', 'rotate(' + top + 'deg)');
});