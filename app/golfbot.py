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
config.read('../configs/congif.ini')

driver.get(config['GOLFBOT']['url'])

element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "dateInput"))
    )

# Find the search box
# search_box = driver.find_element(By.ID, "dateInput")
# time.sleep(1)
# search_box.clear()
# time.sleep(1)

# # Type a search query
# search_box.send_keys("04/06/2024")
# time.sleep(1)
# driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/ui-view/div/div/div/div[1]/div[2]/div/h2").click()
# time.sleep(1)

# # Press Enter
# driver.find_element(By.CLASS_NAME, "btn-10").click()
# # Wait for a few seconds to see the results

# time.sleep(3)

while(True):
    try:
        # Attempt to find the element
        element = driver.find_element(By.ID, "pickerDate")
        print("on next page")
        time.sleep(3)
        break
    except NoSuchElementException:
        print("initiating search")
        # Find the search box
        search_box = driver.find_element(By.ID, "dateInput")
        time.sleep(1)
        search_box.clear()
        time.sleep(1)

        # Type a search query
        search_box.send_keys("04/06/2024")
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/ui-view/div/div/div/div[1]/div[2]/div/h2").click()
        time.sleep()
        driver.find_element(By.CLASS_NAME, "btn-10").click()
        time.sleep(3)

driver.quit()
        


# # Press Enter
# driver.find_element(By.CLASS_NAME, "btn-10").click()

# while(True): pass

# element = WebDriverWait(driver, 60).until(
#         EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'My Account')]"))
#     )

# # Find the search box
# time.sleep(2)
# search_box = driver.find_element(By.ID, "pickerDate")
# search_box.click()


# # Type a search query
# # actions = ActionChains(driver)
# # actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()  # Select all text
# # actions.send_keys("04/06/2024")  # Type the new text to replace it
# # actions.perform()
# time.sleep(3)
# search_box.send_keys("04/06/2024")
# time.sleep(1)
# time.sleep(1)
