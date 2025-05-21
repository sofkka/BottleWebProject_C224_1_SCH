% rebase('layout.tpl', title=title, year=year)

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    % if refresh:
        <meta http-equiv="refresh" content="1">
    % end
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/content/style_wolf_island.css">
</head>
<body>
    <div class="content-wrapper">
        <h2>{{ title }}</h2>

        <form method="GET" action="/wolf_island" id="simulation-form">
            <input type="hidden" name="save" value="">
            <div class="simulation-wrapper">
                <div class="left-panel">
                    <h3>Simulation Parameters</h3>
                    <div class="input-row">
                        <label for="input-n">Island Width (N, 5-15):</label>
                        <input type="text" id="input-n" name="N" value="{{N}}" maxlength="2">
                    </div>
                    <div class="input-row">
                        <label for="input-m">Island Height (M, 5-15):</label>
                        <input type="text" id="input-m" name="M" value="{{M}}" maxlength="2">
                    </div>
                    <div class="input-row">
                        <label for="input-rabbits">Initial Rabbits (1 to N*M/10):</label>
                        <input type="text" id="input-rabbits" name="rabbits" value="{{rabbits}}" maxlength="2">
                    </div>
                    <div class="input-row">
                        <label for="input-wolves">Initial Wolves (1 to N*M/10):</label>
                        <input type="text" id="input-wolves" name="wolves" value="{{wolves}}" maxlength="2">
                    </div>
                    <div class="input-row">
                        <label for="input-she-wolves">Initial She-Wolves (1 to N*M/10):</label>
                        <input type="text" id="input-she-wolves" name="she_wolves" value="{{she_wolves}}" maxlength="2">
                    </div>
                    <div class="input-row">
                        <label for="input-steps">Simulation Steps (10-240):</label>
                        <input type="text" id="input-steps" name="steps" value="{{steps}}" maxlength="3">
                    </div>
                    <div class="action-buttons">
                        <button type="submit" id="btn-generate" name="action" value="generate">Generate random values</button>
                    </div>
                    <div class="action-buttons">
                        <button type="submit" id="btn-reset" name="action" value="reset">Reset</button>
                        <button type="submit" id="btn-start" name="action" value="start">Start</button>
                    </div>
                </div>
                <div class="middle-panel">
                    <h3>Population Statistics</h3>
                    <div class="stats" id="stats-panel">
                        <p>Simulation step: {{stats['step']}}</p>
                        <p>Rabbits: {{stats['rabbits']}}</p>
                        <p>Wolves: {{stats['wolves']}}</p>
                        <p>She-Wolves: {{stats['she_wolves']}}</p>
                    </div>
                    <button type="submit" id="btn-save" class="save-button" name="action" value="save">Save to Json</button>
                    <button id="btn-about" class="about-button">About Wolf Island</button>
                </div>
                <div class="right-panel">
                    <div class="grid" id="grid-panel">
                        % for i in range(15):
                            % for j in range(15):
                                % if i < N and j < M:
                                    <div class="cell">
                                        % if grid_data[i][j] == '/static/images/rabbit.png':
                                            <img src="/static/images/rabbit.png" alt="rabbit" style="width: 25px; height: 25px;">
                                        % elif grid_data[i][j] == '/static/images/wolf.png':
                                            <img src="/static/images/wolf.png" alt="wolf" style="width: 25px; height: 25px;">
                                        % elif grid_data[i][j] == '/static/images/she_wolf.png':
                                            <img src="/static/images/she_wolf.png" alt="she_wolf" style="width: 25px; height: 25px;">
                                        % end
                                    </div>
                                % else:
                                    <div class="cell inactive"></div>
                                % end
                            % end
                        % end
                    </div>
                </div>
            </div>
            % if error:
                <div id="error-message" style="color: red; text-align: center; margin-top: 10px;">{{error}}</div>
            % end
        </form>

        <div class="about-section" id="about-section">
            <h3 class="about-title">About Wolf Island</h3>
            <p>The Wolf Island model is a simulation from the field of queuing systems and models of death and reproduction. It is designed as an interactive tool for studying ecosystem dynamics, allowing you to analyze the interaction of species, their reproduction and survival. The model is intended for educational purposes, helping students, teachers and researchers in the field of ecology and mathematical modeling to conduct experiments with various initial conditions and observe the behavior of populations in real time.</p>
            <p>The Wolf Island model considers an ecosystem on an NxM-sized island inhabited by rabbits, wolves, and she-wolves. Rabbits move randomly: with a probability of 8/9, one of the eight neighboring directions is selected, or with a probability of 1/9, they remain stationary. Each rabbit reproduces with a probability of 0.3, creating another rabbit. She-wolves hunt rabbits: if there is prey in the next cell, they move there, eat the rabbit and get 1 point, and if there is no prey, they lose 0.1 points. Wolves act similarly to she-wolves, but if there are no rabbits nearby and there is a she-wolf nearby, they start chasing her. If a wolf and a she-wolf end up in the same cell without rabbits, offspring of random sex are created. All predators (wolves and she-wolves) start with 1 point, and when they reach zero points, they die. Rabbits can only be eaten by predators. The simulation allows you to set the size of the island, the initial number of individuals and the duration of the process, providing visualization of changes and saving the results for further analysis.</p>
        </div>
    </div>

<script>
    document.querySelector('#btn-about').addEventListener('click', function(event) {
        event.preventDefault();
        document.querySelector('#about-section h3').scrollIntoView({ behavior: 'smooth' });
    });

    const errorMessage = document.getElementById('error-message');
    if (errorMessage && errorMessage.textContent.includes('Cannot save results during simulation')) {
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 10000);
    }
</script>
</body>
</html>