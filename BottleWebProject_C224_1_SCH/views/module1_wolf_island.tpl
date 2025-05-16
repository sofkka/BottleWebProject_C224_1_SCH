% rebase('layout.tpl', title=title, year=year)

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="static/content/style_wolf_island.css">
</head>
<body>
    <div class="content-wrapper">
        <h2>{{ title }}</h2>

        <div class="simulation-wrapper">
            <div class="left-panel">
                <h3>Simulation Parameters</h3>
                <div class="input-row">
                    <label>Island Width (N, 5-15):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Island Height (M, 5-15):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Initial Rabbits (1 to N*M/10):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Initial Wolves (1 to N*M/10):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Initial She-Wolves (1 to N*M/10):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Simulation Steps (10-240):</label>
                    <input type="text">
                </div>
                <div class="action-buttons">
                    <button>Generate random values</button>
                </div>
                <div class="action-buttons">
                    <button>Reset</button>
                    <button>Start</button>
                </div>
            </div>
            <div class="middle-panel">
                <h3>Population Statistics</h3>
                <div class="stats">
                    <p>Simulation step: 0</p>
                    <p>Rabbits: 0</p>
                    <p>Wolves: 0</p>
                    <p>She-Wolves: 0</p>
                </div>
                <button class="save-button">Save to Json</button>
                <button class="about-button">About Wolf Island</button>
            </div>
            <div class="right-panel">
                <div class="grid"></div>
            </div>
        </div>

        <div class="about-section">
            <h3 class="about-title">About Wolf Island</h3>
            <p>The Wolf Island model is a simulation from the field of queuing systems and models of death and reproduction. It is designed as an interactive tool for studying ecosystem dynamics, allowing you to analyze the interaction of species, their reproduction and survival. The model is intended for educational purposes, helping students, teachers and researchers in the field of ecology and mathematical modeling to conduct experiments with various initial conditions and observe the behavior of populations in real time.</p>
            <p>The Wolf Island model considers an ecosystem on an NxM-sized island inhabited by rabbits, wolves, and she-wolves. Rabbits move randomly: with a probability of 8/9, one of the eight neighboring directions is selected, or with a probability of 1/9, they remain stationary. Each rabbit reproduces with a probability of 0.3, creating another rabbit. She-wolves hunt rabbits: if there is prey in the next cell, they move there, eat the rabbit and get 1 point, and if there is no prey, they lose 0.1 points. Wolves act similarly to she-wolves, but if there are no rabbits nearby and there is a she-wolf nearby, they start chasing her. If a wolf and a she-wolf end up in the same cell without rabbits, offspring of random sex are created. All predators (wolves and she-wolves) start with 1 point, and when they reach zero points, they die. Rabbits can only be eaten by predators. The simulation allows you to set the size of the island, the initial number of individuals and the duration of the process, providing visualization of changes and saving the results for further analysis.</p>
        </div>
    </div>

    <script>
        document.querySelector('.about-button').addEventListener('click', function() {
            document.querySelector('.about-section h3').scrollIntoView({ behavior: 'smooth' });
        });
    </script>
</body>
</html>