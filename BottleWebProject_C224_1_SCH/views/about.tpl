% rebase('layout.tpl', title=title, year=year)

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="static/content/style_about.css">
</head>
<body>
    <div class="content-wrapper">
        <h2 class="page-title">{{ title }}</h2>
        <h3 class="subtitle">This web project was developed by 3rd year students of the C224 FSPO GUAP group</h3>

        <div class="authors-container">
            <div class="author-card">
                <div class="author-image">
                    <img src="static/images/chernyshova_s.png" alt="Sofya Chernyshova">
                </div>
                <div class="author-info">
                    <h4>Chernyshova Sofya Leonidovna</h4>
                    <p><strong>Contribution:</strong> Created the project repository, developed the "Infection Spread" model - a simulation of ringworm on a skin area, and designed the main page and header of the site.</p>
                    <a href="https://vk.com/sofkkar" class="vk-link">
                        <img src="static/images/vk_icon.png" alt="VK">
                    </a>
                </div>
            </div>

            <div class="author-card">
                <div class="author-image">
                    <img src="static/images/stebunov_n.jpg" alt="Nikita Stebunov">
                </div>
                <div class="author-info">
                    <h4>Stebunov Nikita Yuryevich</h4>
                    <p><strong>Contribution:</strong> Created the README.md file, developed the "Wolf Island" model - an ecosystem with population dynamics of rabbits, wolves, and she-wolves, and designed this "About authors" page.</p>
                    <a href="https://vk.com/xent7are" class="vk-link">
                        <img src="static/images/vk_icon.png" alt="VK">
                    </a>
                </div>
            </div>

            <div class="author-card">
                <div class="author-image">
                    <img src="static/images/khrustaleva_u.jpg" alt="Ulyana Khrustaleva">
                </div>
                <div class="author-info">
                    <h4>Khrustaleva Ulyana Mikhailovna</h4>
                    <p><strong>Contribution:</strong> Developed the "Cell Life" model - the evolution of cell colonies with customizable rules, and created the website footer with additional information.</p>
                    <a href="https://vk.com/darkpss" class="vk-link">
                        <img src="static/images/vk_icon.png" alt="VK">
                    </a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>