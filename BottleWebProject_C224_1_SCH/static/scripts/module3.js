let intervalId = null;// For controlling the auto-play interval

// Function to update the visual grid display based on current cell states

function updateGridDisplay(grid) {
    const table = document.getElementById('gridTable');
    table.innerHTML = ''; // Clear existing grid
    for (let i = 0; i < grid.length; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < grid[0].length; j++) {
            const cell = document.createElement('td');
            cell.className = grid[i][j] ? 'alive' : ''; // Add 'alive' class if cell is alive
            cell.dataset.x = i;
            cell.dataset.y = j;
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
    adjustCellSizes(); // Adjust cell size dynamically
}

function updateGrid() {
    const width = parseInt(document.getElementById('fieldWidth').value);
    const height = parseInt(document.getElementById('fieldHeight').value);

    if (width < 3 || height < 3 || width > 50 || height > 50) {
        alert('Please enter values between 3 and 50.');
        return;
    }

    const table = document.getElementById('gridTable');
    table.innerHTML = '';

    for (let i = 0; i < height; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < width; j++) {
            const cell = document.createElement('td');
            cell.className = '';
            cell.dataset.x = i;
            cell.dataset.y = j;
            row.appendChild(cell);
        }
        table.appendChild(row);
    }

    adjustCellSizes();
}
// Function to adjust cell sizes based on container size
function adjustCellSizes() {
    const gridWrapper = document.querySelector('.grid-wrapper');
    const settings = document.querySelector('.settings');
    const table = document.getElementById('gridTable');
    const width = parseInt(document.getElementById('fieldWidth').value);
    const height = parseInt(document.getElementById('fieldHeight').value);

    const containerWidth = document.querySelector('.cells-container').offsetWidth;
    const settingsWidth = settings.offsetWidth;
    const availableWidth = containerWidth - settingsWidth - 60; /* Increased padding margin */
    const availableHeight = window.innerHeight - 200; /* Account for header/footer */

    /* Calculate cell size to fit within available space, with a larger max */
    const cellSize = Math.min(
        Math.floor(availableWidth / width),
        Math.floor(availableHeight / height),
        80 /* max cell size for larger cells */
    );

    const cells = table.querySelectorAll('td');
    cells.forEach(cell => {
        cell.style.width = `${cellSize}px`;
        cell.style.height = `${cellSize}px`;
        /* aspectRatio already set in CSS */
    });

    /* Set table dimensions */
    table.style.width = `${cellSize * width}px`;
    table.style.height = `${cellSize * height}px`;

    /* Ensure grid-wrapper doesn't overflow */
    gridWrapper.style.maxWidth = `${cellSize * width + 40}px`;
}

/* Rest of the JavaScript unchanged */
function sendRequest(action, data = {}) {
    const width = document.getElementById('fieldWidth').value;
    const height = document.getElementById('fieldHeight').value;
    const a = document.getElementById('neighborsReproduce').value;
    const b = document.getElementById('fewerNeighbors').value;
    const c = document.getElementById('moreNeighbors').value;

    data = {
        ...data,
        action: action,
        width: width,
        height: height,
        a: a,
        b: b,
        c: c
    };

    fetch('/update_grid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.grid) {
                updateGridDisplay(data.grid);
            }
            if (action === 'start' && !intervalId) {
                intervalId = setInterval(() => {
                    sendRequest('tick');
                }, 2000);
            } else if (action === 'pause' || action === 'reset') {
                clearInterval(intervalId);
                intervalId = null;
            }
            if (action === 'save_json') {
                const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'grid.json';
                a.click();
                window.URL.revokeObjectURL(url);
            }
        });
}
// Event handlers for control buttons
document.getElementById('startBtn').addEventListener('click', () => {
    sendRequest('start');
});

document.getElementById('pauseBtn').addEventListener('click', () => {
    sendRequest('pause');
});

document.getElementById('resetBtn').addEventListener('click', () => {
    sendRequest('reset');
});

document.getElementById('saveJsonBtn').addEventListener('click', () => {
    sendRequest('save_json').then(data => {
        if (data.download_url) {
            const a = document.createElement('a');
            a.href = data.download_url;
            a.download = 'simulation_records.json';
            a.click();
        }
    });
});

document.getElementById('gridTable').addEventListener('click', (e) => {
    if (e.target.tagName === 'TD') {
        const x = e.target.dataset.x;
        const y = e.target.dataset.y;
        sendRequest('toggle_cell', { x: x, y: y });
    }
});

document.getElementById('fieldWidth').addEventListener('input', function () {
    document.getElementById('fieldHeight').value = this.value;
    updateGrid();
    sendRequest('reset');
});

document.getElementById('fieldHeight').addEventListener('input', function () {
    document.getElementById('fieldWidth').value = this.value;
    updateGrid();
    sendRequest('reset');
});

window.addEventListener('resize', adjustCellSizes);

// Initial grid setup
updateGrid();