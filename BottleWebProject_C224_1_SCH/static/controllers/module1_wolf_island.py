# -*- coding: cp1251 -*-
import random
from datetime import datetime

# Глобальный словарь для хранения состояния симуляции
simulation_state = {}

# Класс для кроликов
class Rabbit:
    # Инициализация экземпляра кролика с координатами
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс для волков
class Wolf:
    # Инициализация экземпляра волка с координатами и очками
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 1.0  # Начальные очки волка

# Класс для волчиц
class SheWolf:
    # Инициализация экземпляра волчицы с координатами и очками
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 1.0  # Начальные очки волчицы

# Функция для нахождения соседних клеток в сетке
def get_neighbors(x, y, N, M):
    # Список для хранения координат соседних клеток
    neighbors = []
    # Перебор всех соседних клеток по оси X
    for dx in [-1, 0, 1]:
        # Перебор всех соседних клеток по оси Y
        for dy in [-1, 0, 1]:
            # Проверка, чтобы не включать текущую клетку
            if dx == 0 and dy == 0:
                # Пропуск текущей клетки
                continue
            # Вычисление координат соседней клетки
            new_x = x + dx
            new_y = y + dy
            # Проверка, что координаты находятся внутри сетки
            if 0 <= new_x < N and 0 <= new_y < M:
                # Добавление координат соседней клетки в список
                neighbors.append((new_x, new_y))
    # Возврат списка соседних клеток
    return neighbors

# Функция для инициализации симуляции
def initialize_simulation(N, M, num_rabbits, num_wolves, num_she_wolves):
    # Создание сетки размером N x M с пустыми списками в клетках
    grid = [[[] for i in range(M)] for i in range(N)]
    # Создание списков для хранения кроликов, волков и волчиц
    rabbits_list = []
    wolves_list = []
    she_wolves_list = []

    # Генерация списка всех возможных клеток на сетке
    available_cells = [(i, j) for i in range(N) for j in range(M)]
    # Перемешивание клеток для случайного размещения
    random.shuffle(available_cells)
    
    # Размещение кроликов на сетке
    for i in range(min(num_rabbits, len(available_cells))):
        # Извлечение случайных координат из списка доступных клеток (берет последний элемент)
        x, y = available_cells.pop()
        # Создание нового кролика с заданными координатами
        rabbit = Rabbit(x, y)
        # Добавление кролика в клетку на сетке
        grid[x][y].append(rabbit)
        # Добавление кролика в список кроликов
        rabbits_list.append(rabbit)

    # Размещение волков на сетке
    for i in range(min(num_wolves, len(available_cells))):
        # Извлечение случайных координат (берет последний элемент, индекс -1)
        x, y = available_cells.pop()
        # Создание нового волка
        wolf = Wolf(x, y)
        # Добавление волка в клетку
        grid[x][y].append(wolf)
        # Добавление волка в список волков
        wolves_list.append(wolf)

    # Размещение волчиц на сетке
    for i in range(min(num_she_wolves, len(available_cells))):
        # Извлечение случайных координат (берет последний элемент, индекс -1)
        x, y = available_cells.pop()
        # Создание новой волчицы
        she_wolf = SheWolf(x, y)
        # Добавление волчицы в клетку
        grid[x][y].append(she_wolf)
        # Добавление волчицы в список волчиц
        she_wolves_list.append(she_wolf)

    # Возврат сетки и списков животных
    return grid, rabbits_list, wolves_list, she_wolves_list

