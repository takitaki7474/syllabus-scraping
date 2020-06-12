from common import operate_html as op
from common import save_dict as sd

def note_degree_id(tag_list):
    degree_id = {}
    for tag in tag_list:
        t = tag.get_text()
        if t == "学部":
            degree_id["Bachelor"] = tag["id"]
        elif t == "大学院":
            degree_id["Master_and_Doctor"] = tag["id"]
    return degree_id

def make_current_page_syllabus(soup, page_count):
    current_page_syllabus = []
    subject = {}
    tr_list = soup.find_all("tr")
    for tr in tr_list:
        td_list = tr.find_all("td", {"class": "list-odd-left"})
        exists_td = (td_list != [])
        if not exists_td:
            continue
        subject["category"] = td_list[0].get_text()
        subject["semester"] = td_list[1].get_text()
        subject["subject_name"] = td_list[2].get_text().replace("\n", "").replace(" ", "")
        subject["class_schedule"] = td_list[3].get_text(",").split(",")
        subject["classroom"] = td_list[4].get_text(",").split(",")
        subject["teacher"] = td_list[5].get_text().replace("\u3000", " ")
        current_page_syllabus.append(subject)
        subject = {}
    if len(current_page_syllabus) != 0:
        print("読込済:  {0}  {1}p".format(current_page_syllabus[0]["category"], page_count))
    return current_page_syllabus

def make_all_page_syllabus(driver, menu_ids, degree_id):
    syllabus = {} # 全学科のシラバス
    bachelor_syllabus = [] # 学部のシラバス
    master_and_doctor_syllabus = [] # 大学院のシラバス
    target_syllabus = "Bachelor" # 生成対象のシラバス

    for menu_id in menu_ids:
        if menu_id == degree_id["Bachelor"]:
            target_syllabus = "Bachelor" # 学部のシラバスが対象
        elif menu_id == degree_id["Master_and_Doctor"]:
            target_syllabus = "Master_and_Doctor" # 大学院のシラバスが対象
        op.click_elem_by_id(driver, menu_id)
        op.switch_to_frame(driver, "public_main")
        page_count = 1
        while(1):
            time.sleep(5)
            soup = op.load_html(driver)
            exists_table = (soup.find_all("table", {"class": "list"}) != [])
            exists_next_page = (soup.find_all("a", {"title": "next page"}) != [])
            if exists_table:
                if target_syllabus == "Bachelor":
                    bachelor_syllabus += make_current_page_syllabus(soup, page_count)
                elif target_syllabus == "Master_and_Doctor":
                    master_and_doctor_syllabus += make_current_page_syllabus(soup, page_count)
            if exists_next_page:
                page_count += 1
                op.click_elem_by_xpath(driver, "//a[@title='next page']")
            else:
                break
        op.switch_to_frame(driver, "frame2")
    syllabus["Bachelor"] = bachelor_syllabus
    syllabus["Master_and_Doctor"] = master_and_doctor_syllabus
    return syllabus
