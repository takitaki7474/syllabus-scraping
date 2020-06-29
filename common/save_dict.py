import os
import json

def save_as_json(dic, savepath):
    with open(savepath, "w") as f:
        json.dump(dic, f, indent=4, ensure_ascii=False)

def can_save_as_json(savepath):
    can_save = True
    if not (".json" in os.path.basename(savepath)):
        print("please save the json format")
        can_save = False
    return can_save
