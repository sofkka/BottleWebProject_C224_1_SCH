from bottle import route, request, response, template, view, static_file
from static.controllers.module3_cells_colonies import GameOfLife
from datetime import datetime, timedelta
import json
import os
import uuid
from static.controllers.module1_wolf_island import wolf_island_controller
import random

@route('/')
@route('/home')
@view('index')
def home():
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
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

@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_colonies():
    global game
    game = GameOfLife(3, 3)
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year
    )