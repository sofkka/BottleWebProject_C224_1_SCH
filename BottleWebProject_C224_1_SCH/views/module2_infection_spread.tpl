% rebase('layout.tpl', title=title, year=year)

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
</head>

<h2>{{ title }}.</h2>
<h3>{{ message }}</h3>

<div class="infection-spread">
    <div class="container">
        <div class="controls">
            <form method="GET" action="/infection_spread">
                <label for="field-size">the field size (odd):</label>
                <br>
                <span class="range-limits">3</span>
                <input type="range" id="field-size" name="size" min="3" max="15" value="{{initial_size}}" step="2" onchange="this.form.submit()">
                <span class="range-limits">15</span>
                <br>
                <div class="field-value-wrapper">
                    <span id="field-value">{{initial_size}}</span>
                </div>
                <br>
                    <button type="submit" class="buttons" name="action" value="start">Start</button>
                    <button type="submit" class="buttons" name="saveToJson" value="start">Save to JSON</button>
            </form>
        </div>
        <div class="grid-wrapper">
            <div class="grid-container" id="grid">
                % for i in range(initial_size):
                    <div class="grid-row">
                        % for j in range(initial_size):
                            <div class="grid-cell {{ 'infected' if grid[i][j] == 1 else 'immune' if grid[i][j] == 2 else '' }}"></div>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>

<script>
    const grid = document.getElementById('grid');
    const fieldValue = document.getElementById('field-value');
    const source = new EventSource('/infection_spread/stream?size={{initial_size}}');

    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const newGrid = data.grid;
        const newSize = data.size;

        fieldValue.textContent = newSize;

        grid.innerHTML = '';
        grid.style.width = `${newSize * 32}px`;
        grid.style.height = `${newSize * 32}px`;

        for (let i = 0; i < newSize; i++) {
            const row = document.createElement('div');
            row.className = 'grid-row';
            for (let j = 0; j < newSize; j++) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                if (newGrid[i][j] === 1) {
                    cell.classList.add('infected');
                } else if (newGrid[i][j] === 2) {
                    cell.classList.add('immune');
                }
                row.appendChild(cell);
            }
            grid.appendChild(row);
        }
    };
</script>