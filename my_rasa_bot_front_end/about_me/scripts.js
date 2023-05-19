
const audio_click = new Audio("../audios/click.mp3");

function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    audio_click.play();
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    audio_click.play();
  }

// JavaScript for showing/hiding the dropdown items
document.addEventListener("DOMContentLoaded", function() {
  var creditsBtn = document.querySelector(".credits-btn");
  var documentationBtn = document.querySelector(".documentation-btn");
  var techDependenciesBtn = document.querySelector(".tech-dependencies-btn");
  var demoVideoBtn = document.querySelector(".demo-video-btn");

  var creditsDetails = document.querySelector(".credits-details");
  var documentationDetails = document.querySelector(".documentation-details");
  var techDependenciesDetails = document.querySelector(".tech-dependencies-details");
  var demoVideoDetails = document.querySelector(".demo-video-details");

  creditsBtn.addEventListener("click", function() {
    creditsDetails.classList.toggle("show");
    audio_click.play();
  });

  documentationBtn.addEventListener("click", function() {
    documentationDetails.classList.toggle("show");
    audio_click.play();
  });

  techDependenciesBtn.addEventListener("click", function() {
    techDependenciesDetails.classList.toggle("show");
    audio_click.play();
  });

  demoVideoBtn.addEventListener("click", function() {
    demoVideoDetails.classList.toggle("show");
    audio_click.play();
  });
});
