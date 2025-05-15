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

        <div class="container">
            <div class="left-panel">
                <h3>Simulation Parameters</h3>
                <div class="input-row">
                    <label>Island Width (N, 5-10):</label>
                    <input type="text">
                </div>
                <div class="input-row">
                    <label>Island Height (M, 5-10):</label>
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
                <div class="action-buttons"">
                    <button>Generate random values</button>
                </div>
                <div class="action-buttons"">
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
            </div>
            <div class="right-panel">
                <div class="grid"></div>
            </div>
        </div>
    </div>
</body>
</html>