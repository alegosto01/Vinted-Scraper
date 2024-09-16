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
import searches as search



# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# #1
# options.binary_location = "/usr/bin/google-chrome-stable"   #change to your location 
# #2
# PATH = r'/home/ale/Downloads/chromedriver-linux64/chromedriver' #change also to your location
# service = webdriver.chrome.service.Service(PATH)
# driver = webdriver.Chrome(service=service, options=options)

def select_new_without_bill(driver):
    
    #click condition list menu
    condition_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='catalog--status-filter--trigger']") 
    driver.execute_script("arguments[0].click();", condition_button)
    
    #click new without bill checkbox
    condition_checkbox = driver.find_element(By.XPATH, "//input[@aria-labelledby='status_ids-list-item-1' and @type='checkbox']")
    driver.execute_script("arguments[0].scrollIntoView();", condition_checkbox)
    driver.execute_script("arguments[0].click();", condition_checkbox)


def select_white(driver):    
    #click white checkbox
    white_checkbox = driver.find_element(By.XPATH, "//input[@aria-labelledby='color_ids-list-item-12' and @type='checkbox']")
    driver.execute_script("arguments[0].scrollIntoView();", white_checkbox)
    driver.execute_script("arguments[0].click();", white_checkbox)

def select_black(driver):    
    #click white checkbox
    white_checkbox = driver.find_element(By.XPATH, "//input[@aria-labelledby='color_ids-list-item-1' and @type='checkbox']")
    driver.execute_script("arguments[0].scrollIntoView();", white_checkbox)
    driver.execute_script("arguments[0].click();", white_checkbox)

def find_brand_ids(driver, filters):
    click_brand_list_menu(driver)
    brand_ids = []
    for filter in filters:
        try:
            parent_element = driver.find_elements(By.XPATH, f"//span[contains(text(), '{filter}')]/ancestor::div[contains(@class, 'web_ui__Cell__content')]")
            
            # print(f"parent length = {len(parent_element)}")
            for element in parent_element:
                # print(element.get_attribute("id"))
                if element.text.split("(")[0] == filter:
                    parent_parent = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'web_ui__Cell__cell web_ui__Cell__default web_ui__Cell__navigating')]")
                    brand_id = parent_parent.get_attribute("id").split("-")[-1]
                    brand_ids.append(brand_id)
        except:
            print("the try failed.")
    return brand_ids


def find_color_ids(color_list):
    color_ids = []
    for color in color_list:
        color_ids.append(search.colori[color])
    return color_ids




def set_price_from(driver, value):
    price_input = driver.find_element(By.ID, "price_from")

    price_input.clear()

    price_input.send_keys(f"{value}")

def set_price_to(driver, value):
    price_input = driver.find_element(By.ID, "price_to")

    price_input.clear()

    price_input.send_keys(f"{value}")
    price_input.send_keys(Keys.ENTER)

def sort_items(driver, sorting):
    checkbox_filtro = driver
    if sorting == "bassoAlto":
        checkbox_filtro = driver.find_element(By.XPATH, "//input[@data-testid='sort-by-list-price_low_to_high--input']")
    
    driver.execute_script("arguments[0].scrollIntoView();", checkbox_filtro)
    driver.execute_script("arguments[0].click();", checkbox_filtro)



    
########## clicking  menus below ##################
def click_color_list_menu(driver):
    #click color list menu
    color_menu_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='catalog--color-filter--trigger']") 
    driver.execute_script("arguments[0].click();", color_menu_button)

def click_sort_list_menu(driver):
    #click color list menu
    sort_menu_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='catalog--sort-filter--trigger']") 
    driver.execute_script("arguments[0].click();", sort_menu_button)


def click_brand_list_menu(driver):
    #click color list menu
    color_menu_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='catalog--brand-filter--trigger']") 
    driver.execute_script("arguments[0].click();", color_menu_button)

def click_price_menu(driver):
    #click color list menu
    print("clickckckckck")

    price_menu_button = driver.find_element(By.XPATH, "//button[@data-testid='catalog--price-filter--trigger']")
    driver.execute_script("arguments[0].click();", price_menu_button)


    

def hellooo():
    print("helloo")



















# def tick_brands(filters, driver):
#     brand_piles = driver.find_elements(By.XPATH, "//div[contains(@id, 'brand_ids-list-item')]")
#     for brand in brand_piles:
#         for filter in filters:
#             try:
#                 # Locate the parent element containing both the span with the text "Nike" and the checkbox
#                 nike_parent_element = driver.find_element(By.XPATH, f"//span[contains(text(), '{filter}')]/ancestor::div[contains(@class, 'web_ui__Cell__content')]")
#                 print(nike_parent_element.text)
#                 parent_parent = nike_parent_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'web_ui__Cell__cell web_ui__Cell__default web_ui__Cell__navigating')]")
#                 # brand_id = parent_parent.get_attribute("id").split("-")[-1]

#                 # print(parent_parent.get_attribute('outerHTML'))
#                 # Find the checkbox within the parent element
#                 nike_checkbox = parent_parent.find_element(By.XPATH, ".//input[@type='checkbox']")

#                 if not nike_checkbox.is_selected():
#                     driver.execute_script("arguments[0].scrollIntoView();", nike_checkbox)
#                     driver.execute_script("arguments[0].click();", nike_checkbox)
#                     print("Nike checkbox clicked successfully.")
#                     break
#             except:
#                 print("the try failed.")