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
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import time
import general_functions as gen_func
import Scraper

import requests



def log_in(driver):

    driver.get("https://www.vinted.it/")
    time.sleep(5)
    try:
        cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        driver.execute_script("arguments[0].scrollIntoView();", cookie)
        driver.execute_script("arguments[0].click();", cookie)
        # cookie.click()
    except:
        pass    

    #click on login button
    login_btn = driver.find_element(By.XPATH,  "//a[@data-testid='header--login-button']")
    driver.execute_script("arguments[0].scrollIntoView();", login_btn)
    driver.execute_script("arguments[0].click();", login_btn)
    # login_btn.click()

    time.sleep(5)


    accedi_btn = driver.find_element(By.XPATH,  "//span[@data-testid='auth-select-type--register-switch']")
    driver.execute_script("arguments[0].scrollIntoView();", accedi_btn)
    driver.execute_script("arguments[0].click();", accedi_btn)
    # accedi_btn.click()

    time.sleep(5)

    mail_btn = driver.find_element(By.XPATH,  "//span[@data-testid='auth-select-type--login-email']")
    driver.execute_script("arguments[0].scrollIntoView();", mail_btn)
    driver.execute_script("arguments[0].click();", mail_btn) 
    # mail_btn.click()


    time.sleep(5)

    mail = "ale.gostoli@gmail.com"
    password = "xhni4sK3$/wf5AS"


    mail_box = driver.find_element(By.XPATH, "//input[@id='username']")
    mail_box.send_keys(mail)

    time.sleep(5)


    password_box = driver.find_element(By.XPATH,  "//input[@id='password']")
    password_box.send_keys(password)
    password_box.send_keys(Keys.RETURN)   



def process_chats(driver):
    driver.get("")
    time.sleep(3)
    try:
        cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie.click()
    except:
        pass    

    #raccogli tutti i div clickabili nella pagina e clickali uno ad uno
    list_chats = driver.find_elements(By.XPATH, "//div[@class='web_ui__Cell__cell web_ui__Cell__default web_ui__Cell__navigating']")
    for chat in list_chats:
        action = ActionChains(driver)
        action.move_to_element(chat).perform()

        # Click the div to open the chat
        chat.click()



        #capisci che chat c'è

        #offerta da qualcuno
        try:
            decline_btn = driver.find_element(By.XPATH, "//button[@data-testid='offer-message-decline-button']")    
            driver.execute_script("arguments[0].scrollIntoView();", decline_btn)
            driver.execute_script("arguments[0].click();", decline_btn)

            
            gen_func.random_sleep(3,5)
            delete_chat(driver)
            gen_func.random_sleep(3,5)
        except:
            pass
            
        try:
            decline_btn = driver.find_element(By.XPATH, "//button[@data-testid='offer-message-decline-button']")    
            driver.execute_script("arguments[0].scrollIntoView();", decline_btn)
            driver.execute_script("arguments[0].click();", decline_btn)
        except:
            pass



def make_offer(driver, url, offer):
    #non provata. non so cosa succede dopo che ha cliccato make an offer la seconda volta per submittarla
    driver.get(url)
    gen_func.random_sleep(2,4)
    make_offer_btn = driver.find_element(By.XPATH, "//button[@data-testid='item-buyer-offer-button']")
    make_offer_btn.click()

    gen_func.random_sleep(2,4)

    offer_price_box = driver.find_element(By.XPATH, "//input[@data-testid='offer-price-field']")
    offer_price_box.send_keys(offer)

    gen_func.random_sleep(2,4)

    
    submit_offer_btn = driver.find_element(By.XPATH, "//button[@data-testid='offer-submit-button']")
    submit_offer_btn.click()


def delete_chat(driver):
    info_btn = driver.find_element(By.XPATH, "//button[@data-testid='details-button']")
    info_btn.click()

    gen_func.random_sleep(1,3)
    delete_chat_div = driver.find_element(By.XPATH, "//div[@data-testid='conversation-actions-delete']")
    delete_chat_div.click()

    gen_func.random_sleep(1,3)
    
    confirm_delete_btn = driver.find_element(By.XPATH, "//button[@class='web_ui__Button__button web_ui__Button__filled web_ui__Button__default web_ui__Button__warning web_ui__Button__truncated']")
    confirm_delete_btn.click()



# driver = webdriver.Chrome()

# log_in(driver)

# input("something")
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