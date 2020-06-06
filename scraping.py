import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_current_page_html(driver):
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def switch_to_frame(driver, frame_name):
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, frame_name)))
    driver.switch_to.frame(driver.find_element_by_name(frame_name))

def click_elem_id(driver, elem_id):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, elem_id)))
    driver.find_element_by_id(elem_id).click()

# id_list: html内に存在するaタグのidのリスト
# degree_id: テキストが"学部"と"大学院"のaタグのid
def generate_id_list_and_degree_id(soup):
    id_list = []
    degree_id = {}
    a_tag_list = soup.find_all('a')
    for a_tag in a_tag_list:
        a_tag_id = a_tag["id"]
        id_list.append(a_tag_id)
        a_tag_text = a_tag.get_text()
        if a_tag_text == "学部":
            degree_id["Bachelor"] = a_tag_id
        elif a_tag_text == "大学院":
            degree_id["Master_and_Doctor"] = a_tag_id
    return (id_list, degree_id)
