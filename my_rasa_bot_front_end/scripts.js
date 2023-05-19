
const audio_click = new Audio("./audios/click.mp3");

function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    audio_click.play();
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    audio_click.play();
  }

