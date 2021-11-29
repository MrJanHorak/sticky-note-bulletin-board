
var positions = JSON.parse(localStorage.positions || "{}");
$(function () {
  var d = $("[id=draggable]").attr("id", function (i) {
    return "draggable_" + i;
  });
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

