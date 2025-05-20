# -*- coding: cp1251 -*-

import unittest
import random
import json
import os
import sys
from unittest.mock import patch

# ���������� �������� ���������� ������� � sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from static.controllers.module1_wolf_island import (Rabbit, Wolf, SheWolf, get_neighbors, initialize_simulation,
                                                       clean_grid, process_rabbits, process_she_wolves, process_wolves,
                                                       run_simulation_step, prepare_grid_data, save_to_json, wolf_island_controller)
except ImportError as e:
    print(f"������ �������: {e}")
    raise

class TestWolfIsland(unittest.TestCase):
    # ����� ��� ������� ��������
    def test_rabbit_init(self):
        # �������� ������������� ������� Rabbit
        rabbit = Rabbit(2, 3)
        self.assertEqual(rabbit.x, 2, "���������� x ������� ������ ���� 2")
        self.assertEqual(rabbit.y, 3, "���������� y ������� ������ ���� 3")

    def test_wolf_init(self):
        # �������� ������������� ������� Wolf
        wolf = Wolf(1, 4)
        self.assertEqual(wolf.x, 1, "���������� x ����� ������ ���� 1")
        self.assertEqual(wolf.y, 4, "���������� y ����� ������ ���� 4")
        self.assertEqual(wolf.points, 1.0, "��������� ���� ����� ������ ���� 1.0")

    def test_she_wolf_init(self):
        # �������� ������������� ������� SheWolf
        she_wolf = SheWolf(0, 5)
        self.assertEqual(she_wolf.x, 0, "���������� x ������� ������ ���� 0")
        self.assertEqual(she_wolf.y, 5, "���������� y ������� ������ ���� 5")
        self.assertEqual(she_wolf.points, 1.0, "��������� ���� ������� ������ ���� 1.0")

    # ����� ��� ������� get_neighbors
    def test_get_neighbors_center(self):
        # �������� �������� ������ ��� ����������� �������
        neighbors = get_neighbors(1, 1, 3, 3)
        expected = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� ��� 8 ������� ��� ����������� ������")

    def test_get_neighbors_corner(self):
        # �������� �������� ������ ��� ������� �������
        neighbors = get_neighbors(0, 0, 3, 3)
        expected = [(0,1), (1,0), (1,1)]
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� 3 ������ ��� ������� ������")

    def test_get_neighbors_edge(self):
        # �������� �������� ������ ��� ������� �� �������
        neighbors = get_neighbors(1, 0, 3, 3)
        expected = [(0,0), (0,1), (1,1), (2,0), (2,1)]
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� 5 ������� ��� ������ �� �������")

if __name__ == '__main__':
    unittest.main()