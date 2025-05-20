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

        <form method="GET" action="/wolf_island">
            <input type="hidden" name="save" value="">
            <div class="simulation-wrapper">
                <div class="left-panel">
                    <h3>Simulation Parameters</h3>
                    <div class="input-row">
                        <label>Island Width (N, 5-15):</label>
                        <input type="text" name="N" value="{{N}}">
                    </div>
                    <div class="input-row">
                        <label>Island Height (M, 5-15):</label>
                        <input type="text" name="M" value="{{M}}">
                    </div>
                    <div class="input-row">
                        <label>Initial Rabbits (1 to N*M/10):</label>
                        <input type="text" name="rabbits" value="{{rabbits}}">
                    </div>
                    <div class="input-row">
                        <label>Initial Wolves (1 to N*M/10):</label>
                        <input type="text" name="wolves" value="{{wolves}}">
                    </div>
                    <div class="input-row">
                        <label>Initial She-Wolves (1 to N*M/10):</label>
                        <input type="text" name="she_wolves" value="{{she_wolves}}">
                    </div>
                    <div class="input-row">
                        <label>Simulation Steps (10-240):</label>
                        <input type="text" name="steps" value="{{steps}}">
                    </div>
                    <div class="action-buttons">
                        <button type="submit" name="action" value="generate">Generate random values</button>
                    </div>
                    <div class="action-buttons">
                        <button type="submit" name="action" value="reset">Reset</button>
                        <button type="submit" name="action" value="start">Start</button>
                    </div>
                </div>
                <div class="middle-panel">
                    <h3>Population Statistics</h3>
                    <div class="stats">
                        <p>Simulation step: {{stats['step']}}</p>
                        <p>Rabbits: {{stats['rabbits']}}</p>
                        <p>Wolves: {{stats['wolves']}}</p>
                        <p>She-Wolves: {{stats['she_wolves']}}</p>
                    </div>
                    <button type="submit" class="save-button" name="action" value="save">Save to Json</button>
                    <button class="about-button">About Wolf Island</button>
                </div>
                <div class="right-panel">
                    <div class="grid">
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

        <div class="about-section">
            <h2 class="about-title">Theory</h2>

            <h3>About the "Wolf Island" model</h3>
            <p>The "Wolf Island" model is a simulation from the field of queuing systems and models of death and reproduction, developed as an interactive educational tool. It allows students, teachers and researchers in the field of ecology and mathematical modeling to study the dynamics of ecosystems, analyze the interaction of species, their reproduction and survival, conducting experiments with different initial conditions and observing the behavior of populations in real time.</p>
            <p>The ecosystem is modeled on an island of size NxM (where 5 <= N, M <= 15) inhabited by rabbits, wolves and she-wolves. Rabbits move randomly: with a probability of 8/9 they choose one of the eight neighboring directions, and with a probability of 1/9 they stay in place. Each rabbit reproduces with a probability of 0.3, creating a new rabbit in its cell. She-wolves hunt rabbits: if there is a rabbit in the current or neighboring cell, the she-wolf moves there, eats it and gets 1 point; if there is no prey, she loses 0.1 points. Wolves act similarly, but in the absence of rabbits and the presence of a she-wolf nearby, they begin to chase her. If a wolf and a she-wolf end up in the same cell without rabbits, offspring of a random sex with 1 point are born. Predators (wolves and she-wolves) die if their points reach zero.</p>
            <p>The simulation allows you to set the size of the island, the initial number of individuals (from 1 to [NxM/10] for each species) and the duration of the process (from 10 to 240 steps). The initial populations are placed either manually via the web interface (with the coordinates checked), or randomly. The results are displayed as a grid, where each cell shows the presence of entities, and the text information reflects the current number of each type. After the simulation is completed, the data is saved to a JSON file.</p>

            <h3>The modeling algorithm</h3>
            <p>The algorithm consists of three main stages: initialization, simulation cycle, and output of results.</p>
            <ol>
                <li><b>Initialization</b>
                    <ul>
                        <li>A two-dimensional NxM grid is formed, where each cell can be empty or contain a rabbit, a wolf, or a she-wolf.</li>
                        <li>Initial populations are placed randomly or manually via the web interface. When entering incorrect data manually (for example, off-grid coordinates or the intersection of entities), an error message is sent with a suggestion to correct the input or use random placement.</li>
                        <li>Each predator is assigned 1 survival point.</li>
                    </ul>
                </li>
                <li><b>Simulation cycle</b>
                    <p>The cycle runs for a set number of steps T (10-240). At every step:</p>
                    <ul>
                        <li><b>Rabbit processing:</b>
                            <ul>
                                <li>With a probability of 0.3, the rabbit reproduces by creating a new rabbit in its cell.</li>
                                <li>With a probability of 1/9, the rabbit stays in place, with a probability of 8/9 it moves to a random neighboring cell (within the grid).</li>
                            </ul>
                        </li>
                        <li><b>Treatment of she-wolves:</b>
                            <ul>
                                <li>If there is a rabbit in the current cell, the she-wolf eats it, increasing points by 1.</li>
                                <li>If there is no rabbit, neighboring cells are checked. If there is a rabbit, the she-wolf moves there and eats it, getting 1 point.</li>
                                <li>If there are no rabbits, the she-wolf moves to a random neighboring cell, losing 0.1 points.</li>
                                <li>If the she-wolf's score is less than 0, she dies and is removed from the grid.</li>
                            </ul>
                        </li>
                        <li><b>Wolf treatment:</b>
                            <ul>
                                <li>If there is a rabbit in the current cell, the wolf eats it, increasing points by 1.</li>
                                <li>If there is no rabbit, neighboring cells are checked. If there is a rabbit, the wolf moves there and eats it, getting 1 point.</li>
                                <li>If there are no rabbits, but there is a she-wolf, the wolf moves to her. If they end up in the same cell without rabbits, offspring of a random sex with 1 point are born.</li>
                                <li>If there are no targets, the wolf moves to a random neighboring cell, losing 0.1 points.</li>
                                <li>If the wolf's score is less than 0, it dies and is removed from the grid.</li>
                            </ul>
                        </li>
                        <li><b>Updating the grid:</b> After processing all entities, the grid is updated to reflect new positions, the removal of the deceased and the appearance of offspring.</li>
                        <li><b>Collecting statistics:</b> The current number of rabbits, wolves, and she-wolves is calculated, and text fields in the web interface are updated.</li>
                    </ul>
                </li>
                <li><b>Visualization and output of results</b>
                    <ul>
                        <li>At each step, the web interface displays a grid with a visual representation of the entities and textual information about the number of species.</li>
                        <li>After the simulation is completed, the results are saved to a JSON file.</li>
                    </ul>
                </li>
            </ol>

            <h3>The Monte Carlo method</h3>
            <p>The Monte Carlo method is a statistical modeling or simulation method. This is a numerical method for solving problems by modeling random variables.</p>
            <p>The idea of the method is extremely simple and consists in the following. Instead of describing the process using an analytical apparatus, a drawing of a random phenomenon is carried out using a specially organized procedure that includes randomness and gives a random result. The implementation of a random process develops differently each time, i.e. we get different outcomes of the process under consideration. This set of implementations can be used as some kind of artificially obtained statistical material that can be processed using conventional methods of mathematical statistics. After such processing, you can get: the probability of an event, mathematical expectation, etc. Using the Monte Carlo method, any probabilistic problem can be solved, but it is justified when the drawing procedure is simpler, and not more complicated than analytical calculation.</p>
            <h4>Application of the Monte Carlo method in the Wolf Island model</h4>
            <p>In the framework of the Wolf Island model, the Monte Carlo method is used to simulate random events:</p>
            <ul>
                <li>Random movement of rabbits (probabilities 1/9 and 8/9).</li>
                <li>Reproduction of rabbits (probability 0.3).</li>
                <li>Random movement of wolves and she-wolves in the absence of targets.</li>
                <li>Random selection of the offspring's sex during mating.</li>
            </ul>
            <p>Multiple runs of the simulation allow you to collect statistical data on the behavior of the system, such as the average population size or the probability of species extinction.</p>
        </div>
    </div>

<script>
    document.querySelector('.about-button').addEventListener('click', function(event) {
        event.preventDefault();
        document.querySelector('.about-section h2').scrollIntoView({ behavior: 'smooth' });
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