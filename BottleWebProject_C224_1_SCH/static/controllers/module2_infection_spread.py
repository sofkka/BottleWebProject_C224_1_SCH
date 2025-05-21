import os
import random
import copy
import json
from datetime import datetime

def initialize_grid(size):
    """
        Функция initialize_grid
        Используется для инициализации сетки размером n x n, где центральная ячейка заражена, 
        а остальные ячейки здоровы.

        Принимаемые поля (агрументы): 
        size - размер сетки, которая будет создана, имеет форму n x n.

        Возвращаемые поля:
        grid - двумерный список, представляющий сетку, в котором каждый элемент внешнего
        списка представляет строку сетки (всего n), которая состоит из n ячеек.
    """

    # Создание двумерной сетки размером n * n, где каждая ячейка представлена
    # словарём с ключами состояния клетки и счётчика времени.
    grid = [[{'state': 'H', 'timer': 0} for _ in range(size)] for _ in range(size)]

    # Вычисляется индекс центральной ячейки и устанавливается в состояние 'I' (заражённая) с таймером 0.
    center = size // 2
    grid[center][center] = {'state': 'I', 'timer': 0}

    # Возвращается инициализированная сетка.
    return grid


def grid_to_json(grid):
    """
        Функция grid_to_json
        Преобразует сетку в формат, совместимый с JSON, для передачи данных клиенту.

        Принимаемые поля (аргументы):
        grid - двумерный список, представляющий сетку.

        Возвращаемые поля:
        двумерный список, где каждая ячейка представлена словарём
        с ключами 'state' и 'timer', готовый для сериализации в JSON.
    """
    return [[{'state': cell['state'], 'timer': cell['timer']} for cell in row] for row in grid]


def is_all_healthy(grid, size):
    """
        Функция is_all_healthy
        Проверяет, являются ли все ячейки сетки здоровыми (в состоянии 'H').

        Принимаемые поля (аргументы): 
        grid - двумерный список, представляющий сетку, где каждая ячейка — словарь
        с ключами 'state' и 'timer'.
        size - размер сетки (n * n).

        Возвращаемые поля:
        True, если все ячейки здоровы, False в противном случае.
    """
    # Перебираются все строки сетки
    for i in range(size):
        # Перебираются все столбцы 
        for j in range(size):
            # Проверяется состояние текущей ячейки. Если оно не 'H' (здоровое),
            # возвращается False, указывая, что не все ячейки здоровы.
            if grid[i][j]['state'] != 'H':
                return False
    # Если все ячейки здоровы, возвращается True.
    return True


def simulate_step(grid, size):
    """
        Функция simulate_step
        Выполняет один шаг симуляции распространения инфекции, обновляя состояние сетки.

        Принимаемые поля (аргументы): 
        grid - двумерный список, представляющий текущую сетку, где каждая ячейка — словарь
        с ключами 'state' и 'timer'.
        size - размер сетки (n x n).

        Возвращаемые поля:
        new_grid - обновлённая сетка после одного шага симуляции, где ячейки могут изменить
        состояние и таймеры.
    """
    # Направления смещения для проверки соседних ячеек (вверх, вниз, влево, вправо).
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Копия исходной сетки, чтобы изменения не затрагивали оригинал.
    new_grid = copy.deepcopy(grid)

    # Перебираются все строки сетки
    for i in range(size):
        # Перебираются все столбцы сетки
        for j in range(size):
            # Проверяется, является ли текущая ячейка заражённой ('I').
            if grid[i][j]['state'] == 'I':
                # Если таймер заражённой ячейки достиг или превысил 6 шагов,
                # ячейка переходит в состояние 'R' и таймер сбрасывается.
                if grid[i][j]['timer'] >= 6:
                    new_grid[i][j]['state'] = 'R'
                    new_grid[i][j]['timer'] = 0
                else:
                    # Таймер заражённой ячейки увеличивается на 1.
                    new_grid[i][j]['timer'] += 1

                    # Перебираются все соседние ячейки, определённые направлениями.
                    for di, dj in directions:
                        # Вычисляются координаты соседней ячейки (ni, nj).
                        ni, nj = i + di, j + dj

                        # Проверяется, находится ли соседняя ячейка в пределах сетки
                        # и является ли она здоровой.
                        if 0 <= ni < size and 0 <= nj < size and grid[ni][nj]['state'] == 'H':
                            # С вероятностью 50% соседняя ячейка заражается, и её таймер сбрасывается.
                            if random.random() < 0.5:
                                new_grid[ni][nj]['state'] = 'I'
                                new_grid[ni][nj]['timer'] = 0

            # Проверяется, является ли текущая ячейка невосприимчивой.
            elif grid[i][j]['state'] == 'R':
                # Если таймер невосприимчивой ячейки достиг или превысил 3 шага,
                # ячейка переходит в состояние 'H' и таймер сбрасывается.
                if grid[i][j]['timer'] >= 3:
                    new_grid[i][j]['state'] = 'H'
                    new_grid[i][j]['timer'] = 0

                else:
                    # Таймер невосприимчивой ячейки увеличивается на 1.
                    new_grid[i][j]['timer'] += 1

    # Возвращается обновлённая сетка после одного шага симуляции.
    return new_grid

