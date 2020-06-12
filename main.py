import scraping

URL = "https://porta.nanzan-u.ac.jp/syllabus/"
SAVE_PATH = "./saved_json/syllabus.json"

if __name__ == "__main__":
    scraping.make_nanzan_syllabus(URL, SAVE_PATH)
