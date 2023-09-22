document.addEventListener('DOMContentLoaded', function () {
    const cardContainer = document.querySelector('.card-container');
    const cards = document.querySelectorAll('.card');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');

    let currentIndex = 0;

    function showCards() {
        cards.forEach((card, index) => {
            if (index >= currentIndex && index < currentIndex + 3) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    prevButton.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentIndex > 0) {
            currentIndex -= 3;
            showCards();
        }
    });

    nextButton.addEventListener('click', function (e) {
        e.preventDefault();
        if (currentIndex < cards.length - 3) {
            currentIndex += 3;
            showCards();
        }
    });

    showCards();
});

document.querySelectorAll('.scroll-links a').forEach(function(link) {
    link.addEventListener('click', function(event) {
      event.preventDefault();
      var targetId = this.getAttribute('href').substring(1); // Remove the '#'
      var targetElement = document.getElementById(targetId);

      // 해당 섹션으로 스크롤
      targetElement.scrollIntoView({
        behavior: 'smooth'
      });
    });
  });