def simulate_all_steps(initial_grid, size, max_steps=100):
    """
        Функция simulate_all_steps
        Генерирует все шаги симуляции распространения инфекции до достижения максимального
        количества шагов или состояния, когда все ячейки здоровы.

        Принимаемые поля (аргументы):
        initial_grid - начальная двумерная сетка, где каждый элемент - список ячеек, каждая
        ячейка - словарь с ключами 'state' (строка: 'H', 'I', 'R') и 'timer' (целое число).
        size - размер сетки (целое число), определяющий количество строк и столбцов.
        max_steps - максимальное количество шагов симуляции (целое число, по умолчанию 100).

        Возвращаемые поля:
        steps - список всех шагов симуляции, каждый элемент - двумерный список ячеек
        (копия сетки на каждом шаге).
        final_grid - конечная сетка после выполнения всех шагов или достижения состояния
        всех здоровых ячеек.
        all_healthy - булево значение (True, если все ячейки в конечной сетке имеют 'state' 'H',
        иначе False).
    """

    # Создаётся список steps, содержащий исходную сетку как первый элемент.
    steps = [initial_grid]

    # Текущая сетка инициализируется копией исходной сетки.
    current_grid = initial_grid

    # Выполняется цикл до max_steps раз.
    for _ in range(max_steps):
        # Выполняется один шаг симуляции, обновляя текущую сетку.
        current_grid = simulate_step(current_grid, size)

        # Обновлённая сетка добавляется в список шагов.
        steps.append(current_grid)

        # Проверяется, являются ли все ячейки здоровыми. Если да, цикл прерывается.
        if is_all_healthy(current_grid, size):
            break
    # Проверяется состояние всех ячеек в конечной сетке и сохраняется результат
    # в переменную all_healthy (True, если все ячейки здоровы, иначе False).
    all_healthy = is_all_healthy(current_grid, size)

    # Кортеж из списка всех шагов, конечной сетки и флага all_healthy.
    return steps, current_grid, all_healthy


def save_to_json(grid, size, step_count, elapsed_steps):
    """
        Функция save_to_json
        Сохраняет текущее состояние симуляции в JSON-файл с историей всех запусков,
        организованной по датам. Каждая запись содержит метаданные и состояние сетки.

        Принимаемые поля (аргументы):
        grid - текущая двумерная сетка, где каждый элемент - список ячеек, каждая
        ячейка - словарь с ключами 'state' (строка: 'H', 'I', 'R') и 'timer' (целое число).
        size - размер сетки (целое число), определяющий количество строк и столбцов.
        step_count - текущий шаг симуляции (целое число).
        elapsed_steps - общее количество прошедших шагов (целое число).

        Возвращаемые поля:
        Кортеж из двух элементов:
        - success - булево значение (True, если сохранение прошло успешно, иначе False)
        - message - строка с описанием результата операции или ошибки

        Формат сохраняемых данных можно посмотреть в файле jsons\result_module2.json
    """

    json_path = 'jsons/result_module2.json'
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Подсчет клеток и формирование компактного представления сетки
    healthy = infected = resistant = 0
    grid_state_compact = []
    for row in grid:
        row_str = ""
        for cell in row:
            state = cell['state']
            row_str += state
            row_str += " "
            if state == 'H':
                healthy += 1
            elif state == 'I':
                infected += 1
            elif state == 'R':
                resistant += 1
        grid_state_compact.append(row_str)
    
    # Формирование данных для сохранения
    save_data = {
        'time': current_time,
        'input_parameters': {
            'grid_size': size,
        },
        'simulation_results': {
            'simulation_step': step_count,
            'healthy_cells': healthy,
            'infected_cells': infected,
            'resistant_cells': resistant,
            'grid_state': grid_state_compact
        },
        'status': 'Simulation in progress' if infected > 0 else 'Infection eradicated'
    }
    
    # Создание директории при необходимости
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    # Загрузка существующих данных
    json_data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        except (json.JSONDecodeError, IOError):
            json_data = {}
    
    # Добавление новой записи
    if current_date not in json_data:
        json_data[current_date] = []
    json_data[current_date].insert(0, save_data)
    
    # Сохранение обновленных данных
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        return True, 'Saved successfully'
    except IOError as e:
        return False, f'Failed to save to JSON: {str(e)}'