# Функция для очистки сетки после шага симуляции
def clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M):
    # Создание новых списков для актуальных животных
    new_rabbits_list = []
    new_wolves_list = []
    new_she_wolves_list = []

    # Проход по всем клеткам сетки
    for i in range(N):
        for j in range(M):
            # Проверка наличия животных в текущей клетке
            if len(grid[i][j]) > 0:
                # Формирование списка кроликов в клетке
                rabbits_in_cell = [e for e in grid[i][j] if isinstance(e, Rabbit)]
                # Проверка наличия кроликов
                if rabbits_in_cell:
                    # Формирование списка хищников с положительными очками
                    predators = [e for e in grid[i][j] if isinstance(e, (Wolf, SheWolf)) and e.points > 0]
                    # Проверка наличия хищников
                    if predators:
                        # Выбор кролика для съедения
                        rabbit = rabbits_in_cell[0]
                        # Выбор случайного хищника
                        predator = random.choice(predators)
                        # Увеличение очков хищника
                        predator.points += 1
                        # Удаление кролика из клетки
                        grid[i][j].remove(rabbit)
                        # Проверка наличия кролика в общем списке
                        if rabbit in rabbits_list:
                            # Удаление кролика из списка
                            rabbits_list.remove(rabbit)
                
                # Проверка наличия нескольких животных в клетке
                if len(grid[i][j]) > 1:
                    # Нахождение первой живой волчицы (приоритет 1)
                    she_wolf = next((e for e in grid[i][j] if isinstance(e, SheWolf) and e.points > 0), None)
                    # Нахождение первого живого волка (приоритет 2)
                    wolf = next((e for e in grid[i][j] if isinstance(e, Wolf) and e.points > 0), None)
                    # Нахождение первого кролика (приоритет 3)
                    rabbit = next((e for e in grid[i][j] if isinstance(e, Rabbit)), None)
                    # Проверка наличия волчицы
                    if she_wolf:
                        # Оставить волчицу в клетке
                        grid[i][j] = [she_wolf]
                        # Добавление волчицы в новый список
                        new_she_wolves_list.append(she_wolf)
                    # Проверка наличия волка при отсутствии волчицы
                    elif wolf:
                        # Оставить волка
                        grid[i][j] = [wolf]
                        # Добавление волка в новый список
                        new_wolves_list.append(wolf)
                    # Проверка наличия кролика при отсутствии хищников
                    elif rabbit:
                        # Оставить кролика
                        grid[i][j] = [rabbit]
                        # Добавление кролика в новый список
                        new_rabbits_list.append(rabbit)
                    # Обработка случая отсутствия подходящих животных
                    else:
                        # Очистка клетки
                        grid[i][j] = []
                # Проверка наличия одного животного в клетке
                elif grid[i][j]:
                    # Получение единственного животного
                    entity = grid[i][j][0]
                    # Проверка типа животного
                    if isinstance(entity, Rabbit):
                        # Добавление кролика в новый список
                        new_rabbits_list.append(entity)
                    # Проверка наличия живого волка
                    elif isinstance(entity, Wolf) and entity.points > 0:
                        # Добавление волка в новый список
                        new_wolves_list.append(entity)
                    # Проверка наличия живой волчицы
                    elif isinstance(entity, SheWolf) and entity.points > 0:
                        # Добавление волчицы в новый список
                        new_she_wolves_list.append(entity)
                    # Обработка мертвого животного
                    else:
                        # Очистка клетки
                        grid[i][j] = []
                # Обработка пустой клетки
                else:
                    # Оставить клетку пустой
                    grid[i][j] = []

    # Обновление списков животных
    rabbits_list[:] = new_rabbits_list
    wolves_list[:] = new_wolves_list
    she_wolves_list[:] = new_she_wolves_list

    # Возврат обновленной сетки и списков
    return grid, rabbits_list, wolves_list, she_wolves_list

