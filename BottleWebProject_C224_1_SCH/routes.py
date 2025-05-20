"""
Routes and views for the bottle application.
"""
from bottle import route, request, response, template, view, static_file
from static.controllers.module3_cells_colonies import GameOfLife
from datetime import datetime, timedelta
import json
import os
import uuid

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About authors',
        year=datetime.now().year
    )

@route('/wolf_island')
@view('module1_wolf_island')
def module1_wolf_island():
    """Renders the module1_wolf_island page."""
    return dict(
        title='The model of death and reproduction',
        message='A simulation model exploring death and reproduction dynamics on Wolf Island.',
        year=datetime.now().year
    )

@route('/infection_spread')
@view('module2_infection_spread')
def module2_infection_spread():
    # Get 'size' from GET request, default to '9'
    size = request.GET.get('size', '9')
    try:
        # Convert size to integer and validate: must be odd, between 3 and 15
        size = int(size)
        if size % 2 == 0 or size < 3 or size > 15:
            size = 3
    except ValueError:
        size = 3

    # Create a grid of size x size filled with 0 (healthy cells)
    grid = [[0 for _ in range(size)] for _ in range(size)]

    # Return data for the template
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        initial_size=size,
        grid=grid
    )


# Store the current game state and simulation timing
game = None  # Instance of the GameOfLife class representing the current game
start_time = None  # Timestamp when the simulation was started
simulation_records_file = 'downloads/simulation_records.json'  # Path to the JSON file for saving simulation records

@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_colonies():
    """Render the 'cells_colonies' page."""
    global game
    # Initialize a new game with 3x3 grid upon page load
    game = GameOfLife(3, 3)
    return dict(
        title='Colonies of living cells',  # Page title
        message='A simulation of growth and interaction in colonies of living cells.',  # Description message
        year=datetime.now().year  # Current year
    )

@route('/update_grid', method='POST')
def update_grid():
    """Handle grid updates and user actions for the Game of Life simulation."""
    global game, start_time
    
    # Get form data
    action = request.forms.get('action')
    width = int(request.forms.get('width', 3))
    height = int(request.forms.get('height', 3))
    a = int(request.forms.get('a', 2))
    b = int(request.forms.get('b', 3))
    c = int(request.forms.get('c', 3))
    
    # Validate input dimensions
    if width < 1 or height < 1 or width > 50 or height > 50:
        response.status = 400
        return {'error': 'Invalid dimensions'}
    
    # Validate parameters a, b, c
    if a < 1 or b < 2 or c < 1 or a > 8 or b > 8 or c > 8:
        response.status = 400
        return {'error': 'Invalid parameters a, b, or c'}
    
    # If grid size or rules changed, create a new game instance
    if (game is None or
        game.width != width or
        game.height != height or
        game.a != a or
        game.b != b or
        game.c != c):
        game = GameOfLife(width, height, a, b, c)
    
    # Handle different user actions
    if action == 'start':
        # Start timing the simulation
        start_time = datetime.now()
    elif action == 'tick':
        # Advance the game by one generation
        game.next_generation()
    elif action == 'pause' or action == 'reset':
        # Pause or reset the simulation
        if start_time:
            # Calculate total runtime in seconds
            runtime = (datetime.now() - start_time).total_seconds()
            # Save the current simulation record
            save_simulation_record({
                'record_id': str(uuid.uuid4()),  # Unique record ID
                'runtime_seconds': runtime,
                'width': game.width,
                'height': game.height,
                'a': game.a,
                'b': game.b,
                'c': game.c,
                'initial_cell_count': game.initial_cell_count,
                'initial_cells': game.initial_cells,
                'final_cell_count': game.current_cell_count
            })
            start_time = None  # Reset start time
        if action == 'reset':
            # Reset the game to a new random state
            game.reset()
    elif action == 'toggle_cell':
        # Toggle the state of a specific cell
        x = request.forms.get('x')
        y = request.forms.get('y')
        if x is not None and y is not None:
            try:
                x, y = int(x), int(y)
                # Check if coordinates are within bounds
                if 0 <= x < height and 0 <= y < width:
                    game.toggle_cell(x, y)
                else:
                    response.status = 400
                    return {'error': 'Invalid cell coordinates'}
            except ValueError:
                response.status = 400
                return {'error': 'Invalid cell coordinates'}
    elif action == 'save_json':
        # Save current simulation data to file
        if start_time:
            # Calculate total runtime
            runtime = (datetime.now() - start_time).total_seconds()
            # Save the record
            save_simulation_record({
                'record_id': str(uuid.uuid4()),
                'runtime_seconds': runtime,
                'width': game.width,
                'height': game.height,
                'a': game.a,
                'b': game.b,
                'c': game.c,
                'initial_cell_count': game.initial_cell_count,
                'initial_cells': game.initial_cells,
                'final_cell_count': game.current_cell_count
            })
            start_time = None
        # Return URL for downloading the records file
        return {'download_url': '/download_records'}
    
    # Return current grid state for rendering
    return {'grid': game.grid}

def save_simulation_record(record):
    """Append a simulation record to the JSON file."""
    os.makedirs('downloads', exist_ok=True)  # Ensure the directory exists
    records = []
    # Load existing records if the file exists
    if os.path.exists(simulation_records_file):
        try:
            with open(simulation_records_file, 'r') as f:
                records = json.load(f)
        except json.JSONDecodeError:
            # If JSON is invalid, start fresh
            records = []
    # Append the new record
    records.append(record)
    # Save all records back to the file
    with open(simulation_records_file, 'w') as f:
        json.dump(records, f, indent=2)

@route('/download_records')
def download_records():
    """Provide the JSON file containing all simulation records for download."""
    return static_file('simulation_records.json', root='downloads', download=True)