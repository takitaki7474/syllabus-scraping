from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_html(driver):
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_html_attr(tag_list, attr="id"):
    attr_list = []
    for tag in tag_list:
        attr_list.append(tag[attr])
    return attr_list

def switch_to_frame(driver, frame_name):
    driver.switch_to.default_content()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, frame_name)))
    driver.switch_to.frame(driver.find_element_by_name(frame_name))

def click_elem_by_id(driver, elem_id):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, elem_id)))
    driver.find_element_by_id(elem_id).click()

def click_elem_by_xpath(driver, elem_xpath):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, elem_xpath)))
    driver.find_element_by_xpath(elem_xpath).click()