# Функция для обработки поведения кроликов
def process_rabbits(grid, rabbits_list, N, M):
    # Создание списка для новых кроликов
    new_rabbits = []
    # Проход по копии списка кроликов
    for rabbit in rabbits_list[:]:
        # Получение текущей клетки кролика
        current_cell = grid[rabbit.x][rabbit.y]
        # Проверка наличия кролика в своей клетке
        if rabbit not in current_cell:
            # Пропуск итерации при отсутствии кролика
            continue
        
        # Проверка вероятности размножения, сравнение с рандомным числом от 0 до 1
        if random.random() < 0.3:
            # Получение соседних клеток
            neighbors = get_neighbors(rabbit.x, rabbit.y, N, M)
            # Фильтрация свободных соседних клеток
            free_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # Проверка наличия свободных клеток
            if free_neighbors:
                # Выбор случайных координат для перемещения
                new_x, new_y = random.choice(free_neighbors)
                # Создание нового кролика в текущей клетке
                new_rabbit = Rabbit(rabbit.x, rabbit.y)
                # Добавление нового кролика в клетку
                grid[rabbit.x][rabbit.y].append(new_rabbit)
                # Добавление нового кролика в список
                new_rabbits.append(new_rabbit)
                # Проверка наличия кролика в текущей клетке
                if rabbit in current_cell:
                    # Удаление старого кролика из клетки
                    current_cell.remove(rabbit)
                # Обновление координат старого кролика
                rabbit.x, rabbit.y = new_x, new_y
                # Добавление старого кролика в новую клетку
                grid[new_x][new_y].append(rabbit)
        # Обработка случая без размножения
        else:
            # Проверка вероятности остаться на месте (1/9)
            if random.random() < 1/9:
                # Пропуск перемещения
                continue
            # Получение соседних клеток
            neighbors = get_neighbors(rabbit.x, rabbit.y, N, M)
            # Фильтрация свободных клеток
            free_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # Проверка наличия свободных клеток
            if free_neighbors:
                # Выбор случайных координат
                new_x, new_y = random.choice(free_neighbors)
                # Проверка наличия кролика в текущей клетке
                if rabbit in current_cell:
                    # Удаление кролика из текущей клетки
                    current_cell.remove(rabbit)
                # Обновление координат кролика
                rabbit.x, rabbit.y = new_x, new_y
                # Добавление кролика в новую клетку
                grid[new_x][new_y].append(rabbit)
    
    # Добавление новых кроликов в общий список
    rabbits_list.extend(new_rabbits)
    
    # Возврат обновленной сетки и списка кроликов
    return grid, rabbits_list

# Функция для обработки поведения волчиц
def process_she_wolves(grid, she_wolves_list, rabbits_list, N, M):
    # Проход по копии списка волчиц
    for she_wolf in she_wolves_list[:]:
        # Получение текущей клетки волчицы
        current_cell = grid[she_wolf.x][she_wolf.y]
        # Проверка наличия волчицы в клетке
        if she_wolf not in current_cell:
            # Пропуск итерации
            continue
        
        # Установка флага съедения кролика
        ate_rabbit = False
        # Формирование списка кроликов в текущей клетке
        rabbits_in_cell = [e for e in grid[she_wolf.x][she_wolf.y] if isinstance(e, Rabbit)]
        # Проверка наличия кроликов
        if rabbits_in_cell:
            # Выбор кролика для съедения
            rabbit_to_eat = rabbits_in_cell[0]
            # Удаление кролика из клетки
            current_cell.remove(rabbit_to_eat)
            # Проверка наличия кролика в общем списке
            if rabbit_to_eat in rabbits_list:
                # Удаление кролика из списка
                rabbits_list.remove(rabbit_to_eat)
            # Увеличение очков волчицы
            she_wolf.points += 1
            # Установка флага съедения
            ate_rabbit = True
        # Обработка отсутствия кролика в текущей клетке
        else:
            # Получение соседних клеток
            neighbors = get_neighbors(she_wolf.x, she_wolf.y, N, M)
            # Фильтрация клеток с кроликами
            rabbit_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, Rabbit) for e in grid[nx][ny])]
            # Проверка наличия кроликов в соседних клетках
            if rabbit_neighbors:
                # Выбор случайной клетки с кроликом
                target_x, target_y = random.choice(rabbit_neighbors)
                # Проверка наличия волчицы в текущей клетке
                if she_wolf in current_cell:
                    # Удаление волчицы из текущей клетки
                    current_cell.remove(she_wolf)
                # Обновление координат волчицы
                she_wolf.x, she_wolf.y = target_x, target_y
                # Добавление волчицы в целевую клетку
                grid[target_x][target_y].append(she_wolf)
                # Формирование списка кроликов в целевой клетке
                rabbits_in_target = [e for e in grid[target_x][target_y] if isinstance(e, Rabbit)]
                # Проверка наличия кроликов
                if rabbits_in_target:
                    # Выбор кролика для съедения
                    rabbit_to_eat = rabbits_in_target[0]
                    # Удаление кролика из клетки
                    grid[target_x][target_y].remove(rabbit_to_eat)
                    # Проверка наличия кролика в списке
                    if rabbit_to_eat in rabbits_list:
                        # Удаление кролика из списка
                        rabbits_list.remove(rabbit_to_eat)
                    # Увеличение очков волчицы
                    she_wolf.points += 1
                    # Установка флага съедения
                    ate_rabbit = True
        
        # Проверка отсутствия съедения кролика
        if not ate_rabbit:
            # Уменьшение очков волчицы
            she_wolf.points -= 0.1
            # Получение соседних клеток
            neighbors = get_neighbors(she_wolf.x, she_wolf.y, N, M)
            # Фильтрация свободных клеток
            empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # Проверка наличия свободных клеток
            if empty_neighbors:
                # Выбор случайных координат
                new_x, new_y = random.choice(empty_neighbors)
                # Проверка наличия волчицы в текущей клетке
                if she_wolf in current_cell:
                    # Удаление волчицы из текущей клетки
                    current_cell.remove(she_wolf)
                # Обновление координат волчицы
                she_wolf.x, she_wolf.y = new_x, new_y
                # Добавление волчицы в новую клетку
                grid[new_x][new_y].append(she_wolf)
        
        # Проверка достаточности очков у волчицы
        if she_wolf.points <= 0:
            # Проверка наличия волчицы в клетке
            if she_wolf in grid[she_wolf.x][she_wolf.y]:
                # Удаление волчицы из клетки
                grid[she_wolf.x][she_wolf.y].remove(she_wolf)
            # Проверка наличия волчицы в списке
            if she_wolf in she_wolves_list:
                # Удаление волчицы из списка
                she_wolves_list.remove(she_wolf)
    
    # Возврат обновленной сетки и списков
    return grid, she_wolves_list, rabbits_list

