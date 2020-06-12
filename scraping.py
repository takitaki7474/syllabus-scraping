
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
