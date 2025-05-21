# -*- coding: cp1251 -*-

import unittest
import random
import json
import os
from datetime import datetime
from unittest.mock import patch, mock_open, Mock
import uuid
import bottle
from bottle import Bottle, request, response

# Добавление корневой директории проекта в sys.path для корректного импорта модулей
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    # Импорт классов и функций из модуля module3_cells_colonies
    from static.controllers.module3_cells_colonies import GameOfLife, app, JSON_DIR, save_simulation_record, reset_game_state, game as global_game
    from routes import module3_cells_colonies  # Добавлен импорт маршрута
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    raise

class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        # Инициализация объекта GameOfLife с сеткой 5x5 и параметрами a=2, b=3, c=3
        self.game = GameOfLife(5, 5, a=2, b=3, c=3)
        # Сброс глобального состояния перед каждым тестом
        reset_game_state()
        # Ensure global game is accessible
        global global_game

    def tearDown(self):
        # Сброс глобального состояния после каждого теста
        reset_game_state()
        global global_game

    # Тесты для инициализации класса GameOfLife 
    def test_game_of_life_init(self):
        self.assertEqual(self.game.width, 5, "Ширина сетки должна быть 5")
        self.assertEqual(self.game.height, 5, "Высота сетки должна быть 5")
        self.assertEqual(self.game.a, 2, "Параметр a должен быть 2")
        self.assertEqual(self.game.b, 3, "Параметр b должен быть 3")
        self.assertEqual(self.game.c, 3, "Параметр c должен быть 3")
        self.assertEqual(len(self.game.grid), 5, "Длина сетки должна быть 5")
        self.assertEqual(len(self.game.grid[0]), 5, "Ширина сетки должна быть 5")
        self.assertEqual(self.game.current_cell_count, sum(row.count(1) for row in self.game.grid), "Текущие живые клетки должны быть подсчитаны корректно")
    # Тесты для функции toggle_cell Тест убеждается, что клетка меняет состояние корректно и 
    # что повторное переключение возвращает её в исходное состояние.
    def test_toggle_cell(self):
        test_cases = [
            (0, 0, 0, 1),
            (1, 1, 1, 0),
            (2, 2, 0, 1),
            (3, 3, 1, 0),
            (4, 4, 0, 1),
        ]
        for x, y, initial, expected in test_cases:
            self.game.grid[x][y] = initial
            self.game.toggle_cell(x, y)
            self.assertEqual(self.game.grid[x][y], expected, f"Клетка ({x}, {y}) должна быть {expected}")
            self.game.toggle_cell(x, y)
            self.assertEqual(self.game.grid[x][y], initial, f"Клетка ({x}, {y}) должна вернуться к {initial}")

    # Тесты для функции update_cell_count подсчет количества живых клеток
    def test_update_cell_count(self):
        test_cases = [
            ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0),
            ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 9),
            ([[1, 0, 1], [0, 1, 0], [1, 0, 1]], 5),
            ([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 4),
            ([[1, 1, 0], [0, 0, 0], [0, 0, 0]], 2),
        ]
        for grid, expected in test_cases:
            self.game.grid = grid
            self.game.width = len(grid[0])
            self.game.height = len(grid)
            self.game.update_cell_count()
            self.assertEqual(self.game.current_cell_count, expected, f"Должно быть {expected} живых клеток")

    # Тесты для функции to_json
    def test_to_json(self):
        test_cases = [
            (3, 3, 2, 3, 3, [[0, 1, 0], [1, 0, 1], [0, 1, 0]], 3),
            (4, 4, 1, 2, 3, [[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 2),
            (5, 5, 2, 3, 4, [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 3),
            (2, 3, 2, 2, 2, [[1, 0], [0, 1], [1, 0]], 3),
            (6, 6, 3, 4, 3, [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 0, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 7),
        ]
        for width, height, a, b, c, grid, initial_count in test_cases:
            self.game = GameOfLife(width, height, a, b, c)
            self.game.grid = grid
            self.game.initial_cells = [[i, j] for i in range(height) for j in range(width) if grid[i][j] == 1]
            self.game.initial_cell_count = initial_count
            json_data = self.game.to_json()
            self.assertEqual(json_data['width'], width, f"Ширина должна быть {width}")
            self.assertEqual(json_data['height'], height, f"Высота должна быть {height}")
            self.assertEqual(json_data['a'], a, f"Параметр a должен быть {a}")
            self.assertEqual(json_data['b'], b, f"Параметр b должен быть {b}")
            self.assertEqual(json_data['c'], c, f"Параметр c должен быть {c}")
            self.assertEqual(json_data['grid'], grid, "Сетка должна соответствовать входной")
            self.assertEqual(json_data['initial_cell_count'], initial_count, f"Начальное количество клеток должно быть {initial_count}")

    # Тесты для функции save_simulation_record 
    # Тест убеждается, что запись сохраняется с правильными данными, 
    # включая параметры симуляции и временную метку.
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('static.controllers.module3_cells_colonies.datetime')
    def test_save_simulation_record(self, mock_datetime, mock_dump, mock_load, mock_open_file, mock_makedirs):
        mock_datetime.now.return_value = datetime(2025, 5, 21, 11, 5, 0)  # 08:05 AM -03, May 21, 2025
        mock_load.return_value = []
        test_cases = [
            {'record_id': str(uuid.uuid4()), 'width': 3, 'height': 3, 'a': 2, 'b': 3, 'c': 3, 'initial_cell_count': 2},
            {'record_id': str(uuid.uuid4()), 'width': 5, 'height': 5, 'a': 1, 'b': 2, 'c': 3, 'initial_cell_count': 5},
            {'record_id': str(uuid.uuid4()), 'width': 10, 'height': 10, 'a': 2, 'b': 3, 'c': 4, 'initial_cell_count': 20},
            {'record_id': str(uuid.uuid4()), 'width': 4, 'height': 6, 'a': 2, 'b': 2, 'c': 2, 'initial_cell_count': 10},
            {'record_id': str(uuid.uuid4()), 'width': 7, 'height': 7, 'a': 3, 'b': 4, 'c': 3, 'initial_cell_count': 15},
        ]
        for record in test_cases:
            save_simulation_record(record)
            expected_record = {
                'record_id': record['record_id'],
                'width': record['width'],
                'height': record['height'],
                'a': record['a'],
                'b': record['b'],
                'c': record['c'],
                'initial_cell_count': record['initial_cell_count'],
                'datetime': '2025-05-21 11:05:00'
            }
            mock_dump.assert_called()
            written_data = mock_dump.call_args[0][0]
            self.assertIn(expected_record, written_data, "Запись должна быть сохранена с правильными данными")


if __name__ == '__main__':
    unittest.main()