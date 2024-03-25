from math import e
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

# Methods
def login():
    driver.find_element(By.LINK_TEXT, "Sign In").click()
    
    username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))
    username_box.send_keys(config["GOLFBOT"]["username"])

    password_box = driver.find_element(By.NAME, "password")
    password_box.send_keys(config["GOLFBOT"]["password"])
    
    time.sleep(0.2)
    password_box.send_keys(Keys.ENTER) 
    
    return True

def buy_tee_time(tee_time):
    parent = tee_time.find_element(By.XPATH, "./ancestor::li")
    parent.find_element(By.CSS_SELECTOR, "button.primary-btn").click()
    
    add_to_cart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "addToCartBtn")))
    time.sleep(0.2)
    add_to_cart.click()
    
    buy_time = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "buyTeeTime")))
    time.sleep(0.3)
    buy_time.click()
    
    finish = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "topFinishBtn")))
    time.sleep(0.3)
    if config.getboolean("GOLFBOT", "autobuy"):
        finish.click()
    else:
        time.sleep(10)    
        
def find_tee_times():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tee-time-block .time.ng-binding")))
        
    tee_times = driver.find_elements(By.CSS_SELECTOR, ".tee-time-block .time.ng-binding")
    start_time = datetime.strptime(config["TEETIME"]["start_time"], "%I:%M %p")
    end_time = datetime.strptime(config["TEETIME"]["end_time"], "%I:%M %p")
    print(f"Checking for tee time's between {start_time.strftime("%I:%M %p")} and {end_time.strftime("%I:%M %p")}")
    for tee_time in tee_times:
        current_time = datetime.strptime(tee_time.text, "%I:%M %p")
        if start_time <= current_time <= end_time:
            print(f"Found tee time at {current_time.strftime("%I:%M %p")}")
            buy_tee_time(tee_time)
            break
    
    return True
       
def attempt_search():
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
     
    # Search
    driver.find_element(By.CLASS_NAME, "btn-10").click()
        
    # Give app time to either load results or redirect
    time.sleep(2)
    
def initiate_search():
    retries = 0
    max_retries = int(config["GOLFBOT"]["max_retries"])
    while(retries < max_retries):
        try:
            retries += 1
            driver.find_element(By.ID, "pickerDate")
            print("Successfully loaded search results")
            time.sleep(1)
            break
        except NoSuchElementException:
            print(f"Attempting to initialize search. Attempt {retries}/{max_retries}")
            attempt_search()
           
def refresh_page_by_player_select():
    dropdown_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "players-button")))
    dropdown_button.click()
    throwaway_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[text()='4']")))
    throwaway_option.click()
    time.sleep(2)
    
def exclude_courses(excluded_courses):
    if "AB" in excluded_courses:
        driver.find_element(By.ID, "courseLabel_Ash Brook GC").click()
        time.sleep(0.5)
    if "GH" in excluded_courses:
        driver.find_element(By.ID, "courseLabel_Galloping Hill GC").click()
        time.sleep(0.5)
    if "LC" in excluded_courses:
        driver.find_element(By.ID, "courseLabel_Galloping Hill GC (Learning Center 9)").click()
        time.sleep(0.5)

# Driver Code
driver = uc.Chrome(use_subprocess = True, headless = False)
config = configparser.ConfigParser()
config.read("configs/config.ini")
driver.get(config["GOLFBOT"]["url"])


# wait for human to pass captcha check
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dateInput")))

# Attempt to initiate search, if page redirects keep trying to initiate search
initiate_search()

# Login to account
login()


WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "tee-time-block")))

excluded_courses = config["TEETIME"]["excluded_courses"].split(",")
exclude_courses(excluded_courses)

max_refreshes = int(config["GOLFBOT"]["max_refreshes"])
for counter in range(max_refreshes):
    if driver.find_element(By.CLASS_NAME, "no-results").is_displayed():
        refresh_page_by_player_select()
    else:
        print("Tee times are live")
        find_tee_times()
        break

time.sleep(30)
driver.close()
driver.quit()