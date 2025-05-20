# -*- coding: cp1251 -*-

import unittest
import random
import json
import os
import sys
from unittest.mock import patch

# Добавление корневой директории проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from static.controllers.module1_wolf_island import (Rabbit, Wolf, SheWolf, get_neighbors, initialize_simulation,
                                                       clean_grid, process_rabbits, process_she_wolves, process_wolves,
                                                       run_simulation_step, prepare_grid_data, save_to_json, wolf_island_controller)
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    raise

class TestWolfIsland(unittest.TestCase):
    # Тесты для классов животных
    def test_rabbit_init(self):
        # Проверка инициализации объекта Rabbit
        rabbit = Rabbit(2, 3)
        self.assertEqual(rabbit.x, 2, "Координата x кролика должна быть 2")
        self.assertEqual(rabbit.y, 3, "Координата y кролика должна быть 3")

    def test_wolf_init(self):
        # Проверка инициализации объекта Wolf
        wolf = Wolf(1, 4)
        self.assertEqual(wolf.x, 1, "Координата x волка должна быть 1")
        self.assertEqual(wolf.y, 4, "Координата y волка должна быть 4")
        self.assertEqual(wolf.points, 1.0, "Начальные очки волка должны быть 1.0")

    def test_she_wolf_init(self):
        # Проверка инициализации объекта SheWolf
        she_wolf = SheWolf(0, 5)
        self.assertEqual(she_wolf.x, 0, "Координата x волчицы должна быть 0")
        self.assertEqual(she_wolf.y, 5, "Координата y волчицы должна быть 5")
        self.assertEqual(she_wolf.points, 1.0, "Начальные очки волчицы должны быть 1.0")

    # Тесты для функции get_neighbors
    def test_get_neighbors_center(self):
        # Проверка соседних клеток для центральной позиции
        neighbors = get_neighbors(1, 1, 3, 3)
        expected = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены все 8 соседей для центральной клетки")

    def test_get_neighbors_corner(self):
        # Проверка соседних клеток для угловой позиции
        neighbors = get_neighbors(0, 0, 3, 3)
        expected = [(0,1), (1,0), (1,1)]
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены 3 соседа для угловой клетки")

    def test_get_neighbors_edge(self):
        # Проверка соседних клеток для позиции на границе
        neighbors = get_neighbors(1, 0, 3, 3)
        expected = [(0,0), (0,1), (1,1), (2,0), (2,1)]
        self.assertCountEqual(neighbors, expected, "Должны быть возвращены 5 соседей для клетки на границе")

if __name__ == '__main__':
    unittest.main()