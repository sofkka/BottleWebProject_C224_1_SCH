% rebase('layout.tpl', title=title, year=year)

<h2 class="lead">{{ title }}.</h2>
<h3 class="lead">{{ message }}</h3>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
</head>
<div class="cells-container">
    <div class="grid-wrapper">
        <table class="grid-table" id="gridTable">
            % width = get('width', 3)  
            % height = get('height', 3)  
            % initial_cells = get('initial_cells', [(0,0), (0,1), (1,1), (2,0)]) 
            % for i in range(height):
                <tr>
                % for j in range(width):
                    % is_alive = (i, j) in initial_cells
                    <td class="{{ 'alive' if is_alive else '' }}"></td>
                % end
                </tr>
            % end
        </table>
    </div>
    <div class="settings">
        <p class="lead">Choose:</p>
        <p class="lead">
            the field size: 
            <input type="number" class="parameters" name="field_width" id="fieldWidth" value="{{ width }}" min="1" max="50" style="width: 60px;">
            X
            <input type="number" class="parameters" name="field_height" id="fieldHeight" value="{{ height }}" min="1" max="50" style="width: 60px;">
            <button type="submit" class="buttons" onclick="updateGrid()">Update Grid</button>
        </p>
        <p class="lead">
            Parameter a the number of neighbors to reproduce (1-8): 
            <select class="parameters" name="neighbors_reproduce" id="neighborsReproduce">
                % for i in range(1, 9):
                    <option value="{{ i }}">{{ i }}</option>
                % end
            </select>
        </p>
        <p class="lead">
            Parameter b fewer neighbors (2-8): 
            <select class="parameters" name="fewer_neighbors" id="fewerNeighbors">
                % for i in range(2, 9):
                    <option value="{{ i }}">{{ i }}</option>
                % end
            </select>
        </p>
        <p class="lead">
            Parameter c more neighbors (1-7): 
            <select class="parameters" name="more_neighbors" id="moreNeighbors">
                % for i in range(1, 8):
                    <option value="{{ i }}">{{ i }}</option>
                % end
            </select>
        </p>
    </div>
</div>
<button type="submit" class="buttons" name="action" value="start" id="startBtn">Start</button>
<button type="submit" class="buttons" name="action" value="pause" id="pauseBtn">Pause</button>
<button type="submit" class="buttons" name="action" value="reset" id="resetBtn">Reset</button>


<script>
    document.getElementById('fieldWidth').addEventListener('input', function() {
        document.getElementById('fieldHeight').value = this.value;
    });

    document.getElementById('fieldHeight').addEventListener('input', function() {
        document.getElementById('fieldWidth').value = this.value;
    });

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
    }
</script>