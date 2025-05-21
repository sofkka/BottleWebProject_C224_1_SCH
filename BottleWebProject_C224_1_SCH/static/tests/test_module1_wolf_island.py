# -*- coding: cp1251 -*-

import unittest
import random
import json
import os
import sys
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock

# Добавление корневой директории проекта в sys.path для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    # Импорт классов и функций из модуля wolf_island
    from static.controllers.module1_wolf_island import (Rabbit, Wolf, SheWolf, get_neighbors, initialize_simulation,
                                                       clean_grid, process_rabbits, process_she_wolves, process_wolves,
                                                       run_simulation_step, prepare_grid_data, save_to_json, wolf_island_controller,
                                                       simulation_state)
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    raise

class TestWolfIsland(unittest.TestCase):
    # Тесты для классов животных
    def test_rabbit_init(self):
        # Создание объекта кролика с координатами (2, 3)
        rabbit = Rabbit(2, 3)
        # Проверка инициализации кролика
        self.assertEqual(rabbit.x, 2, "Координата x кролика должна быть 2")
        self.assertEqual(rabbit.y, 3, "Координата y кролика должна быть 3")

    def test_wolf_init(self):
        # Создание объекта волка с координатами (1, 4)
        wolf = Wolf(1, 4)
        # Проверка инициализации волка
        self.assertEqual(wolf.x, 1, "Координата x волка должна быть 1")
        self.assertEqual(wolf.y, 4, "Координата y волка должна быть 4")
        self.assertEqual(wolf.points, 1.0, "Начальные очки волка должны быть 1.0")

    def test_she_wolf_init(self):
        # Создание объекта волчицы с координатами (0, 5)
        she_wolf = SheWolf(0, 5)
        # Проверка инициализации волчицы
        self.assertEqual(she_wolf.x, 0, "Координата x волчицы должна быть 0")
        self.assertEqual(she_wolf.y, 5, "Координата y волчицы должна быть 5")
        self.assertEqual(she_wolf.points, 1.0, "Начальные очки волчицы должны быть 1.0")

    # Тесты для функции get_neighbors
    def test_get_neighbors_center(self):
        # Получение соседних клеток для центральной позиции (2, 2) в сетке 5x5
        neighbors = get_neighbors(2, 2, 5, 5)
        # Ожидаемые координаты соседних клеток вокруг центральной позиции
        expected = [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)]
        # Проверка соседних клеток для центральной позиции
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены все 8 соседних клеток для центральной клетки")

    def test_get_neighbors_corner(self):
        # Получение соседних клеток для угловой позиции (0, 0) в сетке 5x5
        neighbors = get_neighbors(0, 0, 5, 5)
        # Ожидаемые координаты соседних клеток для угловой позиции
        expected = [(0,1), (1,0), (1,1)]
        # Проверка соседних клеток для угловой позиции
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены 3 соседних клетки для угловой клетки")

    def test_get_neighbors_edge(self):
        # Получение соседних клеток для позиции на границе (1, 0) в сетке 5x5
        neighbors = get_neighbors(1, 0, 5, 5)
        # Ожидаемые координаты соседних клеток для позиции на границе
        expected = [(0,0), (0,1), (1,1), (2,0), (2,1)]
        # Проверка соседних клеток для позиции на границе
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены 5 соседних клеток для клетки на границе")

    # Тесты для функции initialize_simulation
    def test_initialize_simulation(self):
        # Функция для предотвращения перемешивания списка, возвращающая исходный список
        def no_shuffle(lst):
            return lst
        
        # Мокирование результата random.shuffle для контроля размещения животных
        with patch('random.shuffle') as mock_shuffle:
            # Установка поведения mock_shuffle: вместо перемешивания возвращается исходный список
            mock_shuffle.side_effect = no_shuffle
            N, M = 5, 5
            # Создание двумерного списка с пустыми списками для каждой клетки сетки
            grid = [[[] for i in range(M)] for i in range(N)]
            # Инициализация симуляции с 2 кроликами, 1 волком и 1 волчицей
            grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, 2, 1, 1)
            # Проверка корректности инициализации симуляции
            self.assertEqual(len(grid), N, "Длина сетки должна быть равна N")
            self.assertEqual(len(grid[0]), M, "Ширина сетки должна быть равна M")
            self.assertEqual(len(rabbits_list), 2, "Должно быть 2 кролика")
            self.assertEqual(len(wolves_list), 1, "Должен быть 1 волк")
            self.assertEqual(len(she_wolves_list), 1, "Должна быть 1 волчица")
            # Определение ожидаемых позиций животных (2 кролика, 1 волк, 1 волчица) в последней строке сетки 5x5
            expected_positions = [(4, 4), (4, 3), (4, 2), (4, 1)]
            self.assertEqual((rabbits_list[0].x, rabbits_list[0].y), expected_positions[0], "Первый кролик размещен неверно")
            self.assertEqual((rabbits_list[1].x, rabbits_list[1].y), expected_positions[1], "Второй кролик размещен неверно")
            self.assertEqual((wolves_list[0].x, wolves_list[0].y), expected_positions[2], "Волк размещен неверно")
            self.assertEqual((she_wolves_list[0].x, she_wolves_list[0].y), expected_positions[3], "Волчица размещена неверно")

    # Тесты для функции clean_grid
    def test_clean_grid_rabbit_eaten_by_wolf(self):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Создание кролика и волка в одной клетке (2, 2)
        rabbit = Rabbit(2, 2)
        wolf = Wolf(2, 2)
        grid[2][2] = [rabbit, wolf]
        rabbits_list = [rabbit]
        wolves_list = [wolf]
        she_wolves_list = []
        # Вызов функции очистки сетки для обработки взаимодействия животных
        grid, new_rabbits, new_wolves, new_she_wolves = clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
        # Проверка очистки сетки после поедания кролика волком
        self.assertEqual(len(new_rabbits), 0, "Кролик должен быть съеден")
        self.assertEqual(len(new_wolves), 1, "Волк должен остаться")
        self.assertEqual(new_wolves[0].points, 2.0, "Очки волка должны увеличиться")
        self.assertEqual(len(grid[2][2]), 1, "В клетке должен остаться только волк")
        self.assertIsInstance(grid[2][2][0], Wolf, "В клетке должен быть волк")

    # Тесты для функции process_rabbits
    # Мокирование результата random.random и random.choice для контроля размножения кроликов
    @patch('random.random')
    @patch('random.choice')
    def test_process_rabbits_reproduction(self, mock_choice, mock_random):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Создание кролика в клетке (2, 2)
        rabbit = Rabbit(2, 2)
        grid[2][2] = [rabbit]
        rabbits_list = [rabbit]
        # Установка вероятности размножения (0.2 < 0.3, значит кролик размножается)
        mock_random.side_effect = [0.2]
        # Установка выбора соседней клетки (2, 3) для перемещения кролика
        mock_choice.return_value = (2, 3)
        # Вызов функции обработки кроликов для проверки размножения
        grid, rabbits_list = process_rabbits(grid, rabbits_list, N, M)
        # Проверка размножения и перемещения кроликов
        self.assertEqual(len(rabbits_list), 2, "Должно быть 2 кролика после размножения")
        self.assertEqual((rabbits_list[0].x, rabbits_list[0].y), (2, 3), "Старый кролик должен переместиться")
        self.assertEqual((rabbits_list[1].x, rabbits_list[1].y), (2, 2), "Новый кролик должен быть в старой клетке")
        self.assertEqual(len(grid[2][2]), 1, "В старой клетке должен быть новый кролик")
        self.assertEqual(len(grid[2][3]), 1, "В новой клетке должен быть старый кролик")

    # Тесты для функции process_she_wolves
    def test_process_she_wolves_eat_rabbit_in_cell(self):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Создание кролика и волчицы в одной клетке (2, 2)
        rabbit = Rabbit(2, 2)
        she_wolf = SheWolf(2, 2)
        grid[2][2] = [rabbit, she_wolf]
        rabbits_list = [rabbit]
        she_wolves_list = [she_wolf]
        # Вызов функции обработки волчиц для проверки поедания кролика
        grid, she_wolves_list, rabbits_list = process_she_wolves(grid, she_wolves_list, rabbits_list, N, M)
        # Проверка поедания кролика волчицей
        self.assertEqual(len(rabbits_list), 0, "Кролик должен быть съеден")
        self.assertEqual(len(she_wolves_list), 1, "Волчица должна остаться")
        self.assertEqual(she_wolves_list[0].points, 2.0, "Очки волчицы должны увеличиться")
        self.assertEqual(len(grid[2][2]), 1, "В клетке должна остаться только волчица")

    # Тесты для функции process_wolves
    # Мокирование результата random.choice для контроля размножения волков
    @patch('random.choice')
    def test_process_wolves_reproduction(self, mock_choice):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Создание волка в клетке (2, 2) и волчицы в соседней клетке (2, 3)
        wolf = Wolf(2, 2)
        she_wolf = SheWolf(2, 3)
        grid[2][2] = [wolf]
        grid[2][3] = [she_wolf]
        wolves_list = [wolf]
        she_wolves_list = [she_wolf]
        rabbits_list = []
        # Установка последовательности выбора: клетка для размножения, пол нового волка, клетки для перемещения
        mock_choice.side_effect = [(2, 3), 'wolf', (2, 4), (3, 3)]
        # Вызов функции обработки волков для проверки размножения
        grid, wolves_list, rabbits_list, she_wolves_list = process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M)
        # Проверка размножения волков
        self.assertEqual(len(wolves_list), 2, "Должен появиться новый волк")
        self.assertEqual(len(she_wolves_list), 1, "Волчица должна остаться")
        self.assertEqual(wolves_list[0].points, 0.9, "Очки волка должны уменьшиться")
        self.assertEqual(she_wolves_list[0].points, 0.9, "Очки волчицы должны уменьшиться")
        self.assertEqual((wolves_list[1].x, wolves_list[1].y), (2, 3), "Новый волк должен быть в клетке размножения")

    # Тесты для функции run_simulation_step
    def test_run_simulation_step(self):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Создание кролика и волка в одной клетке (2, 2)
        rabbit = Rabbit(2, 2)
        wolf = Wolf(2, 2)
        grid[2][2] = [rabbit, wolf]
        rabbits_list = [rabbit]
        wolves_list = [wolf]
        she_wolves_list = []
        # Мокирование подфункций для проверки их вызова и возвращаемых значений
        with patch('static.controllers.module1_wolf_island.process_wolves', return_value=(grid, wolves_list, rabbits_list, she_wolves_list)) as mock_wolves, \
             patch('static.controllers.module1_wolf_island.process_she_wolves', return_value=(grid, she_wolves_list, rabbits_list)) as mock_she_wolves, \
             patch('static.controllers.module1_wolf_island.process_rabbits', return_value=(grid, rabbits_list)) as mock_rabbits, \
             patch('static.controllers.module1_wolf_island.clean_grid', return_value=(grid, rabbits_list, wolves_list, she_wolves_list)) as mock_clean:
            # Вызов функции выполнения шага симуляции
            result = run_simulation_step(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
            # Проверка выполнения шага симуляции
            mock_wolves.assert_called_once()
            mock_she_wolves.assert_called_once()
            mock_rabbits.assert_called_once()
            mock_clean.assert_called_once()
            self.assertEqual(result, (grid, rabbits_list, wolves_list, she_wolves_list), "Функция должна вернуть обновленные данные")

    # Тесты для функции prepare_grid_data
    def test_prepare_grid_data(self):
        N, M = 5, 5
        # Создание двумерного списка с пустыми списками для каждой клетки сетки
        grid = [[[] for i in range(M)] for i in range(N)]
        # Размещение животных в разных клетках сетки
        grid[0][0] = [Rabbit(0, 0)]
        grid[2][2] = [Wolf(2, 2)]
        grid[4][4] = [SheWolf(4, 4)]
        # Подготовка данных сетки для отображения (замена объектов на пути к изображениям)
        grid_data = prepare_grid_data(grid, N, M)
        # Проверка подготовки данных сетки
        self.assertEqual(grid_data[0][0], '/static/images/rabbit.png', "Должно быть изображение кролика")
        self.assertEqual(grid_data[2][2], '/static/images/wolf.png', "Должно быть изображение волка")
        self.assertEqual(grid_data[4][4], '/static/images/she_wolf.png', "Должно быть изображение волчицы")
        self.assertIsNone(grid_data[0][1], "Пустая клетка должна быть None")

    # Тесты для функции save_to_json
    # Мокирование результата os.makedirs, open, json.load, json.dump и datetime для контроля записи в файл
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_save_to_json(self, mock_datetime, mock_dump, mock_load, mock_open_file, mock_makedirs):
        # Установка текущей даты и времени для мокирования
        mock_datetime.now.return_value = datetime(2025, 5, 20, 22, 30)
        # Установка результата чтения JSON файла (пустой словарь)
        mock_load.return_value = {}
        # Создание состояния симуляции для сохранения
        simulation_state = {
            'current_step': 10,
            'rabbits_list': [Rabbit(1, 1)],
            'wolves_list': [Wolf(2, 2)],
            'she_wolves_list': [SheWolf(3, 3)]
        }
        # Входные параметры симуляции
        input_data = {
            'N': '5',
            'M': '5',
            'rabbits': '2',
            'wolves': '1',
            'she_wolves': '1',
            'steps': '10'
        }
        # Вызов функции сохранения данных в JSON
        success, error = save_to_json(simulation_state, input_data)
        # Проверка сохранения данных в JSON
        self.assertTrue(success, "Сохранение должно быть успешным")
        self.assertEqual(error, '', "Не должно быть ошибок")
        mock_dump.assert_called_once()
        # Ожидаемые данные для записи в JSON файл
        expected_data = {
            '2025-05-20': [{
                'time': '22:30:00',
                'input_parameters': {'N': 5, 'M': 5, 'rabbits': 2, 'wolves': 1, 'she_wolves': 1, 'steps': 10},
                'simulation_results': {'simulation_step': 10, 'rabbits': 1, 'wolves': 1, 'she_wolves': 1},
                'status': 'Simulation completed successfully'
            }]
        }
        self.assertEqual(mock_dump.call_args[0][0], expected_data, "Должны быть сохранены правильные данные")

    # Тесты для функции wolf_island_controller
    # Мокирование результата datetime для контроля даты
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_wolf_island_controller_reset(self, mock_datetime):
        # Установка текущей даты для мокирования
        mock_datetime.now.return_value = datetime(2025, 5, 20)
        # Вызов функции контроллера с командой сброса
        result = wolf_island_controller('reset', '', '', '', '', '', '')
        # Проверка сброса состояния симуляции
        self.assertEqual(result['N'], 15, "N должен быть 15")
        self.assertEqual(result['M'], 15, "M должен быть 15")
        self.assertEqual(result['stats'], {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0}, "Статистика должна быть сброшена")
        self.assertEqual(simulation_state, {}, "Состояние симуляции должно быть очищено")

    # Мокирование результата random.randint и datetime для контроля генерации параметров
    @patch('random.randint')
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_wolf_island_controller_generate(self, mock_datetime, mock_randint):
        # Установка текущей даты для мокирования
        mock_datetime.now.return_value = datetime(2025, 5, 20)
        # Установка последовательности случайных чисел для генерации параметров
        mock_randint.side_effect = [5, 5, 2, 1, 1, 20]
        # Вызов функции контроллера с командой генерации параметров
        result = wolf_island_controller('generate', '', '', '', '', '', '')
        # Проверка генерации случайных параметров
        self.assertEqual(result['N'], 5, "N должен быть сгенерирован")
        self.assertEqual(result['M'], 5, "M должен быть сгенерирован")
        self.assertEqual(result['rabbits'], 2, "Должно быть сгенерировано 2 кролика")
        self.assertEqual(result['wolves'], 1, "Должен быть сгенерирован 1 волк")
        self.assertEqual(result['she_wolves'], 1, "Должна быть сгенерирована 1 волчица")
        self.assertEqual(result['steps'], 20, "Должно быть сгенерировано 20 шагов")

    # Тесты валидации входных данных
    def test_wolf_island_controller_invalid_N(self):
        # Вызов функции контроллера с некорректным значением N (20 > 15)
        result = wolf_island_controller('start', '20', '5', '2', '1', '1', '50')
        # Проверка ошибки валидации N и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of N. Must be an integer from 5 to 15.', "Должна быть ошибка валидации N")
        self.assertEqual(result['N'], 15, "N должен быть сброшен на 15")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_N_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением N
        result = wolf_island_controller('start', 'abc', '5', '2', '1', '1', '50')
        # Проверка ошибки валидации нецелочисленного N и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of N. Must be an integer from 5 to 15.', "Должна быть ошибка валидации N")
        self.assertEqual(result['N'], 15, "N должен быть сброшен на 15")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_M(self):
        # Вызов функции контроллера с некорректным значением M (20 > 15)
        result = wolf_island_controller('start', '5', '20', '2', '1', '1', '50')
        # Проверка ошибки валидации M и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of M. Must be an integer from 5 to 15.', "Должна быть ошибка валидации M")
        self.assertEqual(result['M'], 15, "M должен быть сброшен на 15")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_M_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением M
        result = wolf_island_controller('start', '5', 'abc', '2', '1', '1', '50')
        # Проверка ошибки валидации нецелочисленного M и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of M. Must be an integer from 5 to 15.', "Должна быть ошибка валидации M")
        self.assertEqual(result['M'], 15, "M должен быть сброшен на 15")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_rabbits(self):
        # Вызов функции контроллера с некорректным значением rabbits (3 > 2)
        result = wolf_island_controller('start', '5', '5', '3', '1', '1', '50')
        # Проверка ошибки валидации rabbits и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of rabbits. Must be an integer from 1 to 2.', "Должна быть ошибка валидации rabbits")
        self.assertEqual(result['rabbits'], '', "Поле rabbits должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_rabbits_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением rabbits
        result = wolf_island_controller('start', '5', '5', 'abc', '1', '1', '50')
        # Проверка ошибки валидации нецелочисленного rabbits и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of rabbits. Must be an integer from 1 to 2.', "Должна быть ошибка валидации rabbits")
        self.assertEqual(result['rabbits'], '', "Поле rabbits должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_wolves(self):
        # Вызов функции контроллера с некорректным значением wolves (3 > 2)
        result = wolf_island_controller('start', '5', '5', '2', '3', '1', '50')
        # Проверка ошибки валидации wolves и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of wolves. Must be an integer from 1 to 2.', "Должна быть ошибка валидации wolves")
        self.assertEqual(result['wolves'], '', "Поле wolves должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_wolves_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением wolves
        result = wolf_island_controller('start', '5', '5', '2', 'abc', '1', '50')
        # Проверка ошибки валидации нецелочисленного wolves и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of wolves. Must be an integer from 1 to 2.', "Должна быть ошибка валидации wolves")
        self.assertEqual(result['wolves'], '', "Поле wolves должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_she_wolves(self):
        # Вызов функции контроллера с некорректным значением she_wolves (3 > 2)
        result = wolf_island_controller('start', '5', '5', '2', '1', '3', '50')
        # Проверка ошибки валидации she_wolves и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of she-wolves. Must be an integer from 1 to 2.', "Должна быть ошибка валидации she-wolves")
        self.assertEqual(result['she_wolves'], '', "Поле she_wolves должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_she_wolves_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением she_wolves
        result = wolf_island_controller('start', '5', '5', '2', '1', 'abc', '50')
        # Проверка ошибки валидации нецелочисленного she_wolves и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of she-wolves. Must be an integer from 1 to 2.', "Должна быть ошибка валидации she-wolves")
        self.assertEqual(result['she_wolves'], '', "Поле she_wolves должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

    def test_wolf_island_controller_invalid_steps(self):
        # Вызов функции контроллера с некорректным значением steps (5 < 10)
        result = wolf_island_controller('start', '5', '5', '2', '1', '1', '5')
        # Проверка ошибки валидации steps и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of steps. Must be an integer from 10 to 240.', "Должна быть ошибка валидации steps")
        self.assertEqual(result['steps'], '', "Поле steps должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")

    def test_wolf_island_controller_invalid_steps_non_integer(self):
        # Вызов функции контроллера с нецелочисленным значением steps
        result = wolf_island_controller('start', '5', '5', '2', '1', '1', 'abc')
        # Проверка ошибки валидации нецелочисленного steps и сохранения остальных полей
        self.assertEqual(result['error'], 'Incorrect value of steps. Must be an integer from 10 to 240.', "Должна быть ошибка валидации steps")
        self.assertEqual(result['steps'], '', "Поле steps должно быть очищено")
        self.assertEqual(result['N'], 5, "N должен остаться 5")
        self.assertEqual(result['M'], 5, "M должен остаться 5")
        self.assertEqual(result['rabbits'], '2', "Поле rabbits должно остаться '2'")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")

    def test_wolf_island_controller_missing_fields(self):
        # Вызов функции контроллера с пустым полем rabbits
        result = wolf_island_controller('start', '5', '5', '', '1', '1', '50')
        # Проверка ошибки из-за незаполненных полей
        self.assertEqual(result['error'], 'All fields must be filled to start the simulation.', "Должна быть ошибка из-за незаполненных полей")
        self.assertEqual(result['rabbits'], '', "Поле rabbits должно остаться пустым")
        self.assertEqual(result['wolves'], '1', "Поле wolves должно остаться '1'")
        self.assertEqual(result['she_wolves'], '1', "Поле she_wolves должно остаться '1'")
        self.assertEqual(result['steps'], '50', "Поле steps должно остаться '50'")

if __name__ == '__main__':
    unittest.main()