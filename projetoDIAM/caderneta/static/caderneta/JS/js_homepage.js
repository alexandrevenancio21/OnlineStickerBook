
  //viragem das cartas
  document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.card');
    [...cards].forEach((card)=>{
      card.addEventListener('click', function() {
        card.classList.toggle('is-flipped');
      });
    });
  });


