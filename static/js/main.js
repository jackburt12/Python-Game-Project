/**
 *  Simply moved the compas needle towards the mouse on hover
 *  Offers no funcitonality except astheitic.
**/
var arrow=$(".main-arrow");
var compass=$(".compass");
var arrowCenter=[arrow.offset().left+arrow.width()/4, arrow.offset().top+arrow.height()/4];

$(compass).on( "mousemove", function(event) {
  var angle = Math.atan2(event.pageX- arrowCenter[0],- (event.pageY- arrowCenter[1]) )*(180/Math.PI);

    arrow.css({ "-webkit-transform": 'rotate(' + angle + 'deg)'});
    arrow.css({ '-moz-transform': 'rotate(' + angle + 'deg)'});
    arrow.css({ 'transform': 'rotate(' + angle + 'deg)'});
});

$(function() {
  $('.direction-seg').bind('click', function(event) {

    var direction = '/' + event.target.id;
    console.log(direction);

    $.getJSON(direction,
        function(data) {
      //do nothing
    });
    return false;
  });
});
