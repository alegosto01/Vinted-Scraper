from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import time





def analize_chats(driver):
    driver.get("https://www.vinted.it")
    time.sleep(3)
    try:
        cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie.click()
    except:
        pass    

    #click on login button
    login_btn = driver.find_element(By.XPATH,  "//a[@data-testid='header--login-button']")
    login_btn.click()

    time.sleep(2)


    accedi_btn = driver.find_element(By.XPATH,  "//span[@data-testid='auth-select-type--register-switch']")
    accedi_btn.click()

    time.sleep(2)

    mail_btn = driver.find_element(By.XPATH,  "//span[@data-testid='auth-select-type--login-email']")
    mail_btn.click()


    time.sleep(2)

    mail = "ale.gostoli@gmail.com"
    password = "xhni4sK3$/wf5AS"


    mail_box = driver.find_element(By.XPATH, "//input[@id='username']")
    mail_box.send_keys(mail)

    time.sleep(2)


    password_box = driver.find_element(By.XPATH,  "//input[@id='password']")
    password_box.send_keys(password)
    # password_box.send_keys(Keys.RETURN)   




    




# # Setup WebDriver (make sure to download the appropriate driver)
# driver = webdriver.Chrome()

# # Open the login page
# driver.get('https://example.com/login')

# # Find and fill the login fields
# username = driver.find_element_by_name('username')
# password = driver.find_element_by_name('password')

# username.send_keys('your_username')
# password.send_keys('your_password')

# # Submit the form
# password.send_keys(Keys.RETURN)

# # Now you are logged in, and you can scrape protected content
# driver.get('https://example.com/protected')
# print(driver.page_source)