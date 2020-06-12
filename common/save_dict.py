import os
import json

def save_as_json(dic, filepath):
    with open(filepath, "w") as f:
        json.dump(dic, f)

def can_save_as_json(save_path):
    can_save = True
    if not (".json" in os.path.basename(save_path)):
        print("please save the json format")
        can_save = False
    return can_save