# Функция для обработки поведения волков
def process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M):
    # Проход по копии списка волков
    for wolf in wolves_list[:]:
        # Получение текущей клетки волка
        current_cell = grid[wolf.x][wolf.y]
        # Проверка наличия волка в клетке
        if wolf not in current_cell:
            # Пропуск итерации
            continue
        
        # Установка флагов для съедения и размножения
        ate_rabbit = False
        reproduction = False
        # Формирование списка кроликов в текущей клетке
        rabbits_in_cell = [e for e in current_cell if isinstance(e, Rabbit)]
        # Проверка наличия кроликов
        if rabbits_in_cell:
            # Выбор кролика для съедения
            rabbit_to_eat = rabbits_in_cell[0]
            # Удаление кролика из клетки
            current_cell.remove(rabbit_to_eat)
            # Проверка наличия кролика в списке
            if rabbit_to_eat in rabbits_list:
                # Удаление кролика из списка
                rabbits_list.remove(rabbit_to_eat)
            # Увеличение очков волка
            wolf.points += 1
            # Установка флага съедения
            ate_rabbit = True
        # Обработка отсутствия кролика в текущей клетке
        else:
            # Получение соседних клеток
            neighbors = get_neighbors(wolf.x, wolf.y, N, M)
            # Фильтрация клеток с кроликами
            rabbit_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, Rabbit) for e in grid[nx][ny])]
            # Проверка наличия кроликов в соседних клетках
            if rabbit_neighbors:
                # Выбор случайной клетки с кроликом
                target_x, target_y = random.choice(rabbit_neighbors)
                # Проверка наличия волка в текущей клетке
                if wolf in current_cell:
                    # Удаление волка из текущей клетки
                    current_cell.remove(wolf)
                # Обновление координат волка
                wolf.x, wolf.y = target_x, target_y
                # Добавление волка в целевую клетку
                grid[target_x][target_y].append(wolf)
                # Формирование списка кроликов в целевой клетке
                rabbits_in_target = [e for e in grid[target_x][target_y] if isinstance(e, Rabbit)]
                # Проверка наличия кроликов
                if rabbits_in_target:
                    # Выбор кролика для съедения
                    rabbit_to_eat = rabbits_in_target[0]
                    # Удаление кролика из клетки
                    grid[target_x][target_y].remove(rabbit_to_eat)
                    # Проверка наличия кролика в списке
                    if rabbit_to_eat in rabbits_list:
                        # Удаление кролика из списка
                        rabbits_list.remove(rabbit_to_eat)
                    # Увеличение очков волка
                    wolf.points += 1
                    # Установка флага съедения
                    ate_rabbit = True
            # Обработка отсутствия кроликов поблизости
            else:
                # Фильтрация клеток с живыми волчицами
                she_wolf_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, SheWolf) and e.points > 0 for e in grid[nx][ny])]
                # Проверка наличия волчиц поблизости
                if she_wolf_neighbors:
                    # Выбор случайной клетки с волчицей
                    target_x, target_y = random.choice(she_wolf_neighbors)
                    # Проверка наличия волка в текущей клетке
                    if wolf in current_cell:
                        # Удаление волка из текущей клетки
                        current_cell.remove(wolf)
                    # Обновление координат волка
                    wolf.x, wolf.y = target_x, target_y
                    # Добавление волка в целевую клетку
                    grid[target_x][target_y].append(wolf)
                    # Формирование списка живых волчиц в клетке
                    she_wolves_in_cell = [e for e in grid[target_x][target_y] if isinstance(e, SheWolf) and e.points > 0]
                    # Проверка наличия волчиц
                    if she_wolves_in_cell:
                        # Выбор первой волчицы
                        she_wolf = she_wolves_in_cell[0]
                        # Получение соседних клеток
                        neighbors = get_neighbors(target_x, target_y, N, M)
                        # Фильтрация свободных клеток
                        empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
                        # Проверка наличия минимум 3 свободных клеток для размножения
                        if len(empty_neighbors) >= 3:
                            # Определение пола потомства случайным образом
                            descendant_gender = random.choice(['wolf', 'she_wolf'])
                            # Проверка пола потомка (волк)
                            if descendant_gender == 'wolf':
                                # Создание нового волка
                                descendant = Wolf(target_x, target_y)
                                # Добавление волка в список
                                wolves_list.append(descendant)
                            # Проверка пола потомка (волчица)
                            else:
                                # Создание новой волчицы
                                descendant = SheWolf(target_x, target_y)
                                # Добавление волчицы в список
                                she_wolves_list.append(descendant)
                            # Установка начальных очков потомства
                            descendant.points = 1.0
                            # Добавление потомства в клетку
                            grid[target_x][target_y].append(descendant)
                            # Установка флага размножения
                            reproduction = True
                            # Выбор координат для перемещения волчицы
                            new_x, new_y = random.choice(empty_neighbors)
                            # Проверка наличия волчицы в клетке
                            if she_wolf in grid[target_x][target_y]:
                                # Удаление волчицы из клетки
                                grid[target_x][target_y].remove(she_wolf)
                            # Обновление координат волчицы
                            she_wolf.x, she_wolf.y = new_x, new_y
                            # Добавление волчицы в новую клетку
                            grid[new_x][new_y].append(she_wolf)
                            # Удаление использованных координат из списка
                            empty_neighbors.remove((new_x, new_y))
                            # Уменьшение очков волчицы
                            she_wolf.points -= 0.1
                            # Выбор координат для перемещения волка
                            new_x, new_y = random.choice(empty_neighbors)
                            # Проверка наличия волка в клетке
                            if wolf in grid[target_x][target_y]:
                                # Удаление волка из клетки
                                grid[target_x][target_y].remove(wolf)
                            # Обновление координат волка
                            wolf.x, wolf.y = new_x, new_y
                            # Добавление волка в новую клетку
                            grid[new_x][new_y].append(wolf)
                            # Уменьшение очков волка
                            wolf.points -= 0.1
                        # Обработка случая с недостатком свободных клеток
                        else:
                            # Пропуск размножения
                            continue
        
        # Проверка отсутствия съедения или размножения
        if not ate_rabbit and not reproduction:
            # Уменьшение очков волка
            wolf.points -= 0.1
            # Получение соседних клеток
            neighbors = get_neighbors(wolf.x, wolf.y, N, M)
            # Фильтрация свободных клеток
            empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # Проверка наличия свободных клеток
            if empty_neighbors:
                # Выбор случайных координат
                new_x, new_y = random.choice(empty_neighbors)
                # Проверка наличия волка в текущей клетке
                if wolf in current_cell:
                    # Удаление волка из текущей клетки
                    current_cell.remove(wolf)
                # Обновление координат волка
                wolf.x, wolf.y = new_x, new_y
                # Добавление волка в новую клетку
                grid[new_x][new_y].append(wolf)
        
        # Проверка достаточности очков у волка
        if wolf.points <= 0:
            # Проверка наличия волка в клетке
            if wolf in grid[wolf.x][wolf.y]:
                # Удаление волка из клетки
                grid[wolf.x][wolf.y].remove(wolf)
            # Проверка наличия волка в списке
            if wolf in wolves_list:
                # Удаление волка из списка
                wolves_list.remove(wolf)
    
    # Возврат обновленной сетки и списков
    return grid, wolves_list, rabbits_list, she_wolves_list

