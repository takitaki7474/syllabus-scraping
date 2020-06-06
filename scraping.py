import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def switch_to_frame(driver, frame_name):
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, frame_name)))
    driver.switch_to.frame(driver.find_element_by_name(frame_name))

def click_elem_id(driver, elem_id):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, elem_id)))
    driver.find_element_by_id(elem_id).click()
