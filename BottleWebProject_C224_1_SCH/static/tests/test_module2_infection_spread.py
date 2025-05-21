# -*- coding: cp1251 -*-

import unittest
import os
import sys
import json
from datetime import datetime
from unittest.mock import patch, mock_open

# ���������� �������� ���������� ������� � sys.path ��� ����������� ������� �������
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    # ������ ������� �� ������ infection_spread
    from static.controllers.module2_infection_spread import (
        initialize_grid, 
        grid_to_json, 
        is_all_healthy, 
        simulate_step, 
        simulate_all_steps, 
        save_to_json
    )
except ImportError as e:
    print(f"Import error: {e}")
    raise

class TestInfectionSpread(unittest.TestCase):
    # ����� ������ ��� ������������
    def setUp(self):
        self.test_grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'I', 'timer': 3}, {'state': 'R', 'timer': 5}]
        ]
        self.size = 2
        self.step_count = 5
        self.elapsed_steps = 10
        self.test_json_path = 'jsons/result_module2.json'

    def tearDown(self):
        pass  # �� ������� ������� ������

    # ���� 1: �������� ��������� ���������� ������
    @patch('os.makedirs')
    def test_save_to_json_success(self, mock_makedirs):
        """���� ��������� ���������� ������ � JSON"""
        with patch('builtins.open', mock_open()) as mock_file:
            success, message = save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
            
            self.assertTrue(success)
            self.assertEqual(message, 'Saved successfully')
            mock_makedirs.assert_called_once_with(os.path.dirname(self.test_json_path), exist_ok=True)

    # ���� 2: �������� ��������� ������ ��� ����������
    @patch('os.makedirs')
    def test_save_to_json_failure(self, mock_makedirs):
        """���� ��������� ������ ������ � ����"""
        with patch('builtins.open', side_effect=IOError("Disk error")):
            success, message = save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
            
            self.assertFalse(success)
            self.assertIn('Failed to save to JSON', message)
            self.assertIn('Disk error', message)

    # ���� 3: �������� ��������� ����������� ������
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_saved_data_structure(self, mock_makedirs, mock_exists):
        """���� ������������ ��������� ����������� ������"""
        with patch('builtins.open', mock_open()) as mock_file:
            # �������� ����������� �������
            save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
        
            # �������� ��� ������ write
            write_calls = mock_file().write.mock_calls
        
            # ���������� ��� ����� � ���� ������
            written_data = "".join(call.args[0] for call in write_calls)
        
            # ������ JSON ��� �������� ���������
            saved_data = json.loads(written_data)
        
            # ��������� ��������� ������
            current_date = datetime.now().strftime('%Y-%m-%d')
            self.assertIn(current_date, saved_data)
        
            today_data = saved_data[current_date]
            self.assertEqual(len(today_data), 1)
        
            entry = today_data[0]
            self.assertEqual(entry['input_parameters']['grid_size'], self.size)
            self.assertEqual(entry['simulation_results']['healthy_cells'], 2)
            self.assertEqual(entry['simulation_results']['infected_cells'], 1)
            self.assertEqual(entry['simulation_results']['resistant_cells'], 1)
            self.assertEqual(entry['status'], 'Simulation in progress')
        
            # ��������� ��������� grid_state
            grid_state = entry['simulation_results']['grid_state']
            self.assertEqual(len(grid_state), 2)  # 2 ������ � �����
            self.assertEqual(grid_state[0].strip(), "H H")  # ������ ������
            self.assertEqual(grid_state[1].strip(), "I R")  # ������ ������

    # ���� 4: �������� ��������� - ��� ������ �������
    def test_simulation_all_healthy(self):
        """���� ��������� ����� ��� ������ �������"""
        grid = [[{'state': 'H', 'timer': 0} for _ in range(2)] for _ in range(2)]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=2, max_steps=10)
        
        self.assertTrue(all_healthy)
        self.assertGreaterEqual(len(steps), 1)

    # ���� 5: �������� ��������� � ���������
    def test_simulation_with_infection(self):
        """���� ��������� � ����� ���������� �������"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'I', 'timer': 3}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}]
        ]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=3, max_steps=15)
        
        self.assertGreater(len(steps), 1)  # ������ ���� ��������� �����
        self.assertFalse(all_healthy)  # �� ��� ������ �������

    # ���� 6: �������� ������������� �����
    def test_initialize_grid(self):
        """���� ������������ ������������� ����� � ����������� ���������� �������"""
        size = 3
        grid = initialize_grid(size)
        
        self.assertEqual(len(grid), size, "����� ����� ������ ���� ����� size")
        self.assertEqual(len(grid[0]), size, "������ ����� ������ ���� ����� size")
        
        center = size // 2
        self.assertEqual(grid[center][center]['state'], 'I', "����������� ������ ������ ���� ��������")
        self.assertEqual(grid[center][center]['timer'], 0, "������ ����������� ������ ������ ���� 0")
        
        # ���������, ��� ��������� ������ �������
        for i in range(size):
            for j in range(size):
                if i != center or j != center:
                    self.assertEqual(grid[i][j]['state'], 'H', f"������ ({i}, {j}) ������ ���� ��������")
                    self.assertEqual(grid[i][j]['timer'], 0, f"������ ������ ({i}, {j}) ������ ���� 0")

    # ���� 7: �������� ������� grid_to_json
    def test_grid_to_json(self):
        """���� �������������� ����� � JSON-����������� ������"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'I', 'timer': 2}],
            [{'state': 'R', 'timer': 1}, {'state': 'H', 'timer': 0}]
        ]
        json_grid = grid_to_json(grid)
        
        self.assertEqual(len(json_grid), 2, "����� JSON-����� ������ ���� 2")
        self.assertEqual(len(json_grid[0]), 2, "������ JSON-����� ������ ���� 2")
        self.assertEqual(json_grid[0][0], {'state': 'H', 'timer': 0}, "������ ������ ������ ���� {'state': 'H', 'timer': 0}")
        self.assertEqual(json_grid[0][1], {'state': 'I', 'timer': 2}, "������ ������ ������ ������ ������ ���� {'state': 'I', 'timer': 2}")
        self.assertEqual(json_grid[1][0], {'state': 'R', 'timer': 1}, "������ ������ ������ ������ ������ ���� {'state': 'R', 'timer': 1}")
        self.assertEqual(json_grid[1][1], {'state': 'H', 'timer': 0}, "������ ������ ������ ������ ������ ���� {'state': 'H', 'timer': 0}")

    # ���� 8: �������� ������� is_all_healthy
    def test_is_all_healthy(self):
        """���� ��������, �������� �� ��� ������ ���������"""
        # �����, ��� ��� ������ �������
        healthy_grid = [[{'state': 'H', 'timer': 0} for _ in range(2)] for _ in range(2)]
        self.assertTrue(is_all_healthy(healthy_grid, 2), "��� ������ ������ ���� ���������")
        
        # ����� � ����� ���������� �������
        infected_grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'I', 'timer': 3}, {'state': 'H', 'timer': 0}]
        ]
        self.assertFalse(is_all_healthy(infected_grid, 2), "�� ��� ������ ������� ��-�� ����������")

        # ����� � ����� ���������� �������
        resistant_grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'R', 'timer': 1}, {'state': 'H', 'timer': 0}]
        ]
        self.assertFalse(is_all_healthy(resistant_grid, 2), "�� ��� ������ ������� ��-�� ����������")

    # ���� 9: �������� ������ ���� ��������� (��������� �������)
    @patch('random.random')
    def test_simulate_step_infection_spread(self, mock_random):
        """���� ������ ���� ��������� � ���������������� ��������"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'H', 'timer': 0}, {'state': 'I', 'timer': 0}]
        ]
        mock_random.return_value = 0.4  # ����������� ��������� < 0.5, ���������� ��� ������
        new_grid = simulate_step(grid, size=2)
        
        self.assertEqual(new_grid[1][1]['state'], 'I', "���������� ������ ������ �������� ����������")
        self.assertEqual(new_grid[1][1]['timer'], 1, "������ ���������� ������ ������ �����������")
        self.assertEqual(new_grid[0][1]['state'], 'I', "������� ����� ������ ����� ����������")
        self.assertEqual(new_grid[1][0]['state'], 'I', "����� ����� ������ ����� ����������")
        self.assertEqual(new_grid[0][0]['state'], 'H', "��������� ����� ������ �������� ��������")

    # ���� 10: �������� �������� ���������� ������ � ���������� ���������
    def test_simulate_step_infected_to_resistant(self):
        """���� �������� ���������� ������ � ���������� ��������� ����� 6 �����"""
        grid = [[{'state': 'I', 'timer': 6} for _ in range(2)] for _ in range(2)]
        new_grid = simulate_step(grid, size=2)
        
        for i in range(2):
            for j in range(2):
                self.assertEqual(new_grid[i][j]['state'], 'R', f"������ ({i}, {j}) ������ ����� ����������")
                self.assertEqual(new_grid[i][j]['timer'], 0, f"������ ������ ({i}, {j}) ������ ����������")

    # ���� 11: �������� �������� ���������� ������ � �������� ���������
    def test_simulate_step_resistant_to_healthy(self):
        """���� �������� ���������� ������ � �������� ��������� ����� 3 �����"""
        grid = [[{'state': 'R', 'timer': 3} for _ in range(2)] for _ in range(2)]
        new_grid = simulate_step(grid, size=2)
        
        for i in range(2):
            for j in range(2):
                self.assertEqual(new_grid[i][j]['state'], 'H', f"������ ({i}, {j}) ������ ����� ��������")
                self.assertEqual(new_grid[i][j]['timer'], 0, f"������ ������ ({i}, {j}) ������ ����������")

    # ���� 12: �������� ��������� � ������������ ����������� �����
    def test_simulation_max_steps(self):
        """���� ��������� � ����������� ������������� ���������� �����"""
        grid = [[{'state': 'I', 'timer': 0} for _ in range(2)] for _ in range(2)]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=2, max_steps=5)
        
        self.assertEqual(len(steps), 6, "������ ���� 6 ����� (��������� + 5 �����)")
        self.assertFalse(all_healthy, "�� ��� ������ ������� ��-�� ���������")
        for i in range(2):
            for j in range(2):
                self.assertEqual(final_grid[i][j]['timer'], 5, f"������ ������ ({i}, {j}) ������ ���� 5")

    # ���� 13: �������� ���������� � ������ ������
    @patch('os.makedirs')
    def test_save_to_json_empty_grid(self, mock_makedirs):
        """���� ���������� ������ � ������ ������"""
        empty_grid = [[{'state': 'H', 'timer': 0} for _ in range(2)] for _ in range(2)]
        with patch('builtins.open', mock_open()) as mock_file:
            success, message = save_to_json(empty_grid, size=2, step_count=0, elapsed_steps=0)
            
            self.assertTrue(success)
            self.assertEqual(message, 'Saved successfully')
            write_calls = mock_file().write.mock_calls
            written_data = "".join(call.args[0] for call in write_calls)
            saved_data = json.loads(written_data)
            
            current_date = datetime.now().strftime('%Y-%m-%d')
            entry = saved_data[current_date][0]
            self.assertEqual(entry['simulation_results']['healthy_cells'], 4)
            self.assertEqual(entry['simulation_results']['infected_cells'], 0)
            self.assertEqual(entry['simulation_results']['resistant_cells'], 0)
            self.assertEqual(entry['status'], 'Infection eradicated')

if __name__ == '__main__':
    unittest.main()