# Функция для выполнения одного шага симуляции
def run_simulation_step(grid, rabbits_list, wolves_list, she_wolves_list, N, M):
    # Обработка поведения волков
    grid, wolves_list, rabbits_list, she_wolves_list = process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M)
    
    # Обработка поведения волчиц
    grid, she_wolves_list, rabbits_list = process_she_wolves(grid, she_wolves_list, rabbits_list, N, M)
    
    # Обработка поведения кроликов
    grid, rabbits_list = process_rabbits(grid, rabbits_list, N, M)
    
    # Очистка сетки в конце шага
    grid, rabbits_list, wolves_list, she_wolves_list = clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
    
    # Возврат обновленного состояния
    return grid, rabbits_list, wolves_list, she_wolves_list

# Функция для подготовки данных сетки для отображения
def prepare_grid_data(grid, N, M):
    # Создание сетки 15x15 с заполнением значениями None
    grid_data = [[None for i in range(15)] for i in range(15)]
    # Проход по клеткам заданного размера N x M
    for i in range(N):
        for j in range(M):
            # Проверка наличия животных в клетке
            if grid[i][j]:
                # Получение первого животного в клетке
                entity = grid[i][j][0]
                # Проверка типа животного (волк)
                if isinstance(entity, Wolf):
                    # Установка пути к изображению волка
                    grid_data[i][j] = '/static/images/wolf.png'
                # Проверка типа животного (волчица)
                elif isinstance(entity, SheWolf):
                    # Установка пути к изображению волчицы
                    grid_data[i][j] = '/static/images/she_wolf.png'
                # Проверка типа животного (кролик)
                elif isinstance(entity, Rabbit):
                    # Установка пути к изображению кролика
                    grid_data[i][j] = '/static/images/rabbit.png'
    # Возврат подготовленной сетки данных
    return grid_data

