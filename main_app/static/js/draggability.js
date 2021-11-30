function myFunction(x) {
  if (x.matches) { // If media query matches
    $("[id^=draggable]").draggable( "destroy" );
  } else {
    var positions = JSON.parse(localStorage.positions || "{}");
$(function () {
  var d = $("[id^=draggable]")

  $.each(positions, function (id, pos) {
    $("#" + id).css(pos);
  });
  
  d.draggable({
    containment: "#containment-wrapper",
    scroll: false,
    opacity: 0.4,
    stack: ".products",
    zIndex: 100,
    containment: "window",
    stop: function (event, ui) {
      positions[this.id] = ui.position;
      localStorage.positions = JSON.stringify(positions);
    },
  });
});
  }
}

var x = window.matchMedia("(max-width: 480px)")
myFunction(x) // Call listener function at run time
x.addListener(myFunction) // Attach listener function on state changes