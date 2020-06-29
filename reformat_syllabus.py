import json
import jaconv
from common import save_dict as sd

def load_syllabus(filepath):
    with open(filepath, "r") as f:
        syllabus = json.load(f)
    return syllabus

if __name__=="__main__":

    reformatted_syllabus = []
    reformatted_subject = {}
    id_count = 0
