$(document).ready(function() {
  // Dynamically adjust main content height according to window size
  // to keep the footer at the bottom of the page wherever page content
  // is not sufficient
  var min_content_height = $(window).height() - $("header").outerHeight() -
                           ($("footer").outerHeight() * 2) - $("nav").outerHeight();
  $("main").css("min-height", min_content_height + "px");

  $(window).resize(function() {
    var min_content_height = $(window).height() - $("header").outerHeight() -
                             ($("footer").outerHeight() * 2) - $("nav").outerHeight();
    $("main").css("min-height", min_content_height + "px");
  });

  // Define the carousel and start looping through the slides automatically,
  // pausing whilst hovering over the carousel and resuming whilst
  carousel();
  var loop_carousel = window.setInterval(function() {
                        $("#move-right").trigger("click");
                      }, 5000);

  $(".section-carousel").mouseover(function (){
    clearInterval(loop_carousel);
  });

  $(".section-carousel").mouseleave(function (){
    loop_carousel = window.setInterval(function() {
                      $("#move-right").trigger("click");
                    }, 5000);
  });
});

// Using CSS hidden/active classes, maintain a single active or visible slide whilst hiding the rest
function carousel() {
  $("#move-right").click(function() {
    var next_slide_id = "#" + $(".slide-active").next('.slide').attr("id");
    $(".slide").removeClass("slide-active").removeClass("slide-hidden").addClass("slide-hidden");
    if (next_slide_id !== "#undefined") {
      $(next_slide_id).addClass("slide-active").removeClass("slide-hidden");
    } else {
      $("#slide1").addClass("slide-active").removeClass("slide-hidden");
    }
  });
  $("#move-left").click(function() {
    var prev_slide_id = "#" + $(".slide-active").prev('.slide').attr("id");
    $(".slide").removeClass("slide-active").removeClass("slide-hidden").addClass("slide-hidden");
    if (prev_slide_id !== "#undefined") {
      $(prev_slide_id).addClass("slide-active").removeClass("slide-hidden");
    } else {
      $("#slide5").addClass("slide-active").removeClass("slide-hidden");
    }
  });
}
