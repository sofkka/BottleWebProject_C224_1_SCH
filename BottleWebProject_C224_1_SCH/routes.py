"""
Routes and views for the bottle application.
"""

import json
from bottle import request, response, route, view, static_file
from static.controllers.module2_infection_spread import grid_to_json, simulate_all_steps, initialize_grid, save_grid_state
from datetime import datetime

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
    """Renders the module3_cells_colonies page."""
    return dict(
        title='Colonies of living cells',
        message='A simulation of growth and interaction in colonies of living cells.',
        year=datetime.now().year
    )
