import json
import jaconv
from common import save_dict as sd

def load_syllabus(filepath):
    with open(filepath, "r") as f:
        syllabus = json.load(f)
    return syllabus

if __name__=="__main__":
    loadpath = "./saved_json/syllabus.json"
    savepath = "./saved_json/reformatted_syllabus.json"

    syllabus = load_syllabus(loadpath)
    reformatted_syllabus = []
    reformatted_subject = {}
    id_count = 0
    # Bachelorの処理
    for subject in syllabus["Bachelor"]:
        reformatted_subject["category"] = jaconv.z2h(subject["category"] ,digit=True, ascii=True)
        reformatted_subject["semester"] = jaconv.z2h(subject["semester"] ,digit=True, ascii=True)
        reformatted_subject["subjectName"] = jaconv.z2h(subject["subject_name"] ,digit=True, ascii=True)
        reformatted_subject["teacher"] = jaconv.z2h(subject["teacher"] ,digit=True, ascii=True)
        reformatted_subject["degree"] = "undergraduate"
        if len(subject["class_schedule"]) == len(subject["classroom"]):
            for i in range(len(subject["class_schedule"])):
                class_schedule = jaconv.z2h(subject["class_schedule"][i] ,digit=True, ascii=True)
                reformatted_subject["schedule"] = class_schedule.replace(reformatted_subject["semester"], "")
                reformatted_subject["classroom"] = jaconv.z2h(subject["classroom"][i] ,digit=True, ascii=True)
                reformatted_subject["id"] = id_count
                reformatted_syllabus.append(reformatted_subject.copy())
                id_count += 1
        else:
            print("error")
            break
        reformatted_subject = {}
