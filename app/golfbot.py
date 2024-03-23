from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime
import configparser
import undetected_chromedriver as uc
import time

driver = uc.Chrome(use_subprocess = True, headless = False)
config = configparser.ConfigParser()
config.read("configs/config.ini")
driver.get(config["GOLFBOT"]["url"])


# wait for human to pass captcha check
WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "dateInput")))


# Attempt to initiate search, if page redirects keep trying to initiate search
retries = 0
max_retries = int(config["GOLFBOT"]["max_retries"])
while(retries < max_retries):
    try:
        retries += 1
        element = driver.find_element(By.ID, "pickerDate")
        
        print("Successfully loaded search results")
        time.sleep(1)
        break
    except NoSuchElementException:
        print(f"Attempting to initialize search. Attempt {retries}/{max_retries}")
        
        # Find the date search box
        search_box = driver.find_element(By.ID, "dateInput")
        time.sleep(0.5)
        search_box.clear()
        time.sleep(0.5)
        
        # Insert desired date
        search_box.send_keys(config["TEETIME"]["date"])
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/ui-view/div/div/div/div[1]/div[2]/div/h2").click()
        time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, "btn-10").click()
        
        # Give app time to either load results or redirect
        time.sleep(2)

driver.find_element(By.LINK_TEXT, "Sign In").click()


# Login to account
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "login")))

username_box = driver.find_element(By.NAME, "login")
username_box.send_keys(config["GOLFBOT"]["username"])

password_box = driver.find_element(By.NAME, "password")
password_box.send_keys(config["GOLFBOT"]["password"])
time.sleep(0.5)
password_box.send_keys(Keys.ENTER)


# Find available tee time within range
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".tee-time-block .time.ng-binding")))

tee_times = driver.find_elements(By.CSS_SELECTOR, ".tee-time-block .time.ng-binding")
start_time = datetime.strptime(config["TEETIME"]["start_time"], "%I:%M %p")
end_time = datetime.strptime(config["TEETIME"]["end_time"], "%I:%M %p")
print(f"Checking for tee time's between {start_time.strftime("%I:%M %p")} and {end_time.strftime("%I:%M %p")}")
for tee_time in tee_times:
    current_time = datetime.strptime(tee_time.text, "%I:%M %p")
    if start_time <= current_time <= end_time:
        print(f"Found tee time at {current_time.strftime("%I:%M %p")}")
        parent = tee_time.find_element(By.XPATH, "./ancestor::li")
        parent.find_element(By.CSS_SELECTOR, "button.primary-btn").click()
        time.sleep(0.5)
        driver.find_element(By.ID, "addToCartBtn").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "buyTeeTime")))
        time.sleep(0.2)
        driver.find_element(By.ID, "buyTeeTime").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "topFinishBtn")))
        time.sleep(0.2)
        if config.getboolean("GOLFBOT", "autobuy"):
            driver.find_element(By.ID, "topFinishBtn").click()
        else:
            time.sleep(10)
        
        break
    


time.sleep(5)
driver.close()
driver.quit()