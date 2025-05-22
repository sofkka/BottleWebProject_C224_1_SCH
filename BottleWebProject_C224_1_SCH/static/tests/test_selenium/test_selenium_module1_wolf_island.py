# -*- coding: cp1251 -*-

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Путь к файлу с тестовыми случаями (абсолютный путь)
TEST_CASES_FILE = r"D:\UP02\BottleWebProject_C224_1_SCH\static\tests\test_selenium\test_module1_wolf_island.json"

# Функция для загрузки тестовых случаев из JSON
def load_test_cases():
    try:
        if not os.path.exists(TEST_CASES_FILE):
            raise FileNotFoundError(f"Test cases file not found: {TEST_CASES_FILE}")
        with open(TEST_CASES_FILE, 'r', encoding='utf-8') as file:
            test_cases = json.load(file)
            if not isinstance(test_cases, list):
                raise ValueError("JSON must be a list of test cases")
            for tc in test_cases:
                required_fields = ['test_id', 'N', 'M', 'rabbits', 'wolves', 'she_wolves', 'steps']
                missing_fields = [field for field in required_fields if field not in tc]
                if missing_fields:
                    raise ValueError(f"Missing required fields {missing_fields} in test case {tc.get('test_id', 'unknown')}")
            return test_cases
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise
    except ValueError as e:
        print(f"JSON data error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while loading file: {e}")
        raise

# Функция для ввода данных тестового случая в поля
def input_test_case_data(driver, test_case):
    driver.find_element(By.ID, "input-n").clear()
    driver.find_element(By.ID, "input-n").send_keys(test_case['N'])
    driver.find_element(By.ID, "input-m").clear()
    driver.find_element(By.ID, "input-m").send_keys(test_case['M'])
    driver.find_element(By.ID, "input-rabbits").clear()
    driver.find_element(By.ID, "input-rabbits").send_keys(test_case['rabbits'])
    driver.find_element(By.ID, "input-wolves").clear()
    driver.find_element(By.ID, "input-wolves").send_keys(test_case['wolves'])
    driver.find_element(By.ID, "input-she-wolves").clear()
    driver.find_element(By.ID, "input-she-wolves").send_keys(test_case['she_wolves'])
    driver.find_element(By.ID, "input-steps").clear()
    driver.find_element(By.ID, "input-steps").send_keys(test_case['steps'])

# Фнукцция для проверка ошибки валидации
def check_validation_error(driver, expected_error):
    try:
        error_message = driver.find_element(By.ID, "error-message").text
        assert expected_error in error_message, f"Expected error '{expected_error}' not found, got '{error_message}'"
        print(f"Validation test successful: {expected_error}")
    except Exception as e:
        print(f"Validation check error: {e}")
        raise

