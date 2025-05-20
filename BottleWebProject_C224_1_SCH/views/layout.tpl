<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/style_infection_spread.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/style_cell_colonies.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="navbar navbar-custom navbar-fixed-top">
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li class="logo">
                    <a href="/home">
                        <img src="/static/images/icon.png" alt="Logo">
                    </a>
                </li>
                <li class="links">
                    <div class="button-container">
                        <a href="/wolf_island" class="nav-button">Death and reproduction</a>
                        <a href="/infection_spread" class="nav-button">The spread of infection</a>
                        <a href="/cells_colonies" class="nav-button">Colonies of living cells</a>
                        <a href="/about" class="nav-button">About authors</a>
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
    </div>
    <footer class="footer-style">
  <div class="footer">
  <div class="columns">
    <h1>Navigation</h1>
    <ul>
      <li><a href="/home" class="nav-link">Home</a></li>
      <li><a href="/wolf_island" class="nav-link">Death and reproduction</a></li>
      <li><a href="/infection_spread" class="nav-link">The spread of infection</a></li>
      <li><a href="/cells_colonies" class="nav-link">Colonies of living cells</a></li>
      <li><a href="/about" class="nav-link">About authors</a></li>
    </ul>
  </div>
  <div class="rating-section">
    <h1>Rate Our Site</h1>
    <form id="star-rating-form">
      <div id="stars">
        <span data-value="1">☆</span>
        <span data-value="2">☆</span>
        <span data-value="3">☆</span>
        <span data-value="4">☆</span>
        <span data-value="5">☆</span>
      </div>
      <input type="hidden" id="rating-value" name="rating" value="">
      <div class="back-to-top">
      <button class="buttons" type="submit">Submit</button>
      </div>
    </form>
    <div id="star-message"></div>
  </div>

  <div class="contact-info">
    <h3>Contact Us</h3>
    <p>Address: 123 Automaton St., Tech City</p>
    <p>Phone: +123 456 7890</p>
    <p>Email: info@cellularautomata.com</p>
    <div class="social-links">
    <img class="d-none d-lg-inline" style="max-height: 3rem;" src="https://src.guap.ru/logos/suai/suai-desc-line.svg" alt="Saint-Petersburg State University of Aerospace Instrumentation (SUAI)">
      <a href="https://guap.ru/en">Website</a>
      <a href="https://vk.com/guap_ru">VK</a>
      <a href="https://t.me/s/new_guap/10249">Telegram</a>
    </div>
  </div>
</div>

<div class="back-to-top">
  <button class="buttons" onclick="window.scrollTo({ top: 0, behavior: 'smooth' });">Back to Top</button>
</div>

<div class="copy">
  © 2025 Practice with Opaleva & Bartasevich. All rights reserved.
</div>
</footer>

<script>
  const stars = document.querySelectorAll('#stars span');
  const ratingInput = document.getElementById('rating-value');
  const messageDiv = document.getElementById('star-message');

  let currentRating = 0;

  stars.forEach(star => {
    star.addEventListener('mouseover', () => {
      const val = parseInt(star.getAttribute('data-value'));
      highlightStars(val);
    });

    star.addEventListener('mouseout', () => {
      highlightStars(currentRating);
    });

    star.addEventListener('click', () => {
      currentRating = parseInt(star.getAttribute('data-value'));
      ratingInput.value = currentRating;
      highlightStars(currentRating);
    });
  });

  function highlightStars(rating) {
    stars.forEach(star => {
      if (parseInt(star.getAttribute('data-value')) <= rating) {
        star.style.color = 'gold';
      } else {
        star.style.color = 'gray';
      }
    });
  }

  document.getElementById('star-rating-form').addEventListener('submit', function(e) {
    e.preventDefault();
    if (currentRating > 0) {
      messageDiv.style.display = 'block';
      messageDiv.innerText = 'Thank you for your rating of ' + currentRating + ' star(s)!';
    } else {
      messageDiv.style.display = 'block';
      messageDiv.innerText = 'Please select a rating before submitting.';
    }
  });
</script>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>