# -*- coding: cp1251 -*-

import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ������������� ���������� ��������� ����� � ������� ��������
random.seed(time.time())

# ������ �������� ����� �� JSON
with open('test_module2_infection_spread.json', 'r', encoding='utf-8') as file:
    test_data = json.load(file)
grid_sizes = test_data['grid_sizes']
print(f"������� ����� �� JSON: {grid_sizes}")
# ����� ���������� ������� �����
grid_size = random.choice(grid_sizes)
print(f"������ ��������� ������ �����: {grid_size} (������: {grid_sizes.index(grid_size)})")

# �������� �������� Edge � �������������� �� ���� �����
driver = webdriver.Edge()
driver.maximize_window()
print("������� Edge ������ � ��������� �� ���� �����")

# ������� �� ������� �������� �����
driver.get("http://localhost:443/")
print("������� �� ������� ��������: http://localhost:443/")
time.sleep(2)

# ��������� �������� 2 ��������
driver.find_element(By.XPATH, '/html/body/div[1]/div/ul/li[2]/div/a[2]').click()
print("������� �������� ������� �������� (/infection_spread)")
time.sleep(2)

# ����: ������ ��������� �� ���������� � ��������� ��������
print(f"����: ������ ��������� �� ���������� � �������� {grid_size}")
slider = driver.find_element(By.ID, "field-size")
driver.execute_script(f"arguments[0].value = {grid_size}; arguments[0].dispatchEvent(new Event('input'));", slider)
print(f"���������� ������ �����: {grid_size}")
# ���������, ��� �������� ���� ����������
field_value = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "field-value"), str(grid_size)))
assert field_value, f"�������� ���� �� ���������� �� {grid_size}"
print(f"�������� ��������: �������� ���� ���������� �� {grid_size}")
time.sleep(2)  # ����� ��� ����������� ��������
start_button = driver.find_element(By.ID, "start-button")
start_button.click()
print("������ ������ Start")
# ���������, ��� ������ ��������� �� "Stop"
assert start_button.text == "Stop", "������ �� ��������� �� 'Stop'"
print("�������� ��������: ������ ��������� �� 'Stop'")
time.sleep(5)  # ���, ����� ��������� ��������� ��������� �����
# ������ ���������� � �������� ���������
save_button = driver.find_element(By.ID, "save-button")
save_button.click()
print("������ ������ Save to JSON (� �������� ���������)")
# ��� alert � ������� ��� � �������
alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
print(f"Alert ��������� (� ��������): {alert.text}")
assert alert.text == "Data successfully saved to JSON!", "�������� ��������� �� �������� ���������� � ��������"
time.sleep(2)
alert.accept()
time.sleep(2)  # ����� ����� ������� ����������
# ��� ���������� ��������� (��������� ���������)
message = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "simulation-message")))
assert "Simulation finished" in message.text, "��������� � ���������� �� ������������"
print("�������� ��������: ��������� ���������, ��������� 'Simulation finished' ������������")
time.sleep(2)  # ����� ��� ��������� ����������
# ������ ���������� ����� ���������� ���������
save_button.click()
print("������ ������ Save to JSON (����� ����������)")
# ��� alert � ������� ��� � �������
alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
print(f"Alert ��������� (����� ����������): {alert.text}")
assert alert.text == "Data successfully saved to JSON!", "�������� ��������� �� �������� ���������� ����� ����������"
time.sleep(2)
alert.accept()
time.sleep(2)  # ����� ����� ������� ����������

# ����� ����� ��������� ��� ������������
print("���������� ������, �������� ��������")
# �������� ��������
driver.quit()
print("������� ������")
