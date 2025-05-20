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
    # Извлекается параметр 'size' из GET-запроса, задающий размер сетки. Если параметр отсутствует - 9
    size = request.GET.get('size', '9')

    # Извлекается параметр 'continue_from', содержащий JSON-представление сетки для продолжения симуляции.
    # Если параметр отсутствует - None.
    continue_from = request.GET.get('continue_from')

    # Проверяется параметр 'save', определяющий, нужно ли сохранить состояние сетки в JSON.
    # Значение 'true' в запросе преобразуется в булево True, иначе False.
    save = request.GET.get('save', 'false') == 'true'

    # Извлекается параметр 'step', указывающий текущий шаг симуляции. Если параметр отсутствует, используется 0.
    step = int(request.GET.get('step', '0'))

    # Проверяется корректность параметра size и преобразуется в целое число.
    try:
        # Параметр size преобразуется в целое число.
        size = int(size)

        # Если size является чётным числом или выходит за допустимый диапазон (3–15) - size = 9.
        if size % 2 == 0 or size < 3 or size > 15:
            size = 9

    # Обработка исключения ValueError, возникающее при некорректном формате size.
    except ValueError:
        size = 9

    # Обрабатывается запрос на сохранение состояния сетки в JSON.
    if save:
        return "The result is saved in JSON"

    # Загружается сетка для симуляции: либо продолжается из переданного состояния, либо создаётся новая.
    if continue_from:
        # Проверяется возможность продолжения симуляции из переданного состояния.
        try:
            # Параметр continue_from декодируется из JSON в двумерный список (сетку).
            continue_grid = json.loads(continue_from)

            # Создаётся новая сетка с переданными параметрами
            grid = [[{'state': cell['state'], 'timer': cell['timer']} for cell in row] for row in continue_grid]

        # Обработка исключения JSONDecodeError, возникающего при некорректном формате continue_from.
        except json.JSONDecodeError:
            # Если декодирование не удалось, создаётся новая сетка размером size.
            grid = initialize_grid(size)
    else:
        # Если continue_from отсутствует, создаётся новая сетка размером size.
        grid = initialize_grid(size)

    # Подготовка данных для передачи в шаблон module2_infection_spread.tpl.

    # Запускается симуляция распространения инфекции.
    simulation_steps, final_grid, all_healthy = simulate_all_steps(grid, size)

    # Преобразуется каждый шаг симуляции в JSON-совместимый формат.
    simulation_steps_json = [grid_to_json(step) for step in simulation_steps]

    # Преобразуется конечная сетка в JSON-совместимый формат.
    final_grid_json = grid_to_json(final_grid)

    # Словарь для передачи.
    return dict(
        title='The model of ringworm infection spread',
        message='A simulation model exploring the spread of ringworm infection.',
        year=datetime.now().year,
        # Передаётся начальный размер сетки.
        initial_size=size,

        # Передаётся список шагов симуляции в JSON-формате для отображения в JavaScript.
        simulation_steps_json=simulation_steps_json,

        # Передаётся конечная сетка в JSON-формате для продолжения или отображения.
        final_grid_json=final_grid_json,

        # Передаётся флаг, указывающий, являются ли все ячейки здоровыми.
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
