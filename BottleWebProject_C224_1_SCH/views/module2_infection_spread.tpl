% rebase('layout.tpl', title=title, year=year)

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
</head>

<h2>{{ title }}</h2>
<div class="link-to-theory">
    <h3>{{ message }}</h3>
    <p class="theory-link"><a href="#theory-section">Read theory</a></p>
</div>

<div class="infection-spread" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <div class="container">
        <div class="controls">
            <!-- Defines a form for selecting the grid size, submitting via GET to the '/infection_spread' route. -->
            <form id="size-form" method="GET" action="/infection_spread">
                <label for="field-size">Choose the field size (odd):</label>
                <div class="slider-row">
                    <span class="range-limits">3</span>
                    <input type="range" id="field-size" name="size" min="3" max="15" value="{{initial_size}}" step="2">
                    <span class="range-limits">15</span>
                </div>
                <div class="field-value-wrapper">
                    <span id="field-value">{{initial_size}}</span>
                </div>
                <div class="two-buttons">
                    <button type="button" class="buttons" id="start-button">Start</button>
                    <button type="button" class="buttons" id="save-button">Save to JSON</button>
                </div>
                <div class="two-buttons">
                    <button type="button" class="buttons" id="reset-button" style="display: none;">Reset</button>
                </div>
            </form>
        </div>

        <div class="grid-wr">
            <div class="grid-container" id="grid"></div>
        </div>
    </div>

    <div class="simulation-message" id="simulation-message">
        Simulation finished, you can start again
    </div>

    <span id="timer">00:00</span>
</div>

<div class="about-section">
    <h2 class="about-title" id="theory-section">Theory</h2>

    <h3>About Infection Spread Model</h3>
    <p>The Infection Spread Model is a simulation from the domain of queuing systems and models of death and reproduction, specifically designed to study the dynamics of ringworm infection on a skin patch. Implemented as an interactive tool, it allows users to explore how an infection propagates across an n * n grid of cells, where n is odd, starting from a single infected central cell. The model serves as an educational resource for students, educators, and researchers in epidemiology, mathematical modeling, and computational biology, enabling experiments with varying grid sizes and real-time visualization of infection dynamics.</p>
    <br>
    <p>The model operates as a Probabilistic Cellular Automaton, where each cell represents a patch of skin and can be in one of three states: Healthy (H), Infected (I), or Resistant (R). The central cell is initially infected, and the infection spreads stochastically: an infected cell can infect any of its four adjacent healthy neighbors with a probability of 0.5 per time step. After 6 time units, an infected cell becomes resistant, gaining immunity for 4 time units, after which it returns to a healthy state. The simulation updates all cells synchronously, tracking their states and timers to reflect the infection's progression.</p>
    <br>
    <p>Users can configure the grid size (n, odd), observe the infection's spread in real-time, and save the results for analysis. The model provides insights into stochastic processes, epidemic dynamics, and the impact of immunity, making it a valuable tool for studying probabilistic systems and their applications in biological contexts.</p>
    
    <div id="vero-klet-avt">
        <div>
            <br><h3>Model: Probabilistic Cellular Automaton</h3>
            <p>A Probabilistic Cellular Automaton (PCA), also known as a stochastic cellular automaton, is a computational model used to simulate dynamic systems where cell states evolve based on probabilistic rules. Unlike deterministic cellular automata, where state transitions are fixed, PCAs incorporate randomness, making them suitable for modeling processes with uncertainty, such as disease spread or population dynamics.</p>
            <p><b>Structure and Rules:</b></p>
            <ul>
                <li>Grid: The PCA consists of a grid of cells, typically arranged in a square lattice (e.g., n * n). Each cell can be in one of a finite number of states (e.g., healthy, infected, resistant).</li>
                <li>Neighborhood: Each cell has a defined neighborhood, usually the four adjacent cells (up, down, left, right), which influence its state transitions.</li>
                <li>Probabilistic Transitions: Rules governing state changes are defined by probabilities. For example, a cell may transition from one state to another based on its current state, the states of its neighbors, and a probability distribution.</li>
                <li>Synchronous Updates: All cells update their states simultaneously at each time step, ensuring a consistent simulation of the system's evolution.</li>
            </ul>
            <p>PCAs are widely used in fields like epidemiology, ecology, and physics to model complex systems where stochastic processes play a critical role.</p>
        </div>
        <img src="/static/images/vero_klet_avtomat.png" alt="Probabilistic Cellular Automaton">
    </div>

    <br><h3>Algorithm for Solving the Problem</h3>
    <p>The simulation of infection spread (ringworm) on a skin patch is implemented using a Probabilistic Cellular Automaton. The algorithm models the infection dynamics on an n * n grid, where n is odd, with the central cell initially infected. The following steps outline the process:</p>
    <ol>
        <b><li>Initialization:</li></b>
        <ul>
            <li>Create an n * n grid where each cell has a state: Healthy (H), Infected (I), or Resistant (R).</li>
            <li>Set the central cell to Infected (I) and all others to Healthy (H).</li>
            <li>Assign a timer to each cell to track the time spent in its current state (I or R).</li>
        </ul>
        <br>
        <b><li>Grid Update (at each time step):</li></b>
        <ul>
            <li>State Transitions:</li>
            <ul>
                <li>For each Infected (I) cell: If 6 time units have passed, transition to Resistant (R) and reset the timer.</li>
                <li>For each Resistant (R) cell: If 4 time units have passed, transition to Healthy (H) and reset the timer.</li>
            </ul>
            <li>Infection Spread:
            <ul>
                <li>For each Infected (I) cell, check its four adjacent neighbors (up, down, left, right).</li>
                <li>If a neighbor is Healthy (H), it becomes Infected (I) with a probability of 0.5, and its timer is reset.</li>
            </ul>
            <li>Timer Update: Increment the timer for all Infected (I) and Resistant (R) cells.</li>
        </ul>
        <br>
        <b><li>Output:</li></b>
        <p>At each time step, display the grid, marking cells as:</p>
        <ul>
            <li>I: Infected</li>
            <li>R: Resistant</li>
            <li>H: Healthy</li>
        </ul>
        <br>
        <b><li>Simulation:</li></b>
        <ul>
            <li>Run the simulation for a specified number of steps (e.g., 15).</li>
            <li>Update the grid and output its state at each step to visualize the infection's progression.</li>
        </ul>
    </ol>
    <p>This algorithm ensures accurate modeling of the infection spread while adhering to the probabilistic and temporal rules specified.</p>
</div>


<!-- Injects server-side data into global variables for use in the external JavaScript file. -->
<script>
    window.simulationSteps = {{ !simulation_steps_json }};
    window.gridSize = {{ initial_size }};
    window.finalGridState = {{ !final_grid_json }};
    window.allCellsHealthy = {{ 'true' if all_healthy else 'false' }};
</script>

<script src="/static/scripts/module2_infection_spread.js"></script>
