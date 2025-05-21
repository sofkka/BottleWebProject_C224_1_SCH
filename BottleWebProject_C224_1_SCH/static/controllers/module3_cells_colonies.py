

import random
import json
import os
import logging
from bottle import Bottle, route, post, request, response, static_file
from datetime import datetime
import uuid

app = Bottle()

logging.basicConfig(level=logging.DEBUG, filename='server.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class GameOfLife:
    def __init__(self, width, height, a=2, b=3, c=3):
        self.width = width
        self.height = height
        self.a = a
        self.b = b
        self.c = c
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.initial_cells = []
        self.initial_cell_count = 0
        self.current_cell_count = 0
        self.initialize_grid()
        self.update_cell_count()

    def initialize_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                if random.random() < 0.2:
                    self.grid[i][j] = 1
                    self.initial_cells.append([i, j])
        self.initial_cell_count = len(self.initial_cells)

    def count_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx = (x + i) % self.height
                ny = (y + j) % self.width
                count += self.grid[nx][ny]
        return count

    def next_generation(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    new_grid[i][j] = 1 if self.a <= neighbors <= self.b else 0
                else:
                    new_grid[i][j] = 1 if neighbors == self.c else 0
        self.grid = new_grid
        self.update_cell_count()

    def toggle_cell(self, x, y):
        self.grid[int(x)][int(y)] = 1 if self.grid[int(x)][int(y)] == 0 else 0
        self.update_cell_count()

    def reset(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.initial_cells = []
        self.initialize_grid()
        self.update_cell_count()

    def update_cell_count(self):
        self.current_cell_count = sum(row.count(1) for row in self.grid)

    def to_json(self):
        return {
            'width': self.width,
            'height': self.height,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'grid': self.grid,
            'initial_cells': self.initial_cells,
            'initial_cell_count': self.initial_cell_count
        }

game = None
start_time = None
JSON_DIR = os.path.join(os.path.dirname(__file__), 'jsons')
os.makedirs(JSON_DIR, exist_ok=True)

@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')

@post('/update_grid')
def update_grid():
    global game, start_time
    action = request.forms.get('action')
    width = int(request.forms.get('width', 3))
    height = int(request.forms.get('height', 3))
    a = int(request.forms.get('a', 2))
    b = int(request.forms.get('b', 3))
    c = int(request.forms.get('c', 3))

    logging.debug(f"Action: {action}, Width: {width}, Height: {height}, a: {a}, b: {b}, c: {c}")

    if width < 1 or height < 1 or width > 50 or height > 50:
        response.status = 400
        logging.error("Invalid dimensions")
        return {'error': 'Invalid dimensions'}
    if a < 1 or b < 2 or c < 1 or a > 8 or b > 8 or c > 8:
        response.status = 400
        logging.error("Invalid parameters a, b, or c")
        return {'error': 'Invalid parameters a, b, or c'}

    if (game is None or game.width != width or game.height != height or
        game.a != a or game.b != b or game.c != c):
        game = GameOfLife(width, height, a, b, c)
        logging.debug("New GameOfLife instance created")

    if action == 'start':
        start_time = datetime.now()
        logging.debug("Simulation started")
    elif action == 'tick':
        game.next_generation()
        logging.debug("Next generation computed")
    elif action in ['pause', 'reset']:
        if start_time:
            save_simulation_record({
                'record_id': str(uuid.uuid4()),
                'width': game.width,
                'height': game.height,
                'a': game.a,
                'b': game.b,
                'c': game.c,
                'initial_cell_count': game.initial_cell_count,
                'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            start_time = None
            logging.debug(f"Simulation saved on {action}")
        if action == 'reset':
            game.reset()
            logging.debug("Game reset")
    elif action == 'toggle_cell':
        x = request.forms.get('x')
        y = request.forms.get('y')
        if x is not None and y is not None:
            try:
                x, y = int(x), int(y)
                if 0 <= x < height and 0 <= y < width:
                    game.toggle_cell(x, y)
                    logging.debug(f"Cell toggled at ({x}, {y})")
                else:
                    response.status = 400
                    logging.error("Invalid cell coordinates")
                    return {'error': 'Invalid cell coordinates'}
            except ValueError:
                response.status = 400
                logging.error("Invalid cell coordinates")
                return {'error': 'Invalid cell coordinates'}

    return {'grid': game.grid}

@post('/save_json_to_file')
def save_json_to_file():
    try:
        data = {
            'record_id': str(uuid.uuid4()),
            'width': int(request.forms.get('width')),
            'height': int(request.forms.get('height')),
            'a': int(request.forms.get('a')),
            'b': int(request.forms.get('b')),
            'c': int(request.forms.get('c')),
            'initial_cell_count': 0,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        grid = json.loads(request.forms.get('grid'))
        logging.debug(f"Received save_json_to_file request: {data}, grid: {grid}")
        initial_cell_count = sum(row.count(1) for row in grid)
        data['initial_cell_count'] = initial_cell_count

        json_file_path = os.path.join(JSON_DIR, 'module3.json')
        records = []
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                try:
                    records = json.load(f)
                    if not isinstance(records, list):
                        records = [records]
                except json.JSONDecodeError:
                    logging.error("Invalid JSON in module3.json, starting fresh")
                    records = []
        records.append(data)
        with open(json_file_path, 'w') as f:
            json.dump(records, f, indent=4, separators=(',', ': '))
        logging.debug(f"Saved record to {json_file_path}")

        return {'success': True}
    except Exception as e:
        logging.error(f"Error in save_json_to_file: {str(e)}")
        response.status = 500
        return {'success': False, 'error': str(e)}

def save_simulation_record(record):
    json_file_path = os.path.join(JSON_DIR, 'module3.json')
    records = []
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            try:
                records = json.load(f)
                if not isinstance(records, list):
                    records = [records]
            except json.JSONDecodeError:
                logging.error("Invalid JSON in module3.json, starting fresh")
                records = []
    record['datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    records.append(record)
    with open(json_file_path, 'w') as f:
        json.dump(records, f, indent=4, separators=(',', ': '))
    logging.debug(f"Saved simulation record to {json_file_path}")

def reset_game_state():
    global game, start_time
    game = None
    start_time = None

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)