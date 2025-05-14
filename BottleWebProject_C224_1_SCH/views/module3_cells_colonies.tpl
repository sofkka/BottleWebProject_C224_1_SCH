% rebase('layout.tpl', title=title, year=year)

<body>
<h2>{{ title }}.</h2>
<h3>{{ message }}</h3>

<p>Use this area to provide additional information.</p>
    <form id="paramsForm">
        <label>Parameter a the number of neighbors to reproduce (1-8):: <input type="number" id="a" name="a" value="{{params['a']}}" min="0" max="8"></label>
        <label>Parameter b fewer neighbors (2-8): <input type="number" id="b" name="b" value="{{params['b']}}" min="0" max="8"></label>
        <label>Parameter c more neighbors (1-7): <input type="number" id="c" name="c" value="{{params['c']}}" min="0" max="8"></label>
        <button type="button" onclick="setParams()">Update Parameters</button>
    </form>

    <button id="startBtn">Start</button>
    <button id="pauseBtn">Pause</button>
    <button id="resetBtn">Reset</button>

    <div id="gridContainer"></div>

    <script>
        const width = 20;
        const height = 20;
        let grid = [];
        let intervalId = null;
        let params = {
            'a': parseInt(document.getElementById('a').value),
            'b': parseInt(document.getElementById('b').value),
            'c': parseInt(document.getElementById('c').value)
        };

        function initGrid() {
            grid = [];
            for (let y=0; y<height; y++) {
                let row = [];
                for (let x=0; x<width; x++) {
                    row.push(0);
                }
                grid.push(row);
            }
        }

        function renderGrid() {
            const container = document.getElementById('gridContainer');
            container.innerHTML = '';
            for (let y=0; y<height; y++) {
                const rowDiv = document.createElement('div');
                rowDiv.className = 'row';
                for (let x=0; x<width; x++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell ' + (grid[y][x] ? 'alive' : 'dead');
                    cell.onclick = () => {
                        grid[y][x] = grid[y][x] ? 0 : 1;
                        renderGrid();
                    };
                    rowDiv.appendChild(cell);
                }
                container.appendChild(rowDiv);
            }
        }

        function setParams() {
            params.a = parseInt(document.getElementById('a').value);
            params.b = parseInt(document.getElementById('b').value);
            params.c = parseInt(document.getElementById('c').value);
        }

        async function step() {
            const response = await fetch('/step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({grid: grid, params: params})
            });
            const data = await response.json();
            grid = data.grid;
            renderGrid();
        }

        function start() {
            if (intervalId) clearInterval(intervalId);
            intervalId = setInterval(step, 500);
        }

        function pause() {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
            }
        }

        function reset() {
            pause();
            initGrid();
            renderGrid();
        }

        document.getElementById('startBtn').onclick = start;
        document.getElementById('pauseBtn').onclick = pause;
        document.getElementById('resetBtn').onclick = reset;

        window.onload = () => {
            initGrid();
            renderGrid();
        };
    </script>
</body>
</html>