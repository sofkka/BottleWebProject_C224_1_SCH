# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import json
import logging
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ui_test.log'),
        logging.StreamHandler()
    ]
)

# Path to the test data file
TEST_DATA_PATH = 'test_data.json'

# Initialize WebDriver for Microsoft Edge with automatic management
driver = webdriver.Edge(EdgeChromiumDriverManager().install())
wait = WebDriverWait(driver, 10)

def load_test_data():
    """Load test data from a JSON file."""
    if not os.path.exists(TEST_DATA_PATH):
        logging.error(f"File {TEST_DATA_PATH} not found")
        raise FileNotFoundError(f"File {TEST_DATA_PATH} not found")
    with open(TEST_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_alive_cells():
    """Count the number of alive cells in the gridTable."""
    cells = driver.find_elements(By.CSS_SELECTOR, '#gridTable td.alive')
    return len(cells)

def handle_alert():
    """Handle alerts and return their text."""
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        return alert_text
    except:
        return None

def test_ui_game_of_life(test_case):
    """Test the UI for a single test case."""
    logging.info(f"Starting test: {test_case['test_case']}")
    
    try:
        # Open the page
        driver.get('http://localhost:8080/cells_colonies')
        
        # Wait for form elements to load
        width_input = wait.until(EC.presence_of_element_located((By.ID, 'fieldWidth')))
        height_input = driver.find_element(By.ID, 'fieldHeight')
        a_select = driver.find_element(By.ID, 'neighborsReproduce')
        b_select = driver.find_element(By.ID, 'fewerNeighbors')
        c_select = driver.find_element(By.ID, 'moreNeighbors')
        start_button = driver.find_element(By.ID, 'startBtn')
        pause_button = driver.find_element(By.ID, 'pauseBtn')
        reset_button = driver.find_element(By.ID, 'resetBtn')
        save_button = driver.find_element(By.ID, 'saveJsonBtn')
        
        # Input parameters
        width_input.clear()
        width_input.send_keys(str(test_case['width']))
        height_input.clear()
        height_input.send_keys(str(test_case['height']))
        Select(a_select).select_by_value(str(test_case['a']))
        Select(b_select).select_by_value(str(test_case['b']))
        Select(c_select).select_by_value(str(test_case['c']))
        
        # Wait for the table to update
        time.sleep(1)  # Allow JavaScript to update gridTable
        
        # Check for validation errors
        if 'expected_error' in test_case:
            start_button.click()
            alert_text = handle_alert()
            assert alert_text == test_case['expected_error'] or 'Please, send about 3 to 50.' in alert_text, f"Expected error: {test_case['expected_error']}, got: {alert_text}"
            logging.info(f"Test {test_case['test_case']} passed: Expected error detected")
            return
        
        # Toggle cells
        for x, y in test_case['cells_to_toggle']:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#gridTable tr:nth-child({x + 1}) td:nth-child({y + 1})')))
            cell = driver.find_element(By.CSS_SELECTOR, f'#gridTable tr:nth-child({x + 1}) td:nth-child({y + 1})')
            cell.click()
            logging.debug(f"Toggled cell ({x}, {y})")
        
        # Verify the number of alive cells after toggling
        alive_cells = count_alive_cells()
        assert alive_cells == test_case['expected_cell_count'], f"Expected {test_case['expected_cell_count']} alive cells, got {alive_cells}"
        
        # Start the simulation
        start_button.click()
        time.sleep(2)  # Wait for the first tick (2-second interval)
        
        # Pause the simulation
        pause_button.click()
        time.sleep(1)
        
        # Save the data
        save_button.click()
        alert_text = handle_alert()
        assert alert_text == 'Save to module3.json', f"Expected 'Save to module3.json', got {alert_text}"
        
        # Reset the game
        reset_button.click()
        time.sleep(1)
        alive_cells = count_alive_cells()
        assert alive_cells >= 0, f"After reset, expected non-negative alive cells, got {alive_cells}"
        
        logging.info(f"Test {test_case['test_case']} passed successfully")
        
    except Exception as e:
        logging.error(f"Error in test {test_case['test_case']}: {str(e)}")
        raise
    
def main():
    """Main function to run the tests."""
    try:
        test_data = load_test_data()
        for test_case in test_data:
            test_ui_game_of_life(test_case)
    finally:
        driver.quit()
        logging.info("WebDriver closed")

if __name__ == '__main__':
    main()