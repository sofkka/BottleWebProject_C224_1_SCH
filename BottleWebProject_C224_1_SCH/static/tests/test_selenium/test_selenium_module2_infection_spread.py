# -*- coding: cp1251 -*-

import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация генератора случайных чисел с текущим временем
random.seed(time.time())

# Чтение размеров сетки из JSON
with open('test_module2_infection_spread.json', 'r', encoding='utf-8') as file:
    test_data = json.load(file)
grid_sizes = test_data['grid_sizes']
print(f"Размеры сетки из JSON: {grid_sizes}")
# Выбор случайного размера сетки
grid_size = random.choice(grid_sizes)
print(f"Выбран случайный размер сетки: {grid_size} (индекс: {grid_sizes.index(grid_size)})")

# Открытие браузера Edge и разворачивание на весь экран
driver = webdriver.Edge()
driver.maximize_window()
print("Браузер Edge открыт и развернут на весь экран")

# Переход на главную страницу сайта
driver.get("http://localhost:443/")
print("Перешли на главную страницу: http://localhost:443/")
time.sleep(2)

# Открываем страницу 2 варианта
driver.find_element(By.XPATH, '/html/body/div[1]/div/ul/li[2]/div/a[2]').click()
print("Открыта страница второго варианта (/infection_spread)")
time.sleep(2)

# Тест: Запуск симуляции до завершения с выбранным размером
print(f"Тест: Запуск симуляции до завершения с размером {grid_size}")
slider = driver.find_element(By.ID, "field-size")
driver.execute_script(f"arguments[0].value = {grid_size}; arguments[0].dispatchEvent(new Event('input'));", slider)
print(f"Установлен размер сетки: {grid_size}")
# Проверяем, что значение поля обновилось
field_value = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "field-value"), str(grid_size)))
assert field_value, f"Значение поля не обновилось до {grid_size}"
print(f"Проверка пройдена: Значение поля обновилось до {grid_size}")
time.sleep(2)  # Пауза для визуального контроля
start_button = driver.find_element(By.ID, "start-button")
start_button.click()
print("Нажата кнопка Start")
# Проверяем, что кнопка сменилась на "Stop"
assert start_button.text == "Stop", "Кнопка не сменилась на 'Stop'"
print("Проверка пройдена: Кнопка сменилась на 'Stop'")
time.sleep(5)  # Ждём, чтобы симуляция выполнила несколько шагов
# Первое сохранение в процессе симуляции
save_button = driver.find_element(By.ID, "save-button")
save_button.click()
print("Нажата кнопка Save to JSON (в процессе симуляции)")
# Ждём alert и выводим его в консоль
alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
print(f"Alert сообщение (в процессе): {alert.text}")
assert alert.text == "Data successfully saved to JSON!", "Неверное сообщение об успешном сохранении в процессе"
time.sleep(2)
alert.accept()
time.sleep(2)  # Пауза после первого сохранения
# Ждём завершения симуляции (появления сообщения)
message = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "simulation-message")))
assert "Simulation finished" in message.text, "Сообщение о завершении не отобразилось"
print("Проверка пройдена: Симуляция завершена, сообщение 'Simulation finished' отобразилось")
time.sleep(2)  # Пауза для просмотра результата
# Второе сохранение после завершения симуляции
save_button.click()
print("Нажата кнопка Save to JSON (после завершения)")
# Ждём alert и выводим его в консоль
alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
print(f"Alert сообщение (после завершения): {alert.text}")
assert alert.text == "Data successfully saved to JSON!", "Неверное сообщение об успешном сохранении после завершения"
time.sleep(2)
alert.accept()
time.sleep(2)  # Пауза после второго сохранения

# Пауза перед закрытием для стабильности
print("Завершение тестов, закрытие браузера")
# Закрытие браузера
driver.quit()
print("Браузер закрыт")
