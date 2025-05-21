"""
Routes and views for the bottle application.
"""
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

@route('/infection_spread')
@view('module2_infection_spread')
def module2_infection_spread():
    # ����������� �������� 'size' �� GET-�������, �������� ������ �����. ���� �������� ����������� - 9
    size = request.GET.get('size', '9')

    # ����������� �������� 'continue_from', ���������� JSON-������������� ����� ��� ����������� ���������.
    # ���� �������� ����������� - None.
    continue_from = request.GET.get('continue_from')

    # ����������� �������� 'save', ������������, ����� �� ��������� ��������� ����� � JSON.
    # �������� 'true' � ������� ������������� � ������ True, ����� False.
    save = request.GET.get('save', 'false') == 'true'

    # ����������� �������� 'step', ����������� ������� ��� ���������. ���� �������� �����������, ������������ 0.
    step = int(request.GET.get('step', '0'))

    # ����������� ������������ ��������� size � ������������� � ����� �����.
    try:
        # �������� size ������������� � ����� �����.
        size = int(size)

        # ���� size �������� ������ ������ ��� ������� �� ���������� �������� (3�15) - size = 9.
        if size % 2 == 0 or size < 3 or size > 15:
            size = 9

    # ��������� ���������� ValueError, ����������� ��� ������������ ������� size.
    except ValueError:
        size = 9

    # �������������� ������ �� ���������� ��������� ����� � JSON.
    if save:
        return "The result is saved in JSON"

    # ����������� ����� ��� ���������: ���� ������������ �� ����������� ���������, ���� �������� �����.
    if continue_from:
        # ����������� ����������� ����������� ��������� �� ����������� ���������.
        try:
            # �������� continue_from ������������ �� JSON � ��������� ������ (�����).
            continue_grid = json.loads(continue_from)

            # �������� ����� ����� � ����������� �����������
            grid = [[{'state': cell['state'], 'timer': cell['timer']} for cell in row] for row in continue_grid]

        # ��������� ���������� JSONDecodeError, ������������ ��� ������������ ������� continue_from.
        except json.JSONDecodeError:
            # ���� ������������� �� �������, �������� ����� ����� �������� size.
            grid = initialize_grid(size)
    else:
        # ���� continue_from �����������, �������� ����� ����� �������� size.
        grid = initialize_grid(size)

    # ���������� ������ ��� �������� � ������ module2_infection_spread.tpl.

    # ����������� ��������� ��������������� ��������.
    simulation_steps, final_grid, all_healthy = simulate_all_steps(grid, size)

    # ������������� ������ ��� ��������� � JSON-����������� ������.
    simulation_steps_json = [grid_to_json(step) for step in simulation_steps]

    # ������������� �������� ����� � JSON-����������� ������.
    final_grid_json = grid_to_json(final_grid)

    # ������� ��� ��������.
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        # ��������� ��������� ������ �����.
        initial_size=size,

        # ��������� ������ ����� ��������� � JSON-������� ��� ����������� � JavaScript.
        simulation_steps_json=simulation_steps_json,

        # ��������� �������� ����� � JSON-������� ��� ����������� ��� �����������.
        final_grid_json=final_grid_json,

        # ��������� ����, �����������, �������� �� ��� ������ ���������.
        all_healthy=all_healthy
    )



@route('/cells_colonies')
@view('module3_cells_colonies')
def module3_cells_colonies():
    """Render the 'cells_colonies' page."""
    global game
    game = GameOfLife(3, 3)
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year
    )