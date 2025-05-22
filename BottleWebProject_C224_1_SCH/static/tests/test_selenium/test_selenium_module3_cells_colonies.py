# -*- coding: cp1251 -*-

import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

random.seed(time.time())

with open('test_module3_cells_colonies.json', 'r', encoding='utf-8') as file:
    test_data = json.load(file)
test_case = random.choice(test_data)
print(f"������ ����: {test_case['test_case']}")

driver = webdriver.Edge()
driver.maximize_window()
print("������� Edge �������")

try:
    # 1. ��������� �������� ��������
    driver.get("http://localhost:443/cells_colonies")
    print("������� �������� ������")
    time.sleep(2)

    # 2. ������������� ���������
    width = driver.find_element(By.ID, 'fieldWidth')
    height = driver.find_element(By.ID, 'fieldHeight')
    width.clear()
    width.send_keys(str(test_case['width']))
    height.clear()
    height.send_keys(str(test_case['height']))
    
    Select(driver.find_element(By.ID, 'neighborsReproduce')).select_by_value(str(test_case['a']))
    Select(driver.find_element(By.ID, 'fewerNeighbors')).select_by_value(str(test_case['b']))
    Select(driver.find_element(By.ID, 'moreNeighbors')).select_by_value(str(test_case['c']))
    print("��������� �����������")
    time.sleep(1)

    # 3. ������� �� �������
    for x, y in test_case['cells_to_toggle']:
        cell = driver.find_element(By.CSS_SELECTOR, f'#gridTable tr:nth-child({x+1}) td:nth-child({y+1})')
        cell.click()
        time.sleep(0.2)
    print("������ �������")

    # 4. ������ ���������� (�� ���������)
    driver.find_element(By.ID, 'saveJsonBtn').click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == 'Save to module3.json', "������ ��� ������ ����������"
    alert.accept()
    print("������ ���������� ���������")
    time.sleep(1)

    # 5. ��������� ���������
    driver.find_element(By.ID, 'startBtn').click()
    print("��������� ��������")
    time.sleep(4)

    # 6. ������ ���������� (�� ����� ���������)
    driver.find_element(By.ID, 'saveJsonBtn').click()
    alert = WebDriverWait(driver, 7).until(EC.alert_is_present())
    assert alert.text == 'Save to module3.json', "������ ��� ������ ����������"
    alert.accept()
    print("������ ���������� ���������")
    time.sleep(1)

    print(f"���� '{test_case['test_case']}' ������� �������!")

except Exception as e:
    print(f"������ � �����: {str(e)}")
    raise

finally:
    driver.quit()
    print("������� ������")