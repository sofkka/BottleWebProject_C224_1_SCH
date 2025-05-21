# -*- coding: cp1251 -*-

import unittest
import random
import json
import os
import sys
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock

# ���������� �������� ���������� ������� � sys.path ��� ����������� ������� �������
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    # ������ ������� � ������� �� ������ wolf_island
    from static.controllers.module1_wolf_island import (Rabbit, Wolf, SheWolf, get_neighbors, initialize_simulation,
                                                       clean_grid, process_rabbits, process_she_wolves, process_wolves,
                                                       run_simulation_step, prepare_grid_data, save_to_json, wolf_island_controller,
                                                       simulation_state)
except ImportError as e:
    print(f"������ �������: {e}")
    raise

class TestWolfIsland(unittest.TestCase):
    # ����� ��� ������� ��������
    def test_rabbit_init(self):
        # �������� ������� ������� � ������������ (2, 3)
        rabbit = Rabbit(2, 3)
        # �������� ������������� �������
        self.assertEqual(rabbit.x, 2, "���������� x ������� ������ ���� 2")
        self.assertEqual(rabbit.y, 3, "���������� y ������� ������ ���� 3")

    def test_wolf_init(self):
        # �������� ������� ����� � ������������ (1, 4)
        wolf = Wolf(1, 4)
        # �������� ������������� �����
        self.assertEqual(wolf.x, 1, "���������� x ����� ������ ���� 1")
        self.assertEqual(wolf.y, 4, "���������� y ����� ������ ���� 4")
        self.assertEqual(wolf.points, 1.0, "��������� ���� ����� ������ ���� 1.0")

    def test_she_wolf_init(self):
        # �������� ������� ������� � ������������ (0, 5)
        she_wolf = SheWolf(0, 5)
        # �������� ������������� �������
        self.assertEqual(she_wolf.x, 0, "���������� x ������� ������ ���� 0")
        self.assertEqual(she_wolf.y, 5, "���������� y ������� ������ ���� 5")
        self.assertEqual(she_wolf.points, 1.0, "��������� ���� ������� ������ ���� 1.0")

    # ����� ��� ������� get_neighbors
    def test_get_neighbors_center(self):
        # ��������� �������� ������ ��� ����������� ������� (2, 2) � ����� 5x5
        neighbors = get_neighbors(2, 2, 5, 5)
        # ��������� ���������� �������� ������ ������ ����������� �������
        expected = [(1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)]
        # �������� �������� ������ ��� ����������� �������
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� ��� 8 �������� ������ ��� ����������� ������")

    def test_get_neighbors_corner(self):
        # ��������� �������� ������ ��� ������� ������� (0, 0) � ����� 5x5
        neighbors = get_neighbors(0, 0, 5, 5)
        # ��������� ���������� �������� ������ ��� ������� �������
        expected = [(0,1), (1,0), (1,1)]
        # �������� �������� ������ ��� ������� �������
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� 3 �������� ������ ��� ������� ������")

    def test_get_neighbors_edge(self):
        # ��������� �������� ������ ��� ������� �� ������� (1, 0) � ����� 5x5
        neighbors = get_neighbors(1, 0, 5, 5)
        # ��������� ���������� �������� ������ ��� ������� �� �������
        expected = [(0,0), (0,1), (1,1), (2,0), (2,1)]
        # �������� �������� ������ ��� ������� �� �������
        self.assertCountEqual(neighbors, expected, "������ ���� ���������� 5 �������� ������ ��� ������ �� �������")

    # ����� ��� ������� initialize_simulation
    def test_initialize_simulation(self):
        # ������� ��� �������������� ������������� ������, ������������ �������� ������
        def no_shuffle(lst):
            return lst
        
        # ����������� ���������� random.shuffle ��� �������� ���������� ��������
        with patch('random.shuffle') as mock_shuffle:
            # ��������� ��������� mock_shuffle: ������ ������������� ������������ �������� ������
            mock_shuffle.side_effect = no_shuffle
            N, M = 5, 5
            # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
            grid = [[[] for i in range(M)] for i in range(N)]
            # ������������� ��������� � 2 ���������, 1 ������ � 1 ��������
            grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, 2, 1, 1)
            # �������� ������������ ������������� ���������
            self.assertEqual(len(grid), N, "����� ����� ������ ���� ����� N")
            self.assertEqual(len(grid[0]), M, "������ ����� ������ ���� ����� M")
            self.assertEqual(len(rabbits_list), 2, "������ ���� 2 �������")
            self.assertEqual(len(wolves_list), 1, "������ ���� 1 ����")
            self.assertEqual(len(she_wolves_list), 1, "������ ���� 1 �������")
            # ����������� ��������� ������� �������� (2 �������, 1 ����, 1 �������) � ��������� ������ ����� 5x5
            expected_positions = [(4, 4), (4, 3), (4, 2), (4, 1)]
            self.assertEqual((rabbits_list[0].x, rabbits_list[0].y), expected_positions[0], "������ ������ �������� �������")
            self.assertEqual((rabbits_list[1].x, rabbits_list[1].y), expected_positions[1], "������ ������ �������� �������")
            self.assertEqual((wolves_list[0].x, wolves_list[0].y), expected_positions[2], "���� �������� �������")
            self.assertEqual((she_wolves_list[0].x, she_wolves_list[0].y), expected_positions[3], "������� ��������� �������")

    # ����� ��� ������� clean_grid
    def test_clean_grid_rabbit_eaten_by_wolf(self):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # �������� ������� � ����� � ����� ������ (2, 2)
        rabbit = Rabbit(2, 2)
        wolf = Wolf(2, 2)
        grid[2][2] = [rabbit, wolf]
        rabbits_list = [rabbit]
        wolves_list = [wolf]
        she_wolves_list = []
        # ����� ������� ������� ����� ��� ��������� �������������� ��������
        grid, new_rabbits, new_wolves, new_she_wolves = clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
        # �������� ������� ����� ����� �������� ������� ������
        self.assertEqual(len(new_rabbits), 0, "������ ������ ���� ������")
        self.assertEqual(len(new_wolves), 1, "���� ������ ��������")
        self.assertEqual(new_wolves[0].points, 2.0, "���� ����� ������ �����������")
        self.assertEqual(len(grid[2][2]), 1, "� ������ ������ �������� ������ ����")
        self.assertIsInstance(grid[2][2][0], Wolf, "� ������ ������ ���� ����")

    # ����� ��� ������� process_rabbits
    # ����������� ���������� random.random � random.choice ��� �������� ����������� ��������
    @patch('random.random')
    @patch('random.choice')
    def test_process_rabbits_reproduction(self, mock_choice, mock_random):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # �������� ������� � ������ (2, 2)
        rabbit = Rabbit(2, 2)
        grid[2][2] = [rabbit]
        rabbits_list = [rabbit]
        # ��������� ����������� ����������� (0.2 < 0.3, ������ ������ ������������)
        mock_random.side_effect = [0.2]
        # ��������� ������ �������� ������ (2, 3) ��� ����������� �������
        mock_choice.return_value = (2, 3)
        # ����� ������� ��������� �������� ��� �������� �����������
        grid, rabbits_list = process_rabbits(grid, rabbits_list, N, M)
        # �������� ����������� � ����������� ��������
        self.assertEqual(len(rabbits_list), 2, "������ ���� 2 ������� ����� �����������")
        self.assertEqual((rabbits_list[0].x, rabbits_list[0].y), (2, 3), "������ ������ ������ �������������")
        self.assertEqual((rabbits_list[1].x, rabbits_list[1].y), (2, 2), "����� ������ ������ ���� � ������ ������")
        self.assertEqual(len(grid[2][2]), 1, "� ������ ������ ������ ���� ����� ������")
        self.assertEqual(len(grid[2][3]), 1, "� ����� ������ ������ ���� ������ ������")

    # ����� ��� ������� process_she_wolves
    def test_process_she_wolves_eat_rabbit_in_cell(self):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # �������� ������� � ������� � ����� ������ (2, 2)
        rabbit = Rabbit(2, 2)
        she_wolf = SheWolf(2, 2)
        grid[2][2] = [rabbit, she_wolf]
        rabbits_list = [rabbit]
        she_wolves_list = [she_wolf]
        # ����� ������� ��������� ������ ��� �������� �������� �������
        grid, she_wolves_list, rabbits_list = process_she_wolves(grid, she_wolves_list, rabbits_list, N, M)
        # �������� �������� ������� ��������
        self.assertEqual(len(rabbits_list), 0, "������ ������ ���� ������")
        self.assertEqual(len(she_wolves_list), 1, "������� ������ ��������")
        self.assertEqual(she_wolves_list[0].points, 2.0, "���� ������� ������ �����������")
        self.assertEqual(len(grid[2][2]), 1, "� ������ ������ �������� ������ �������")

    # ����� ��� ������� process_wolves
    # ����������� ���������� random.choice ��� �������� ����������� ������
    @patch('random.choice')
    def test_process_wolves_reproduction(self, mock_choice):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # �������� ����� � ������ (2, 2) � ������� � �������� ������ (2, 3)
        wolf = Wolf(2, 2)
        she_wolf = SheWolf(2, 3)
        grid[2][2] = [wolf]
        grid[2][3] = [she_wolf]
        wolves_list = [wolf]
        she_wolves_list = [she_wolf]
        rabbits_list = []
        # ��������� ������������������ ������: ������ ��� �����������, ��� ������ �����, ������ ��� �����������
        mock_choice.side_effect = [(2, 3), 'wolf', (2, 4), (3, 3)]
        # ����� ������� ��������� ������ ��� �������� �����������
        grid, wolves_list, rabbits_list, she_wolves_list = process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M)
        # �������� ����������� ������
        self.assertEqual(len(wolves_list), 2, "������ ��������� ����� ����")
        self.assertEqual(len(she_wolves_list), 1, "������� ������ ��������")
        self.assertEqual(wolves_list[0].points, 0.9, "���� ����� ������ �����������")
        self.assertEqual(she_wolves_list[0].points, 0.9, "���� ������� ������ �����������")
        self.assertEqual((wolves_list[1].x, wolves_list[1].y), (2, 3), "����� ���� ������ ���� � ������ �����������")

    # ����� ��� ������� run_simulation_step
    def test_run_simulation_step(self):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # �������� ������� � ����� � ����� ������ (2, 2)
        rabbit = Rabbit(2, 2)
        wolf = Wolf(2, 2)
        grid[2][2] = [rabbit, wolf]
        rabbits_list = [rabbit]
        wolves_list = [wolf]
        she_wolves_list = []
        # ����������� ���������� ��� �������� �� ������ � ������������ ��������
        with patch('static.controllers.module1_wolf_island.process_wolves', return_value=(grid, wolves_list, rabbits_list, she_wolves_list)) as mock_wolves, \
             patch('static.controllers.module1_wolf_island.process_she_wolves', return_value=(grid, she_wolves_list, rabbits_list)) as mock_she_wolves, \
             patch('static.controllers.module1_wolf_island.process_rabbits', return_value=(grid, rabbits_list)) as mock_rabbits, \
             patch('static.controllers.module1_wolf_island.clean_grid', return_value=(grid, rabbits_list, wolves_list, she_wolves_list)) as mock_clean:
            # ����� ������� ���������� ���� ���������
            result = run_simulation_step(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
            # �������� ���������� ���� ���������
            mock_wolves.assert_called_once()
            mock_she_wolves.assert_called_once()
            mock_rabbits.assert_called_once()
            mock_clean.assert_called_once()
            self.assertEqual(result, (grid, rabbits_list, wolves_list, she_wolves_list), "������� ������ ������� ����������� ������")

    # ����� ��� ������� prepare_grid_data
    def test_prepare_grid_data(self):
        N, M = 5, 5
        # �������� ���������� ������ � ������� �������� ��� ������ ������ �����
        grid = [[[] for i in range(M)] for i in range(N)]
        # ���������� �������� � ������ ������� �����
        grid[0][0] = [Rabbit(0, 0)]
        grid[2][2] = [Wolf(2, 2)]
        grid[4][4] = [SheWolf(4, 4)]
        # ���������� ������ ����� ��� ����������� (������ �������� �� ���� � ������������)
        grid_data = prepare_grid_data(grid, N, M)
        # �������� ���������� ������ �����
        self.assertEqual(grid_data[0][0], '/static/images/rabbit.png', "������ ���� ����������� �������")
        self.assertEqual(grid_data[2][2], '/static/images/wolf.png', "������ ���� ����������� �����")
        self.assertEqual(grid_data[4][4], '/static/images/she_wolf.png', "������ ���� ����������� �������")
        self.assertIsNone(grid_data[0][1], "������ ������ ������ ���� None")

    # ����� ��� ������� save_to_json
    # ����������� ���������� os.makedirs, open, json.load, json.dump � datetime ��� �������� ������ � ����
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_save_to_json(self, mock_datetime, mock_dump, mock_load, mock_open_file, mock_makedirs):
        # ��������� ������� ���� � ������� ��� �����������
        mock_datetime.now.return_value = datetime(2025, 5, 20, 22, 30)
        # ��������� ���������� ������ JSON ����� (������ �������)
        mock_load.return_value = {}
        # �������� ��������� ��������� ��� ����������
        simulation_state = {
            'current_step': 10,
            'rabbits_list': [Rabbit(1, 1)],
            'wolves_list': [Wolf(2, 2)],
            'she_wolves_list': [SheWolf(3, 3)]
        }
        # ������� ��������� ���������
        input_data = {
            'N': '5',
            'M': '5',
            'rabbits': '2',
            'wolves': '1',
            'she_wolves': '1',
            'steps': '10'
        }
        # ����� ������� ���������� ������ � JSON
        success, error = save_to_json(simulation_state, input_data)
        # �������� ���������� ������ � JSON
        self.assertTrue(success, "���������� ������ ���� ��������")
        self.assertEqual(error, '', "�� ������ ���� ������")
        mock_dump.assert_called_once()
        # ��������� ������ ��� ������ � JSON ����
        expected_data = {
            '2025-05-20': [{
                'time': '22:30:00',
                'input_parameters': {'N': 5, 'M': 5, 'rabbits': 2, 'wolves': 1, 'she_wolves': 1, 'steps': 10},
                'simulation_results': {'simulation_step': 10, 'rabbits': 1, 'wolves': 1, 'she_wolves': 1},
                'status': 'Simulation completed successfully'
            }]
        }
        self.assertEqual(mock_dump.call_args[0][0], expected_data, "������ ���� ��������� ���������� ������")

    # ����� ��� ������� wolf_island_controller
    # ����������� ���������� datetime ��� �������� ����
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_wolf_island_controller_reset(self, mock_datetime):
        # ��������� ������� ���� ��� �����������
        mock_datetime.now.return_value = datetime(2025, 5, 20)
        # ����� ������� ����������� � �������� ������
        result = wolf_island_controller('reset', '', '', '', '', '', '')
        # �������� ������ ��������� ���������
        self.assertEqual(result['N'], 15, "N ������ ���� 15")
        self.assertEqual(result['M'], 15, "M ������ ���� 15")
        self.assertEqual(result['stats'], {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0}, "���������� ������ ���� ��������")
        self.assertEqual(simulation_state, {}, "��������� ��������� ������ ���� �������")

    # ����������� ���������� random.randint � datetime ��� �������� ��������� ����������
    @patch('random.randint')
    @patch('static.controllers.module1_wolf_island.datetime')
    def test_wolf_island_controller_generate(self, mock_datetime, mock_randint):
        # ��������� ������� ���� ��� �����������
        mock_datetime.now.return_value = datetime(2025, 5, 20)
        # ��������� ������������������ ��������� ����� ��� ��������� ����������
        mock_randint.side_effect = [5, 5, 2, 1, 1, 20]
        # ����� ������� ����������� � �������� ��������� ����������
        result = wolf_island_controller('generate', '', '', '', '', '', '')
        # �������� ��������� ��������� ����������
        self.assertEqual(result['N'], 5, "N ������ ���� ������������")
        self.assertEqual(result['M'], 5, "M ������ ���� ������������")
        self.assertEqual(result['rabbits'], 2, "������ ���� ������������� 2 �������")
        self.assertEqual(result['wolves'], 1, "������ ���� ������������ 1 ����")
        self.assertEqual(result['she_wolves'], 1, "������ ���� ������������� 1 �������")
        self.assertEqual(result['steps'], 20, "������ ���� ������������� 20 �����")

    # ����� ��������� ������� ������
    def test_wolf_island_controller_invalid_N(self):
        # ����� ������� ����������� � ������������ ��������� N (20 > 15)
        result = wolf_island_controller('start', '20', '5', '2', '1', '1', '50')
        # �������� ������ ��������� N � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of N. Must be an integer from 5 to 15.', "������ ���� ������ ��������� N")
        self.assertEqual(result['N'], 15, "N ������ ���� ������� �� 15")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_N_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� N
        result = wolf_island_controller('start', 'abc', '5', '2', '1', '1', '50')
        # �������� ������ ��������� ���������������� N � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of N. Must be an integer from 5 to 15.', "������ ���� ������ ��������� N")
        self.assertEqual(result['N'], 15, "N ������ ���� ������� �� 15")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_M(self):
        # ����� ������� ����������� � ������������ ��������� M (20 > 15)
        result = wolf_island_controller('start', '5', '20', '2', '1', '1', '50')
        # �������� ������ ��������� M � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of M. Must be an integer from 5 to 15.', "������ ���� ������ ��������� M")
        self.assertEqual(result['M'], 15, "M ������ ���� ������� �� 15")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_M_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� M
        result = wolf_island_controller('start', '5', 'abc', '2', '1', '1', '50')
        # �������� ������ ��������� ���������������� M � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of M. Must be an integer from 5 to 15.', "������ ���� ������ ��������� M")
        self.assertEqual(result['M'], 15, "M ������ ���� ������� �� 15")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_rabbits(self):
        # ����� ������� ����������� � ������������ ��������� rabbits (3 > 2)
        result = wolf_island_controller('start', '5', '5', '3', '1', '1', '50')
        # �������� ������ ��������� rabbits � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of rabbits. Must be an integer from 1 to 2.', "������ ���� ������ ��������� rabbits")
        self.assertEqual(result['rabbits'], '', "���� rabbits ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_rabbits_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� rabbits
        result = wolf_island_controller('start', '5', '5', 'abc', '1', '1', '50')
        # �������� ������ ��������� ���������������� rabbits � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of rabbits. Must be an integer from 1 to 2.', "������ ���� ������ ��������� rabbits")
        self.assertEqual(result['rabbits'], '', "���� rabbits ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_wolves(self):
        # ����� ������� ����������� � ������������ ��������� wolves (3 > 2)
        result = wolf_island_controller('start', '5', '5', '2', '3', '1', '50')
        # �������� ������ ��������� wolves � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of wolves. Must be an integer from 1 to 2.', "������ ���� ������ ��������� wolves")
        self.assertEqual(result['wolves'], '', "���� wolves ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_wolves_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� wolves
        result = wolf_island_controller('start', '5', '5', '2', 'abc', '1', '50')
        # �������� ������ ��������� ���������������� wolves � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of wolves. Must be an integer from 1 to 2.', "������ ���� ������ ��������� wolves")
        self.assertEqual(result['wolves'], '', "���� wolves ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_she_wolves(self):
        # ����� ������� ����������� � ������������ ��������� she_wolves (3 > 2)
        result = wolf_island_controller('start', '5', '5', '2', '1', '3', '50')
        # �������� ������ ��������� she_wolves � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of she-wolves. Must be an integer from 1 to 2.', "������ ���� ������ ��������� she-wolves")
        self.assertEqual(result['she_wolves'], '', "���� she_wolves ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_she_wolves_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� she_wolves
        result = wolf_island_controller('start', '5', '5', '2', '1', 'abc', '50')
        # �������� ������ ��������� ���������������� she_wolves � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of she-wolves. Must be an integer from 1 to 2.', "������ ���� ������ ��������� she-wolves")
        self.assertEqual(result['she_wolves'], '', "���� she_wolves ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

    def test_wolf_island_controller_invalid_steps(self):
        # ����� ������� ����������� � ������������ ��������� steps (5 < 10)
        result = wolf_island_controller('start', '5', '5', '2', '1', '1', '5')
        # �������� ������ ��������� steps � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of steps. Must be an integer from 10 to 240.', "������ ���� ������ ��������� steps")
        self.assertEqual(result['steps'], '', "���� steps ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")

    def test_wolf_island_controller_invalid_steps_non_integer(self):
        # ����� ������� ����������� � ��������������� ��������� steps
        result = wolf_island_controller('start', '5', '5', '2', '1', '1', 'abc')
        # �������� ������ ��������� ���������������� steps � ���������� ��������� �����
        self.assertEqual(result['error'], 'Incorrect value of steps. Must be an integer from 10 to 240.', "������ ���� ������ ��������� steps")
        self.assertEqual(result['steps'], '', "���� steps ������ ���� �������")
        self.assertEqual(result['N'], 5, "N ������ �������� 5")
        self.assertEqual(result['M'], 5, "M ������ �������� 5")
        self.assertEqual(result['rabbits'], '2', "���� rabbits ������ �������� '2'")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")

    def test_wolf_island_controller_missing_fields(self):
        # ����� ������� ����������� � ������ ����� rabbits
        result = wolf_island_controller('start', '5', '5', '', '1', '1', '50')
        # �������� ������ ��-�� ������������� �����
        self.assertEqual(result['error'], 'All fields must be filled to start the simulation.', "������ ���� ������ ��-�� ������������� �����")
        self.assertEqual(result['rabbits'], '', "���� rabbits ������ �������� ������")
        self.assertEqual(result['wolves'], '1', "���� wolves ������ �������� '1'")
        self.assertEqual(result['she_wolves'], '1', "���� she_wolves ������ �������� '1'")
        self.assertEqual(result['steps'], '50', "���� steps ������ �������� '50'")

if __name__ == '__main__':
    unittest.main()