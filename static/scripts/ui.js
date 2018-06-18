$(document).ready(function() {
  var min_content_height = $(window).height() - $("header").outerHeight() -
                           ($("footer").outerHeight() * 2) - $("nav").outerHeight();
  $("main").css("min-height", min_content_height + "px");
  $(window).resize(function() {
    var min_content_height = $(window).height() - $("header").outerHeight() -
                             ($("footer").outerHeight() * 2) - $("nav").outerHeight();
    $("main").css("min-height", min_content_height + "px");
  });
});
