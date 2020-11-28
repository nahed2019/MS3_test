/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $("body").bootstrapMaterialDesign();
    $(".sidenav").sidenav({edge: "right"});
    $(".collapsible").collapsible();
    $(".datepicker").datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 15,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});

$(function() {

  $(".my_progress").each(function() {

    var value = $(this).attr('data-value');
    var left = $(this).find('.progress-left .progress-bar');
    var right = $(this).find('.progress-right .progress-bar');

    if (value > 0) {
      if (value <= 50) {
        right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)')
      } else {
        right.css('transform', 'rotate(180deg)')
        left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)')
      }
    }

  })

  function percentageToDegrees(percentage) {

    return percentage / 100 * 360

  }

});
