/**
 *  Call this function to add a piece of commentary to the list and refresh the styling
**/
function commentate(commentary) {
  $('#commentary-list').prepend($('<li>').text(commentary));

  var list_items = $("#commentary-list li");
  list_items.each(function(idx, li) {
    if(idx > 6) {
      li.remove();
    } else {
      li.style.opacity = 1-idx*0.15;
    }
  });
}

// $(document).ready(function(){
//   console.log("ready");
//     $('[data-toggle="popover"]').popover();
// });


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

/**
 *  This is the JS which deals with player movement.
 *  This includes the visible functionality of the map as well as the backend communication.
**/

recent_squares = [];
starting_square = null;
clear_square = null;

$(function() {
  $('.direction-seg').bind('click', function(event) {

    var direction = '/' + event.target.id;
    console.log(direction);

    $.getJSON(direction,
        function(data) {
          console.log(data.error);
          if(data.error !== undefined) {
            console.log("Error");
            commentate(data.error);
          } else {

            var location = data.location;
            $("#hunger").text(data.hunger);
            $("#energy").text(data.energy);

            if(starting_square == null) {

              var starting_row = 11 - $("#starting_square").closest("tr").index();
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
          }
    });
    return false;
  });
});

/**
 *  This is the JS which deals with player sleeping.
 *  This includes the visible functionality as well as the backend communication.
**/

$(function() {
  $('#sleep_button').bind('click', function(event) {

    $('#overlay').animate({
      opacity: 1,
    }, 1500, function() {
      //faded out
      $.getJSON("/sleep", function(data) {

        $("#energy").text(data.energy);
        commentate("You awake feeling refreshed and ready to continue your adventure.");

      });

      $('#overlay').animate({
        opacity: 0,
      }, 3000, function() {
      });
    });
    return false;
  });
});

/**
 *  Below here are useful functions used for the rest of the JS funcitonality.
**/

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
