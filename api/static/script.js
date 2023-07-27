var i = 0;
var txt = 'Hi! I\'m John.';
var speed = 25;



function typeWriter() {
  if (i < txt.length) {
    document.getElementById('typing').innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

var headerText = document.querySelectorAll('.technicolor');

window.addEventListener('scroll', function() {
  var scrollDist = window.scrollY;
  var hue = scrollDist / 10;
  var color = 'linear-gradient(to bottom right, hsl(' + hue + ', 50%, 75%), hsl(' + (hue + 60) + ', 50%, 75%), hsl(' + (hue + 120) + ', 50%, 75%), hsl(' + (hue + 180) + ', 50%, 75%), hsl(' + (hue + 240) + ', 50%, 75%), hsl(' + (hue + 300) + ', 50%, 75%))';
  headerText.forEach(function(element) {
    element.style.background = color;
    element.style.webkitBackgroundClip = 'text';
    element.style.webkitTextFillColor = 'transparent';
  });
});

window.addEventListener('load', function() {
  window.dispatchEvent(new Event('scroll'));
});