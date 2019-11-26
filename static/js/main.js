var arrow=$(".main-arrow");
var compass=$(".compass");
var arrowCenter=[arrow.offset().left+arrow.width()/4, arrow.offset().top+arrow.height()/4];// $(compass).mousemove(function(e){
//
//
//   var angle = Math.atan2(e.pageX- arrowCenter[0],- (e.pageY- arrowCenter[1]) )*(180/Math.PI);
//
//   arrow.css({ "-webkit-transform": 'rotate(' + angle + 'deg)'});
//   arrow.css({ '-moz-transform': 'rotate(' + angle + 'deg)'});
//   arrow.css({ 'transform': 'rotate(' + angle + 'deg)'});
//
// });

$(compass).on( "mousemove", function(event) {
  var angle = Math.atan2(event.pageX- arrowCenter[0],- (event.pageY- arrowCenter[1]) )*(180/Math.PI);

    arrow.css({ "-webkit-transform": 'rotate(' + angle + 'deg)'});
    arrow.css({ '-moz-transform': 'rotate(' + angle + 'deg)'});
    arrow.css({ 'transform': 'rotate(' + angle + 'deg)'});
});