# Основная функция для автоматизации
def run_automation():
    # Создание объекта-драйвера и запуск Edge
    driver = webdriver.Edge()
    driver.maximize_window()

    try:
        # Открытие сайта
        driver.get("http://localhost:443/")

        # Нажатие на кнопку "Death and reproduction" в навигационном меню
        nav_button = driver.find_element(By.XPATH, '//a[@href="/wolf_island" and text()="Death and reproduction"]')
        nav_button.click()

        # Загрузка тестовых случаев
        test_cases = load_test_cases()

        # Установка порядка тестов
        input_test_ids = [
            "invalid_N_too_large",
            "invalid_N_non_integer",
            "invalid_M_too_small",
            "invalid_rabbits_too_large",
            "invalid_wolves_non_integer",
            "invalid_she_wolves_too_large",
            "invalid_steps_too_small",
            "missing_fields",
            "valid_all_fields"
        ]

        # Тестирование всех случаев, связанных с вводом
        for test_id in input_test_ids:
            print(f"\nRunning test: {test_id}")
            test_case = next(tc for tc in test_cases if tc['test_id'] == test_id)

            # Ввод данных
            input_test_case_data(driver, test_case)

            # Прокрутка страницы к кнопке "Start" и нажатие
            start_button = driver.find_element(By.ID, "btn-start")
            driver.execute_script("arguments[0].scrollIntoView(true);", start_button)
            start_button.click()

            # Добавление задержки в 2 секунды после нажатия "Start" для некорректных вводов
            if test_id != "valid_all_fields":
                time.sleep(2)

            # Проверка результата
            if test_case['expected_error']:
                # Проверка наличия ошибки валидации
                check_validation_error(driver, test_case['expected_error'])
            else:
                # Проверка успешного запуска симуляции
                stats = driver.find_element(By.ID, "stats-panel")
                assert 'Simulation step' in stats.text, "Simulation did not start"
                print("Simulation successfully started for valid input")

        # Тестирование остальных случаев
        # Тест "Generate random values"
        test_case = next(tc for tc in test_cases if tc['test_id'] == 'generate_random_values')
        print(f"\nRunning test: {test_case['test_id']}")
        input_test_case_data(driver, test_case)
        generate_button = driver.find_element(By.ID, "btn-generate")
        generate_button.click()

        # Добавление задержки для обновления страницы после генерации случайных значений
        time.sleep(1)  
        # Повторный поиск элементов для предотвращения ошибки
        assert driver.find_element(By.ID, 'input-n').get_attribute('value') != '', "Field N not filled"
        assert driver.find_element(By.ID, 'input-m').get_attribute('value') != '', "Field M not filled"
        assert driver.find_element(By.ID, 'input-rabbits').get_attribute('value') != '', "Field rabbits not filled"
        assert driver.find_element(By.ID, 'input-wolves').get_attribute('value') != '', "Field wolves not filled"
        assert driver.find_element(By.ID, 'input-she-wolves').get_attribute('value') != '', "Field she-wolves not filled"
        assert driver.find_element(By.ID, 'input-steps').get_attribute('value') != '', "Field steps not filled"
        print("Generate random values test successful: fields filled with random values")

        # Тест "Reset simulation"
        test_case = next(tc for tc in test_cases if tc['test_id'] == 'reset_simulation')
        print(f"\nRunning test: {test_case['test_id']}")
        input_test_case_data(driver, test_case)
        reset_button = driver.find_element(By.ID, "btn-reset")
        reset_button.click()
        # Добавление задержки для обновления страницы после сброса
        time.sleep(1)
        # Повторный поиск элементов после сброса для предотвращения ошибки
        assert driver.find_element(By.ID, 'input-n').get_attribute('value') == '15', "Field N not reset"
        assert driver.find_element(By.ID, 'input-m').get_attribute('value') == '15', "Field M not reset"
        assert driver.find_element(By.ID, 'input-rabbits').get_attribute('value') == '', "Field rabbits not reset"
        assert driver.find_element(By.ID, 'input-wolves').get_attribute('value') == '', "Field wolves not reset"
        assert driver.find_element(By.ID, 'input-she-wolves').get_attribute('value') == '', "Field she-wolves not reset"
        assert driver.find_element(By.ID, 'input-steps').get_attribute('value') == '', "Field steps not reset"
        print("Reset simulation test successful: fields reset")

        # Тест "About Wolf Island"
        test_case = next(tc for tc in test_cases if tc['test_id'] == 'about_button')
        print(f"\nRunning test: {test_case['test_id']}")
        input_test_case_data(driver, test_case)
        about_button = driver.find_element(By.ID, "btn-about")
        about_button.click()
        about_section = driver.find_element(By.ID, "about-section")
        assert about_section.is_displayed(), "About Wolf Island section not displayed"
        print("About button test successful: About Wolf Island section displayed")

        # Прокрутка страницы к секции статистики
        stats = driver.find_element(By.ID, "stats-panel")
        driver.execute_script("arguments[0].scrollIntoView(true);", stats)

        print("\nAll actions completed successfully!")

    except Exception as e:
        print(f"Error during execution: {e}")
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    run_automation()
