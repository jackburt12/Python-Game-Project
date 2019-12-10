/**
 *  Simply moved the compas needle towards the mouse on hover
 *  Offers no funcitonality except astheitic.
**/
var arrow=$(".main-arrow");
var compass=$(".compass");
var arrowCenter=[arrow.offset().left+arrow.width()/2, arrow.offset().top+arrow.height()/2];

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

    $.getJSON(direction,
        function(data) {
          if(data.error !== undefined) {
            commentate(data.error);
          } else {

            var location = data.location;
            $("#hunger").text(data.hunger);
            $("#energy").text(data.energy);

            if(data.starving == "true") {
              $("#health").text(data.health);
              commentate("If you don't eat something soon you won't last much longer...")
            }

            if(starting_square == null) {

              var starting_row = 11 - $("#starting_square").closest("tr").index();
              var starting_col = $("#starting_square").closest("td").index();

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
 *  This is the JS which deals with player scavenging.
**/
$(function() {
  $('#scavenge_button').bind('click', function(event) {

    $.getJSON("/scavenge", function(data) {

      if(data.error !== undefined) {
        commentate(data.error);
      } else {
        //disable button for 30 seconds
        var btn = $('#scavenge_button');
        btn.prop('disabled', true);
        setTimeout(function(){
          btn.prop('disabled', false);
        },30000);

        commentate("You search your local area for anything that might be of use");

        var items = data.result;

        for (var i = 0; i < items.length; i++) {
          item = items[i]

          if($(".item-name:contains("+item.name+")").length === 0) {
              $("#inventory tr:last").after("<tr><td class=\"item-name\">" +  "<a data-trigger=\"hover\" data-toggle=\"popover\" title=\""+ item.name +"\" data-content=\""+ item.description +"\" data-html=\"true\">"+item.name+"</a></td><td class=\"item-quantity\">1</td></tr>")
          } else {
            $(".item-name:contains("+item.name+")").next().html(parseInt($(".item-name:contains("+item.name+")").next().html())+1);
          }
        }

        $("#energy").text(data.energy);
        $("#damage").text(data.damage);
        $("#protection").text(data.protection);

        populate_crafting(data.crafting);

        $('[data-toggle="popover"]').popover();


      }
    });
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

/**
  * This function populates the crafting menu based on the materials within the player's inventory
**/
function populate_crafting(items) {

    //clear table
    $('#crafting tbody').empty();

    var table = $("#crafting");

    for (var i = 0; i < items.length; i++) {
      var recipe = items[i];
      var item = recipe.item;

      var materials = "";

      for (var j = 0; j < recipe.materials.length; j++) {
        materials = materials + (recipe.materials[j].quantity + "x " + recipe.materials[j].item_name + "<br>");

      }
      materials = materials + "<br>"

      table.append("<tr><td class=\"item-to-craft\">" + "<a class=\"item-name-craft\" data-trigger=\"hover\" data-toggle=\"popover\" title=\""+ item.name +"\" data-content=\""+ "<b>Cost to craft:</b><br>" + materials + item.description + "\" data-html=\"true\">"+item.name+"</a></td></tr>");

      disabled = false;
      for (var j = 0; j < recipe.materials.length; j++) {
        if(parseInt($(".item-name:contains("+recipe.materials[j].item_name+")").parent().children().eq(1).html()) < parseInt(recipe.materials[j].quantity)) {
          disabled = true;
        }
      }

      if(disabled) {
        $(".item-to-craft > a:contains("+recipe.item.name+")").css({"color":"#888","cursor":"default"});
      }

    }

}

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

/**
 *  Deals with item usage
**/
$(function() {
  $('.item-name').bind('click', function(event) {

    var item_name = '/item/' + event.target.text;
    console.log(item_name);

    $.getJSON(item_name, function(data) {

      if(data.error !== undefined) {
        commentate(data.error);
      } else if(data.effect !== undefined) {

        $("#health").text(data.health);
        $("#hunger").text(data.hunger);
        $("#energy").text(data.energy);

        commentate(data.effect + " increased by " + data.amount);

        var row = event.target.parentElement.parentElement;

        if(data.quantity <= 0) {
          $("[data-toggle='popover']").popover('hide');
          row.remove();
          populate_crafting(data.crafting);
        }

        var quantity = row.childNodes[3];
        quantity.innerHTML = data.quantity;

      }


    });

  });
});

/**
 *  Deals with crafting
**/
$('#crafting').on('click', '.item-name-craft', function(event) {
    // Do something on an existent or future .dynamicElement
    console.log("Test");

    var item_name = '/craft/' + event.target.text;
    console.log(item_name);

    $.getJSON(item_name, function(data) {
      $("[data-toggle='popover']").popover('hide');

      var item = data.item_crafted

      if($(".item-name:contains("+item.name+")").length === 0) {
          $("#inventory tr:last").after("<tr><td class=\"item-name\">" +  "<a data-trigger=\"hover\" data-toggle=\"popover\" title=\""+ item.name +"\" data-content=\""+ item.description +"\" data-html=\"true\">"+item.name+"</a></td><td class=\"item-quantity\">1</td></tr>")
      } else {
        $(".item-name:contains("+item.name+")").next().html(parseInt($(".item-name:contains("+item.name+")").next().html())+1);
      }

      for(var i = 0; i < data.materials_used.length; i++) {
        console.log($(".item-name:contains("+data.materials_used[i].name+")").parent());
        console.log(data.materials_used[i].quantity);
        if(data.materials_used[i].quantity == 0) {
          $(".item-name:contains("+data.materials_used[i].name+")").parent().remove();
        } else {
          $(".item-name:contains("+data.materials_used[i].name+")").parent().children().eq(1).html(data.materials_used[i].quantity);
        }
      }

      $("#damage").text(data.damage);
      $("#protection").text(data.protection);

      commentate("Crafted a " + item.name)

      populate_crafting(data.crafting);


    });


});