# Функция для управления симуляцией через веб-интерфейс
def wolf_island_controller(action, N_str, M_str, rabbits_str, wolves_str, she_wolves_str, steps_str):
    # Объявление глобальной переменной simulation_state
    global simulation_state

    # Проверка действия на начальную загрузку или сброс
    if not action or action == 'reset':
        # Очистка состояния симуляции
        simulation_state = {}
        # Возврат начального состояния страницы
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': 15,
            'M': 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': '',
            'wolves': '',
            'she_wolves': '',
            'steps': '',
            'refresh': False,
            'error': ''
        }

    # Проверка действия на генерацию случайных параметров
    if action == 'generate':
        # Генерация случайных размеров сетки
        N = random.randint(5, 15)
        M = random.randint(5, 15)
        # Вычисление максимального количества животных
        max_animals = (N * M) // 10
        # Генерация случайных количеств животных
        rabbits = random.randint(1, max_animals)
        wolves = random.randint(1, max_animals)
        she_wolves = random.randint(1, max_animals)
        # Генерация случайного количества шагов
        steps = random.randint(10, 240)
        # Очистка состояния симуляции
        simulation_state = {}
        # Сохранение сгенерированных параметров в состоянии симуляции без инициализации животных
        simulation_state = {
            'N': N,
            'M': M,
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves,
            'steps': steps
        }
        # Создание пустой сетки для отображения
        grid_data = [[None for i in range(15)] for i in range(15)]
        # Формирование статистики с нулевыми значениями
        stats = {
            'step': 0,
            'rabbits': 0,
            'wolves': 0,
            'she_wolves': 0
        }
        # Возврат результата генерации с пустой сеткой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': grid_data,
            'stats': stats,
            'rabbits': rabbits,
            'wolves': wolves,
            'she_wolves': she_wolves,
            'steps': steps,
            'refresh': False,
            'error': ''
        }

    # Сохранение входных данных для возврата в форму
    input_data = {
        'N': N_str if N_str else '15',
        'M': M_str if M_str else '15',
        'rabbits': rabbits_str,
        'wolves': wolves_str,
        'she_wolves': she_wolves_str,
        'steps': steps_str
    }

    # Валидация параметра N
    try:
        # Преобразование строки N в число с значением по умолчанию 15
        N = int(N_str) if N_str else 15
        # Проверка допустимого диапазона N
        if not (5 <= N <= 15):
            # Очистка поля N при ошибке
            input_data['N'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': 15,
                'M': int(input_data['M']) if input_data['M'] else 15,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of N. Must be an integer from 5 to 15.'
            }
    # Обработка исключения при некорректном формате N
    except ValueError:
        # Очистка поля N
        input_data['N'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': 15,
            'M': int(input_data['M']) if input_data['M'] else 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of N. Must be an integer from 5 to 15.'
        }

    # Валидация параметра M
    try:
        # Преобразование строки M в число
        M = int(M_str) if M_str else 15
        # Проверка допустимого диапазона M
        if not (5 <= M <= 15):
            # Очистка поля M
            input_data['M'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': 15,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of M. Must be an integer from 5 to 15.'
            }
    # Обработка исключения при некорректном формате M
    except ValueError:
        # Очистка поля M
        input_data['M'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of M. Must be an integer from 5 to 15.'
        }

    # Вычисление максимального количества животных
    max_animals = (N * M) // 10
    # Валидация количества кроликов
    try:
        # Преобразование строки кроликов в число
        rabbits = int(rabbits_str) if rabbits_str else 0
        # Проверка допустимого диапазона кроликов
        if rabbits_str and not (1 <= rabbits <= max_animals):
            # Очистка поля кроликов
            input_data['rabbits'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of rabbits. Must be an integer from 1 to {max_animals}.'
            }
    # Обработка исключения при некорректном формате
    except ValueError:
        # Очистка поля кроликов
        input_data['rabbits'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of rabbits. Must be an integer from 1 to {max_animals}.'
        }

    # Валидация количества волков
    try:
        # Преобразование строки волков в число
        wolves = int(wolves_str) if wolves_str else 0
        # Проверка допустимого диапазона волков
        if wolves_str and not (1 <= wolves <= max_animals):
            # Очистка поля волков
            input_data['wolves'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of wolves. Must be an integer from 1 to {max_animals}.'
            }
    # Обработка исключения при некорректном формате
    except ValueError:
        # Очистка поля волков
        input_data['wolves'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of wolves. Must be an integer from 1 to {max_animals}.'
        }

    # Валидация количества волчиц
    try:
        # Преобразование строки волчиц в число
        she_wolves = int(she_wolves_str) if she_wolves_str else 0
        # Проверка допустимого диапазона волчиц
        if she_wolves_str and not (1 <= she_wolves <= max_animals):
            # Очистка поля волчиц
            input_data['she_wolves'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of she-wolves. Must be an integer from 1 to {max_animals}.'
            }
    # Обработка исключения при некорректном формате
    except ValueError:
        # Очистка поля волчиц
        input_data['she_wolves'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of she-wolves. Must be an integer from 1 to {max_animals}.'
        }

    # Валидация количества шагов
    try:
        # Преобразование строки шагов в число
        steps = int(steps_str) if steps_str else 0
        # Проверка допустимого диапазона шагов
        if steps_str and not (10 <= steps <= 240):
            # Очистка поля шагов
            input_data['steps'] = ''
            # Возврат состояния с ошибкой
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of steps. Must be an integer from 10 to 240.'
            }
    # Обработка исключения при некорректном формате
    except ValueError:
        # Очистка поля шагов
        input_data['steps'] = ''
        # Возврат состояния с ошибкой
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of steps. Must be an integer from 10 to 240.'
        }

