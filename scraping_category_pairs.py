import time
from collections import defaultdict
import jaconv #全角半角変換
from selenium import webdriver
from common import operate_html as op
from common import save_dict as sd

URL = "https://porta.nanzan-u.ac.jp/syllabus/"
SAVE_PATH = "./saved_json/CategoryPairs.json"

TOP_CATEGORY_IDs = ["afld1", "afld116"]
PARENT_CATEGORY_IDs = ["afld2", "afld46", "afld65", "afld80", "afld82", "afld84", "afld86", "afld94", "afld99", "afld104", "afld107", "afld111", "afld117", "afld126", "afld129", "afld138", "afld141", "afld150", "afld152", "afld154"]

if __name__=="__main__":
    driver = webdriver.Chrome()
    driver.get(URL)
    op.switch_to_frame(driver, "frame2")
    soup = op.load_html(driver)
    menu_list = soup.find_all("a")
    menu_ids = op.extract_html_attr(menu_list, "id")

    parent = {}
    child = defaultdict(list)
    id_count = -1
    for menu in menu_list:
        if menu["id"] in TOP_CATEGORY_IDs:
            continue
        elif menu["id"] in PARENT_CATEGORY_IDs:
            id_count += 1
            parent[id_count] = jaconv.z2h(menu.get_text() ,digit=True, ascii=True)
        else:
            child[id_count].append(jaconv.z2h(menu.get_text() ,digit=True, ascii=True))

    syllabus_category = []
    category_pairs = {}
    for i in range(len(list(child.keys()))):
        category_pairs["id"] = i
        category_pairs["parentCategory"] = parent[i]
        category_pairs["childCategory"] = child[i]
        syllabus_category.append(category_pairs)
        category_pairs = {}

    if sd.can_save_as_json(SAVE_PATH):
        sd.save_as_json(syllabus_category, SAVE_PATH)

    time.sleep(3)
    driver.quit()
