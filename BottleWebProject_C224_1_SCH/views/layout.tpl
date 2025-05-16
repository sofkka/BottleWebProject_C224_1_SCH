<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My Bottle Application</title>
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
      <ul >
        <li><a href="index.html" class="h2">Home</a></li>
        <li><a href="articles.html" style="color:#fff; text-decoration:none;">Death and reproduction</a></li>
        <li><a href="about.html" style="color:#fff; text-decoration:none;">The spread of infection</a></li>
        <li><a href="contact.html" style="color:#fff; text-decoration:none;">Colonies of living cells</a></li>
        <li><a href="contact.html" style="color:#fff; text-decoration:none;">About authors</a></li>
      </ul>
    </div>
    
    <div style="flex:1; min-width:200px; margin-bottom:20px;">
      <h3 style="margin-bottom:10px;">Rate Our Site</h3>
      <form id="star-rating-form" style="display:flex; align-items:center;">
        <div id="stars" style="font-size: 2em; cursor: pointer;">
          <span data-value="1" style="color: gray;">★</span>
          <span data-value="2" style="color: gray;">★</span>
          <span data-value="3" style="color: gray;">★</span>
          <span data-value="4" style="color: gray;">★</span>
          <span data-value="5" style="color: gray;">★</span>
        </div>
        <input type="hidden" id="rating-value" name="rating" value="">
        <button type="submit" style="margin-left:10px; padding:8px; background-color:#555; color:#fff; border:none; cursor:pointer;">Submit</button>
      </form>
      <div id="star-message" style="margin-top:10px; font-size:14px; display:none;"></div>
    </div>
    
    <div style="flex:1; min-width:200px; margin-bottom:20px;">
      <h3 style="margin-bottom:10px;">Contact Us</h3>
      <p style="margin:0;">Address: 123 Automaton St., Tech City</p>
      <p style="margin:0;">Phone: +123 456 7890</p>
      <p style="margin:0;">Email: info@cellularautomata.com</p>

      <div style="margin-top:10px;">
        <a href="#" style="margin-right:10px; color:#fff; text-decoration:none;">Website</a>
        <a href="#" style="margin-right:10px; color:#fff; text-decoration:none;">Twitter</a>
        <a href="#" style="margin-right:10px; color:#fff; text-decoration:none;">Facebook</a>
        <a href="#" style="color:#fff; text-decoration:none;">Instagram</a>
      </div>
    </div>
    
  </div>
  <div style="text-align:center; margin-top:20px;">
    <button onclick="window.scrollTo({ top: 0, behavior: 'smooth' });" style="padding:10px 20px; background-color:#555; color:#fff; border:none; cursor:pointer;">Back to Top</button>
  </div>
  <div style="text-align:center; margin-top:10px; font-size:14px;">
    © 2024 Cellular Automaton. All rights reserved.
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