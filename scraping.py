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

def generate_target_category_syllabus(soup):
    target_category_syllabus = []
    one_subject_syllabus = {}
    tr_tag_list = soup.find_all("tr")
    for tr_tag in tr_tag_list:
        exists_td_tag = (tr_tag.find_all("td", {"class": "list-odd-left"}) != [])
        if not exists_td_tag:
            continue
        td_tag_list = tr_tag.find_all("td", {"class": "list-odd-left"})
        one_subject_syllabus["category"] = td_tag_list[0].get_text()
        one_subject_syllabus["semester"] = td_tag_list[1].get_text()
        one_subject_syllabus["subject_name"] = td_tag_list[2].get_text().replace("\n", "")
        one_subject_syllabus["class_schedule"] = td_tag_list[3].get_text(",").split(",")
        one_subject_syllabus["classroom"] = td_tag_list[4].get_text(",").split(",")
        one_subject_syllabus["teacher"] = td_tag_list[5].get_text().replace("\u3000", " ")
        target_category_syllabus.append(one_subject_syllabus)
        one_subject_syllabus = {}
    print("読込済:  {0}".format(target_category_syllabus[0]["category"]))
    return target_category_syllabus

def scraping_syllabus(url):
    driver = webdriver.Chrome()
    driver.get(url)
    switch_to_frame(driver, "frame2")
    soup = generate_current_page_html(driver)
    id_list, degree_id = generate_id_list_and_degree_id(soup)

    syllabus = {} # 全学科のシラバス
    bachelor_syllabus = [] # 学部のシラバス
    master_and_doctor_syllabus = [] # 大学院のシラバス
    target_syllabus = "Bachelor" # 生成対象のシラバス

    for id in id_list:
        if id == degree_id["Bachelor"]:
            target_syllabus = "Bachelor" # 学部のシラバスが対象
        elif id == degree_id["Master_and_Doctor"]:
            target_syllabus = "Master_and_Doctor" # 大学院のシラバスが対象
        click_elem_id(driver, id)
        switch_to_frame(driver, "public_main")
        time.sleep(5)
        soup = generate_current_page_html(driver)
        exists_table_tag = (soup.find_all("table", {"class": "list"}) != [])
        if exists_table_tag:
            if target_syllabus == "Bachelor":
                bachelor_syllabus += generate_target_category_syllabus(soup)
            elif target_syllabus == "Master_and_Doctor":
                master_and_doctor_syllabus += generate_target_category_syllabus(soup)
        switch_to_frame(driver, "frame2")
    syllabus["Bachelor"] = bachelor_syllabus
    syllabus["Master_and_Doctor"] = master_and_doctor_syllabus
    
