from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import configparser
import undetected_chromedriver as uc
import time

driver = uc.Chrome(use_subprocess=True, headless = False)
config = configparser.ConfigParser()
config.read('configs/config.ini')

driver.get(config['GOLFBOT']['url'])

# wait for human to pass captcha check
element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "dateInput"))
    )

# Attempt to initiate search, if page redirects keep trying to initiate search
retries = 0
max_retries = int(config['GOLFBOT']['max_retries'])
while(retries < max_retries):
    try:
        retries += 1
        element = driver.find_element(By.ID, "pickerDate")
        
        print("Successfully loaded search results")
        time.sleep(3)
        break
    except NoSuchElementException:
        print(f"Attempting to initialize search. Attempt {retries}/{max_retries}")
        
        # Find the date search box
        search_box = driver.find_element(By.ID, "dateInput")
        search_box.clear()
        time.sleep(0.5)
        
        # Insert desired date
        search_box.send_keys("04/06/2024")
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/ui-view/div/div/div/div[1]/div[2]/div/h2").click()
        time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, "btn-10").click()
        
        # Give app time to either load results or redirect
        time.sleep(3)

driver.quit()