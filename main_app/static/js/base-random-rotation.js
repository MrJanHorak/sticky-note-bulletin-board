$(function () {
  var d = 300;
  $(".stickynote").each(function () {
    var $this = $(this);
    var r = Math.floor(Math.random()*5 ) ;
    $this.css({
      "-moz-transform": "rotate(" + r + "deg)",
      "-webkit-transform": "rotate(" + r + "deg)",
      transform: "rotate(" + r + "deg)",
    });
  });
  
  $("#navigation a").each(function () {
    var $this = $(this);
    var r = Math.floor(Math.random() * 41) - 20;
    $this.css({
      "-moz-transform": "rotate(" + r + "deg)",
      "-webkit-transform": "rotate(" + r + "deg)",
      transform: "rotate(" + r + "deg)",
    });
    
    $this.stop().animate(
      {
        marginTop: "-70px",
      },
      (d += 150)
    );
  });
  $("#navigation > li")
    .hover(
      function () {
        var $this = $(this);
        $("a", $this).stop().animate(
          {
            marginTop: "-40px",
          },
          200
        );
      },
      function () {
        var $this = $(this);
        $("a", $this).stop().animate(
          {
            marginTop: "-70px",
          },
          200
        );
      }
    )
    .click(function () {
      var $this = $(this);
      var name = this.className;
      $("").animate({ marginTop: -600 }, 300, function () {
        var $this = $(this);
        var r = Math.floor(Math.random() * 41) - 20;
        $this.css({
          "-moz-transform": "rotate(" + r + "deg)",
          "-webkit-transform": "rotate(" + r + "deg)",
          transform: "rotate(" + r + "deg)",
        });
        $("#" + name).show();
        $this.animate({ marginTop: -200 }, 300);
      });
    });
});
