# -*- coding: cp1251 -*-

import unittest
import os
import sys
import json
from datetime import datetime
from unittest.mock import patch, mock_open

# Добавление корневой директории проекта в sys.path для корректного импорта модулей
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    # Импорт функций из модуля infection_spread
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
    # Набор данных для тестирования
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
        pass  # Не удаляем никаких файлов

    # Тест 1: Проверка успешного сохранения данных
    @patch('os.makedirs')
    def test_save_to_json_success(self, mock_makedirs):
        """Тест успешного сохранения данных в JSON"""
        with patch('builtins.open', mock_open()) as mock_file:
            success, message = save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
            
            self.assertTrue(success)
            self.assertEqual(message, 'Saved successfully')
            mock_makedirs.assert_called_once_with(os.path.dirname(self.test_json_path), exist_ok=True)

    # Тест 2: Проверка обработки ошибки при сохранении
    @patch('os.makedirs')
    def test_save_to_json_failure(self, mock_makedirs):
        """Тест обработки ошибки записи в файл"""
        with patch('builtins.open', side_effect=IOError("Disk error")):
            success, message = save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
            
            self.assertFalse(success)
            self.assertIn('Failed to save to JSON', message)
            self.assertIn('Disk error', message)

    # Тест 3: Проверка структуры сохраняемых данных
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_saved_data_structure(self, mock_makedirs, mock_exists):
        """Тест корректности структуры сохраняемых данных"""
        with patch('builtins.open', mock_open()) as mock_file:
            # Вызываем тестируемую функцию
            save_to_json(self.test_grid, self.size, self.step_count, self.elapsed_steps)
        
            # Получаем все вызовы write
            write_calls = mock_file().write.mock_calls
        
            # Объединяем все части в одну строку
            written_data = "".join(call.args[0] for call in write_calls)
        
            # Парсим JSON для проверки структуры
            saved_data = json.loads(written_data)
        
            # Проверяем структуру данных
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
        
            # Проверяем структуру grid_state
            grid_state = entry['simulation_results']['grid_state']
            self.assertEqual(len(grid_state), 2)  # 2 строки в сетке
            self.assertEqual(grid_state[0].strip(), "H H")  # Первая строка
            self.assertEqual(grid_state[1].strip(), "I R")  # Вторая строка

    # Тест 4: Проверка симуляции - все клетки здоровы
    def test_simulation_all_healthy(self):
        """Тест симуляции когда все клетки здоровы"""
        grid = [[{'state': 'H', 'timer': 0} for _ in range(2)] for _ in range(2)]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=2, max_steps=10)
        
        self.assertTrue(all_healthy)
        self.assertGreaterEqual(len(steps), 1)

    # Тест 5: Проверка симуляции с инфекцией
    def test_simulation_with_infection(self):
        """Тест симуляции с одной зараженной клеткой"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'I', 'timer': 3}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}]
        ]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=3, max_steps=15)
        
        self.assertGreater(len(steps), 1)  # Должно быть несколько шагов
        self.assertFalse(all_healthy)  # Не все клетки здоровы

    # Тест 6: Проверка инициализации сетки
    def test_initialize_grid(self):
        """Тест корректности инициализации сетки с центральной зараженной клеткой"""
        size = 3
        grid = initialize_grid(size)
        
        self.assertEqual(len(grid), size, "Длина сетки должна быть равна size")
        self.assertEqual(len(grid[0]), size, "Ширина сетки должна быть равна size")
        
        center = size // 2
        self.assertEqual(grid[center][center]['state'], 'I', "Центральная ячейка должна быть заражена")
        self.assertEqual(grid[center][center]['timer'], 0, "Таймер центральной ячейки должен быть 0")
        
        # Проверяем, что остальные ячейки здоровы
        for i in range(size):
            for j in range(size):
                if i != center or j != center:
                    self.assertEqual(grid[i][j]['state'], 'H', f"Ячейка ({i}, {j}) должна быть здоровой")
                    self.assertEqual(grid[i][j]['timer'], 0, f"Таймер ячейки ({i}, {j}) должен быть 0")

    # Тест 7: Проверка функции grid_to_json
    def test_grid_to_json(self):
        """Тест преобразования сетки в JSON-совместимый формат"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'I', 'timer': 2}],
            [{'state': 'R', 'timer': 1}, {'state': 'H', 'timer': 0}]
        ]
        json_grid = grid_to_json(grid)
        
        self.assertEqual(len(json_grid), 2, "Длина JSON-сетки должна быть 2")
        self.assertEqual(len(json_grid[0]), 2, "Ширина JSON-сетки должна быть 2")
        self.assertEqual(json_grid[0][0], {'state': 'H', 'timer': 0}, "Первая ячейка должна быть {'state': 'H', 'timer': 0}")
        self.assertEqual(json_grid[0][1], {'state': 'I', 'timer': 2}, "Вторая ячейка первой строки должна быть {'state': 'I', 'timer': 2}")
        self.assertEqual(json_grid[1][0], {'state': 'R', 'timer': 1}, "Первая ячейка второй строки должна быть {'state': 'R', 'timer': 1}")
        self.assertEqual(json_grid[1][1], {'state': 'H', 'timer': 0}, "Вторая ячейка второй строки должна быть {'state': 'H', 'timer': 0}")

    # Тест 8: Проверка функции is_all_healthy
    def test_is_all_healthy(self):
        """Тест проверки, являются ли все ячейки здоровыми"""
        # Сетка, где все ячейки здоровы
        healthy_grid = [[{'state': 'H', 'timer': 0} for _ in range(2)] for _ in range(2)]
        self.assertTrue(is_all_healthy(healthy_grid, 2), "Все ячейки должны быть здоровыми")
        
        # Сетка с одной зараженной ячейкой
        infected_grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'I', 'timer': 3}, {'state': 'H', 'timer': 0}]
        ]
        self.assertFalse(is_all_healthy(infected_grid, 2), "Не все ячейки здоровы из-за зараженной")

        # Сетка с одной устойчивой ячейкой
        resistant_grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'R', 'timer': 1}, {'state': 'H', 'timer': 0}]
        ]
        self.assertFalse(is_all_healthy(resistant_grid, 2), "Не все ячейки здоровы из-за устойчивой")

    # Тест 9: Проверка одного шага симуляции (заражение соседей)
    @patch('random.random')
    def test_simulate_step_infection_spread(self, mock_random):
        """Тест одного шага симуляции с распространением инфекции"""
        grid = [
            [{'state': 'H', 'timer': 0}, {'state': 'H', 'timer': 0}],
            [{'state': 'H', 'timer': 0}, {'state': 'I', 'timer': 0}]
        ]
        mock_random.return_value = 0.4  # Вероятность заражения < 0.5, заражаются все соседи
        new_grid = simulate_step(grid, size=2)
        
        self.assertEqual(new_grid[1][1]['state'], 'I', "Зараженная ячейка должна остаться зараженной")
        self.assertEqual(new_grid[1][1]['timer'], 1, "Таймер зараженной ячейки должен увеличиться")
        self.assertEqual(new_grid[0][1]['state'], 'I', "Верхний сосед должен стать зараженным")
        self.assertEqual(new_grid[1][0]['state'], 'I', "Левый сосед должен стать зараженным")
        self.assertEqual(new_grid[0][0]['state'], 'H', "Косвенный сосед должен остаться здоровым")

    # Тест 10: Проверка перехода зараженной ячейки в устойчивое состояние
    def test_simulate_step_infected_to_resistant(self):
        """Тест перехода зараженной ячейки в устойчивое состояние после 6 шагов"""
        grid = [[{'state': 'I', 'timer': 6} for _ in range(2)] for _ in range(2)]
        new_grid = simulate_step(grid, size=2)
        
        for i in range(2):
            for j in range(2):
                self.assertEqual(new_grid[i][j]['state'], 'R', f"Ячейка ({i}, {j}) должна стать устойчивой")
                self.assertEqual(new_grid[i][j]['timer'], 0, f"Таймер ячейки ({i}, {j}) должен сброситься")

    # Тест 11: Проверка перехода устойчивой ячейки в здоровое состояние
    def test_simulate_step_resistant_to_healthy(self):
        """Тест перехода устойчивой ячейки в здоровое состояние после 3 шагов"""
        grid = [[{'state': 'R', 'timer': 3} for _ in range(2)] for _ in range(2)]
        new_grid = simulate_step(grid, size=2)
        
        for i in range(2):
            for j in range(2):
                self.assertEqual(new_grid[i][j]['state'], 'H', f"Ячейка ({i}, {j}) должна стать здоровой")
                self.assertEqual(new_grid[i][j]['timer'], 0, f"Таймер ячейки ({i}, {j}) должен сброситься")

    # Тест 12: Проверка симуляции с максимальным количеством шагов
    def test_simulation_max_steps(self):
        """Тест симуляции с достижением максимального количества шагов"""
        grid = [[{'state': 'I', 'timer': 0} for _ in range(2)] for _ in range(2)]
        steps, final_grid, all_healthy = simulate_all_steps(grid, size=2, max_steps=5)
        
        self.assertEqual(len(steps), 6, "Должно быть 6 шагов (начальный + 5 шагов)")
        self.assertFalse(all_healthy, "Не все ячейки здоровы из-за заражённых")
        for i in range(2):
            for j in range(2):
                self.assertEqual(final_grid[i][j]['timer'], 5, f"Таймер ячейки ({i}, {j}) должен быть 5")

    # Тест 13: Проверка сохранения с пустой сеткой
    @patch('os.makedirs')
    def test_save_to_json_empty_grid(self, mock_makedirs):
        """Тест сохранения данных с пустой сеткой"""
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
