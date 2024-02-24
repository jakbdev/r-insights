var i = 0;
var j = 0;
function move() {

  if (i == 0) {
    i = 1;

    var rocket = document.getElementById("rocket");
    var x = 0;
    var y = 0
    var id = setInterval(frame, 25);

    function frame() {
      if (x > 200) {
        clearInterval(id);
        i = 0;

        var rocket2 = document.getElementById("rocket2")
        var x2 = 0;
        var y2 = 0;
        var id2 = setInterval(frame2, 25);
        
        function frame2() {
            if (x2 > 1300) {
              clearInterval(id2);
              j = 0;
              rocket2.style.display = "none";
            } else {
              x2 = x2 + 10
              y2 = y2 + 10
              rocket2.style.right = y2 + "px";
              rocket2.style.top = x2 + "px";
            }
          }

      } else {
        x = x + 10
        y = y + 10
        rocket.style.left = y + "px";
        rocket.style.bottom = x + "px";
      }
    }
  }
}
