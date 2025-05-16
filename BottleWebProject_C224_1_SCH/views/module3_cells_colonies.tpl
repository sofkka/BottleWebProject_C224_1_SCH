% rebase('layout.tpl', title=title, year=year)

<h2>{{ title }}.</h2>
<h3>{{ message }}</h3>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
</head>
<div class="layout">
    <div class="cells-container">
        <div class="grid-wrapper">
            <table class="grid-table" id="gridTable">
                <tr><td class="alive"></td><td class="alive"></td><td></td></tr>
                <tr><td></td><td class="alive"></td><td></td></tr>
                <tr><td class="alive"></td><td></td><td></td></tr>
            </table>
        </div>
        <div class="settings">
            <p class="leader">Choose:</p>
            <p class="leader">
                the field size: 
                <input type="number" class="parameters" name="field_width" id="fieldWidth" value="3" min="1" max="50">
                X
                <input type="number" class="parameters" name="field_height" id="fieldHeight" value="3" min="1" max="50">
            </p>
            <p class="leader">
                Parameter a the number of neighbors to reproduce (1-8): 
                <select class="parameters" name="neighbors_reproduce" id="neighborsReproduce">
                    % for i in range(1, 9):
                        <option value="{{ i }}">{{ i }}</option>
                    % end
                </select>
            </p>
            <p class="leader">
                Parameter b Fewer neighbors (2-8): 
                <select class="parameters" name="fewer_neighbors" id="fewerNeighbors">
                    % for i in range(2, 9):
                        <option value="{{ i }}">{{ i }}</option>
                    % end
                </select>
            </p>
            <p class="leader">
                Parameter c More neighbors (1-7): 
                <select class="parameters" name="more_neighbors" id="moreNeighbors">
                    % for i in range(1, 8):
                        <option value="{{ i }}">{{ i }}</option>
                    % end
                </select>
            </p>
            <div class="buttons-container">
                <button type="submit" class="buttons" name="action" value="start" id="startBtn">Start</button>
                <button type="submit" class="buttons" name="action" value="pause" id="pauseBtn">Pause</button>
                <button type="submit" class="buttons" name="action" value="reset" id="resetBtn">Reset</button>
            </div>
            <div class="buttons-container">
                <button type="button" class="buttons" id="saveJsonBtn">Save to JSON</button>
            </div>
        </div>
    </div>
    <div class="theory-section about-section">
        <p class="leader about-title">Theory</p>
        <p class="lead">
            Develop a program that simulates the life of generations of hypothetical colonies of living cells that survive, multiply or die 
            in accordance with the following rules:
            <br><br>
            1. If a living cell has fewer than 2 (a) or more than 3 (b) neighbors in a neighborhood of 8 cells, then it dies 
            in the next generation (simulation of real conditions - lack of nutrition or overpopulation), otherwise it survives;
        </p>
        <div class="buttons-container images">
            <img src="/static/images/1.jpg" alt="cell1" class="images">
            <img src="/static/images/2.jpg" alt="cell2" class="images">
        </div>
        <p class="lead">
            2. A live cell appears in an empty cell if the original cell has exactly 3 (c) neighbors. Moreover, the process of birth and 
            death occurs in 1 step (tick).
        </p>
        <div class="buttons-container images">
            <img src="/static/images/3.jpg" alt="cell3" class="images">
            <img src="/static/images/4.jpg" alt="cell4" class="images">
        </div>
        <p class="lead">
            Modify the task so that the number of "neighbors" in which the cell dies or multiplies, the numbers a, b, c, can be changed 
            by the user.
            The algorithm implements a simulation of a cellular automaton, where each cell on a two-dimensional grid can be in one of 
            two states: alive or dead. The process is modeled in stages (in one tick), during which the states of all cells are updated 
            simultaneously according to the set rules. The model takes into account user parameters - the numbers a, b, and c, 
            which determine the conditions of cell death and reproduction.
        </p>
        <h1>About Cellular Automaton</h1>
        <p class="lead">
            A cellular automaton is a mathematical model used to simulate complex systems made up of simple, discrete cells. 
            Each cell exists in a specific state (such as alive or dead) and changes its state over time according to a set of rules 
            based on the states of its neighboring cells. Despite the simplicity of these rules, cellular automata can produce highly 
            complex and interesting patterns, making them useful for studying phenomena in physics, biology, computer science, and other fields. 
            One of the most famous examples is Conway Game of Life, which demonstrates how simple rules can lead to unpredictable and dynamic behaviors.
        </p>
        <h1>Algorithm Stages:</h1>
        <ol class="lead">
            <li>
                <strong>Initialization:</strong><br/>
                Create a two-dimensional array (matrix) of a given size nXn, where each cell is in a specific state (alive or dead). 
                Set the initial state of the cellular area (for example, randomly or according to user settings).
            </li>
            <li>
                <strong>Entering parameters:</strong><br/>
                Get the values of the numbers a, b, c - threshold values for cell death and reproduction, set by the user.
            </li>
            <li>
                <strong>Calculation of neighbors for each cell:</strong><br/>
                For each cell, count the number of neighbors in the "live" state. When calculating, take into account 8 neighboring cells 
                (horizontally, vertically, and diagonally), considering boundary conditions (for example, a toroidal area or fixed boundaries).
            </li>
            <li>
                <strong>Applying the update rules:</strong><br/>
                For each cell, determine its new state according to the following rules:
                <ul>
                    <li>
                        <strong>If the cell is alive:</strong><br/>
                        - Dies if the number of neighbors is less than a or more than b.<br/>
                        - Survives otherwise.
                    </li>
                    <li>
                        <strong>If the cell is dead:</strong><br/>
                        - Becomes alive again if the number of neighbors is c.<br/>
                        - Remains dead in all other cases.
                    </li>
                </ul>
            </li>
        </ol>
    </div>
</div>

<script>
    function updateGrid() {
        const width = parseInt(document.getElementById('fieldWidth').value);
        const height = parseInt(document.getElementById('fieldHeight').value);

        if (width < 1 || height < 1 || width > 50 || height > 50) {
            alert('Please enter values between 1 and 50.');
            return;
        }

        const table = document.getElementById('gridTable');
        table.innerHTML = '';

        for (let i = 0; i < height; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < width; j++) {
                const cell = document.createElement('td');
                cell.className = '';
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        adjustCellSizes();
    }

    function adjustCellSizes() {
        const gridWrapper = document.querySelector('.grid-wrapper');
        const settings = document.querySelector('.settings');
        const table = document.getElementById('gridTable');
        const width = parseInt(document.getElementById('fieldWidth').value);
        const height = parseInt(document.getElementById('fieldHeight').value);

        const containerWidth = document.querySelector('.cells-container').offsetWidth;
        const settingsWidth = settings.offsetWidth;
        const availableWidth = containerWidth - settingsWidth - 40;
        const cellSize = Math.min(Math.floor(availableWidth / width), 60);
        const cells = table.querySelectorAll('td');
        cells.forEach(cell => {
            cell.style.width = `${cellSize}px`;
            cell.style.height = `${cellSize}px`;
            cell.style.aspectRatio = '1 / 1';
        });

        table.style.width = `${cellSize * width}px`;
        table.style.height = `${cellSize * height}px`;
    }

    document.getElementById('fieldWidth').addEventListener('input', function() {
        document.getElementById('fieldHeight').value = this.value;
        updateGrid();
    });

    document.getElementById('fieldHeight').addEventListener('input', function() {
        document.getElementById('fieldWidth').value = this.value;
        updateGrid();
    });

    window.addEventListener('resize', adjustCellSizes);

    updateGrid();
</script>