# Проверка первого запуска симуляции
    if action == 'start' and not simulation_state.get('running'):
        # Проверка заполнения всех полей
        if not (rabbits and wolves and she_wolves and steps):
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'All fields must be filled to start the simulation.'
            }
        # Инициализация состояния симуляции
        simulation_state = {
            'N': N,
            'M': M,
            'steps': steps,
            'current_step': 0,
            'running': True,
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves
        }
        # Инициализация симуляции
        grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, rabbits, wolves, she_wolves)
        # Сохранение состояния сетки и списков
        simulation_state['grid'] = grid
        simulation_state['rabbits_list'] = rabbits_list
        simulation_state['wolves_list'] = wolves_list
        simulation_state['she_wolves_list'] = she_wolves_list
    # Проверка состояния симуляции
    elif not simulation_state.get('running'):
        # Сохранение начальных значений животных
        simulation_state = {
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves
        }
        # Инициализация симуляции без запуска
        grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, rabbits, wolves, she_wolves)
    # Обработка продолжающейся симуляции
    else:
        # Извлечение параметров из состояния
        N = simulation_state['N']
        M = simulation_state['M']
        steps = simulation_state['steps']
        current_step = simulation_state['current_step']
        grid = simulation_state['grid']
        rabbits_list = simulation_state['rabbits_list']
        wolves_list = simulation_state['wolves_list']
        she_wolves_list = simulation_state['she_wolves_list']
        rabbits = simulation_state['initial_rabbits']
        wolves = simulation_state['initial_wolves']
        she_wolves = simulation_state['initial_she_wolves']

        # Проверка завершения шагов
        if current_step < steps:
            # Выполнение шага симуляции
            grid, rabbits_list, wolves_list, she_wolves_list = run_simulation_step(
                grid, rabbits_list, wolves_list, she_wolves_list, N, M
            )
            # Увеличение счетчика шагов
            simulation_state['current_step'] += 1
            # Обновление состояния
            simulation_state['grid'] = grid
            simulation_state['rabbits_list'] = rabbits_list
            simulation_state['wolves_list'] = wolves_list
            simulation_state['she_wolves_list'] = she_wolves_list
            
            # Проверка на вымирание всех животных
            if not rabbits_list and not wolves_list and not she_wolves_list:
                simulation_state['running'] = False
                simulation_state['extinction'] = True
        # Обработка завершения симуляции по шагам
        else:
            # Остановка симуляции
            simulation_state['running'] = False

    # Формирование статистики текущего состояния
    stats = {
        'step': simulation_state.get('current_step', 0),
        'rabbits': len(simulation_state.get('rabbits_list', [])),
        'wolves': len(simulation_state.get('wolves_list', [])),
        'she_wolves': len(simulation_state.get('she_wolves_list', []))
    }
    # Подготовка данных сетки для отображения
    grid_data = prepare_grid_data(grid, N, M)

    # Определение сообщения о состоянии симуляции
    error_message = ''
    if simulation_state.get('extinction', False):
        error_message = 'All animals have died out, simulation stopped'
    elif not simulation_state.get('running', False) and simulation_state.get('current_step', 0) >= steps:
        error_message = 'Simulation completed'

    # Возврат текущего состояния симуляции
    return {
        'title': 'The model of movement and death',
        'year': datetime.now().year,
        'N': N,
        'M': M,
        'grid_data': grid_data,
        'stats': stats,
        'rabbits': input_data['rabbits'],
        'wolves': input_data['wolves'],
        'she_wolves': input_data['she_wolves'],
        'steps': input_data['steps'],
        'refresh': simulation_state.get('running', False),
        'error': error_message
    }