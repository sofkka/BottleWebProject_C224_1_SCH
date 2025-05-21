"""
Routes and views for the bottle application.
"""
from bottle import route, request, response, template, view, static_file
from static.controllers.module3_cells_colonies import GameOfLife
from datetime import datetime, timedelta
import json
import os
import uuid

import json
from bottle import request, response, route, view, static_file
from static.controllers.module2_infection_spread import grid_to_json, simulate_all_steps, initialize_grid, save_to_json
from datetime import datetime

from static.controllers.module1_wolf_island import wolf_island_controller
from static.controllers.module2_infection_spread import grid_to_json, simulate_all_steps, initialize_grid, save_to_json
import random


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

@route('/wolf_island', method=['GET'])
@view('module1_wolf_island')
def wolf_island():
    action = request.query.get('action', '')
    N = request.query.get('N', '')
    M = request.query.get('M', '')
    rabbits = request.query.get('rabbits', '')
    wolves = request.query.get('wolves', '')
    she_wolves = request.query.get('she_wolves', '')
    steps = request.query.get('steps', '')
    return wolf_island_controller(action, N, M, rabbits, wolves, she_wolves, steps)

@route('/wolf_island', method=['GET'])
@view('module1_wolf_island')
def wolf_island():
    action = request.query.get('action', '')
    N = request.query.get('N', '')
    M = request.query.get('M', '')
    rabbits = request.query.get('rabbits', '')
    wolves = request.query.get('wolves', '')
    she_wolves = request.query.get('she_wolves', '')
    steps = request.query.get('steps', '')
    return wolf_island_controller(action, N, M, rabbits, wolves, she_wolves, steps)

@route('/infection_spread')
@view('module2_infection_spread')
def module2_infection_spread():
    size = request.GET.get('size', '9')

    continue_from = request.GET.get('continue_from')

    save = request.GET.get('save', 'false') == 'true'

    step = int(request.GET.get('step', '0'))

    try:
        size = int(size)

        if size % 2 == 0 or size < 3 or size > 15:
            size = 9

    except ValueError:
        size = 9

    if save:
        try:
            grid = json.loads(continue_from)
            success, message = save_to_json(grid, size, step, step)
            return json.dumps({'success': success, 'message': message})
        except Exception as e:
            return json.dumps({'success': False, 'message': str(e)})

    if continue_from:
        try:
            continue_grid = json.loads(continue_from)

        except json.JSONDecodeError:
            grid = initialize_grid(size)
    else:
        grid = initialize_grid(size)


    simulation_steps, final_grid, all_healthy = simulate_all_steps(grid, size)

    simulation_steps_json = [grid_to_json(step) for step in simulation_steps]

    final_grid_json = grid_to_json(final_grid)

    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        initial_size=size,

        simulation_steps_json=simulation_steps_json,

        final_grid_json=final_grid_json,

        all_healthy=all_healthy
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
