//initialise slider
$("[data-slider]")
  .each(function () {
    var input = $(this);
    $("<input>")
      .addClass("output")
      .insertAfter($('#price_pound'));
  })
  .bind("slider:ready slider:changed", function (event, data) {
    $(this)
      .nextAll(".output:first")
        .attr('id', 'price_output')
        .val(data.value.toFixed(0));
    $('#id_style-price').val(data.value.toFixed(0));
  });

function update_model (colour) {
  var url = $('#model').attr('src');
  url = url.substring(0, url.lastIndexOf('/'));
  $('#model').attr('src', url.concat('/').concat(colour).concat('.jpg'));
}

//update garment colour on click and add to form
$('.garment_selection').click(function(){
  var garment = $(this).attr('id');
  $('#id_style-garment').val(garment);
  $('.garment_selection').css('color', 'grey');
  $('#'.concat(garment)).css('color', 'black');
  update_colourpicker(garment);

//initialise slider
$("[data-slider]")
  .bind("slider:ready slider:changed", function (event, data) {
    $(this)
      .nextAll(".output:first")
        .attr('id', 'price_output')
        .val(data.value.toFixed(0));
    $('#id_style-price').val(data.value.toFixed(0));
  });
});

var tee_colours_html = '<div class="colour_selection grid_2 alpha" id="colour_white"></div><div class="colour_selection grid_2" id="colour_black"></div><div class="colour_selection grid_2" id="colour_cardinal_red"></div><div class="colour_selection grid_2 omega" id="colour_chestnut"></div><div class="colour_selection grid_2 alpha" id="colour_daisy"></div><div class="colour_selection grid_2" id="colour_dark_heather"></div><div class="colour_selection grid_2" id="colour_forest_green"></div><div class="colour_selection grid_2 omega" id="colour_sports_grey"></div><div class="colour_selection grid_2 alpha" id="colour_heather_purple"></div><div class="colour_selection grid_2" id="colour_heather_royal"></div><div class="colour_selection grid_2" id="colour_indigo_blue"></div><div class="colour_selection grid_2 omega" id="colour_light_blue"></div><div class="colour_selection grid_2 alpha" id="colour_military_green"></div><div class="colour_selection grid_2" id="colour_navy"></div><div class="colour_selection grid_2" id="colour_orange"></div><div class="colour_selection grid_2 omega" id="colour_purple"></div><div class="colour_selection grid_2 alpha" id="colour_red"></div><div class="colour_selection grid_2 omega" id="colour_royal"></div>';
var sweatshirt_colours_html = '<div class="colour_selection grid_2 alpha" id="sweatshirt_white"></div><div class="colour_selection grid_2" id="sweatshirt_black"></div><div class="colour_selection grid_2" id="sweatshirt_cardinal_red"></div><div class="colour_selection grid_2 omega" id="sweatshirt_forest"></div><div class="colour_selection grid_2 alpha" id="sweatshirt_navy"></div><div class="colour_selection grid_2 omega" id="sweatshirt_sports_grey"></div>';

//function that updates the garment colour picker depending on the selected garment
function update_colourpicker (garment) {
  if (garment == 'garment_tshirt') {
    $('#price_output').val(15);
    $('#colour_selector').html(tee_colours_html);
    //add tick to default colour
    $('#colour_white').html('y');
    update_model('colour_white'); //change model picture
  }
  else {
    $('#price_output').val(20);
    $('#colour_selector').html(sweatshirt_colours_html);
    //add tick to default colour
    $('#sweatshirt_white').html('y');
    update_model('sweatshirt_white'); //change model picture
  }

  //change hover cursor
  $('.colour_selection').hover(function() {
   $(this).css('cursor','pointer');
   }, function() {
   $(this).css('cursor','auto');
  });

  //refresh click function
  $('.colour_selection').click(function(){
    var colour = $(this).attr('id');
    $('#id_style-tee_colour').val(colour); //add to form
    $('#colour_selector').children().html(''); //clear all ticks
    $(this).html('y'); //add tick to selected colour box
    update_model(colour); //change model picture
  });
}



//Initialisation
$(document).ready(function() {
  var preview_colour = $('#id_style-preview_colour').val();
  //var tee_colour = $('#id_style-tee_colour').val();
  var tee_colour = 'colour_white'
  var garment_type = $('#id_style-garment').val();
  var price = $('#id_style-price').val();

  //update from default database values
  $('.selected_colour').css('background-color', preview_colour);
  $('#'.concat(garment_type)).css('color', 'black');
  $('#price_output').val(price);
  update_colourpicker(garment_type);

  //initialise colourpicker
  $('#picker').farbtastic('#color');
  var pick = $.farbtastic('#picker');
  pick.setColor($('#id_style-preview_colour').val()); //initial colour from db form
  pick.linkTo(onColourChange);

  $('#color').keyup(function() { //update when user enter colour manually
    pick.setColor($(this).val());
  });

  function onColourChange(color) { //colourchange event handler
      $('#color').val(color);
      $('#color').css('background-color', color);
      $('#id_style-preview_colour').val(color);
      $('.selected_colour').css('background-color', color)
  };
});