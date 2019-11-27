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

recent_squares = [];
starting_square = null;
clear_square = null;

$(function() {
  $('.direction-seg').bind('click', function(event) {

    var direction = '/' + event.target.id;
    console.log(direction);

    $.getJSON(direction,
        function(data) {
          var location = data.location;
          $("#hunger").text(data.hunger);
          $("#energy").text(data.energy);

          if(starting_square == null) {
            console.log("First step");

            var starting_row = $("#starting_square").closest("tr").index();
            var starting_col = $("#starting_square").closest("td").index();
            console.log(starting_row);
            console.log(starting_col);

            starting_square = [starting_col, starting_row];
            add_to_queue(starting_square);

          }

          $("#location").text(location);
          coordinates = get_coordinates(location);
          add_to_queue(coordinates);

          colour_squares();
    });
    return false;
  });
});

function get_coordinates(result) {
  result = result.replace('\]','');
  result = result.replace('\[','');
  result = result.split(',',2);
  coordinates = [parseInt(result[0]), parseInt(result[1])];
  return coordinates;
}

function add_to_queue(coordinates) {
  if(recent_squares.length == 5) {
    clear_square = recent_squares[0];
    recent_squares.shift();
    recent_squares.push(coordinates);
  } else {
    recent_squares.push(coordinates);
  }
}

function colour_squares() {
  var table = document.getElementById("map");

  if(clear_square != null) {
    var row = table.rows[11-clear_square[1]];
    var cell = row.cells[clear_square[0]];
    cell.style.backgroundColor = "white";
  }

  for (i = 0; i < recent_squares.length; i++) {
    var row = table.rows[11-recent_squares[i][1]];
    var cell = row.cells[recent_squares[i][0]];
    cell.style.backgroundColor = "red";

    opacity = (((i * 2 + 2)/10) + (5-recent_squares.length) * 0.2).toString();
    cell.style.opacity = opacity;
  }



}
