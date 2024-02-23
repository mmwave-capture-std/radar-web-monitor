import requests
from lxml import etree

BASE_URL = "http://192.168.33.180:8000"
CON_URL = "http://192.168.33.180:8080"

def get_latest():
    r = requests.get(BASE_URL)
    root = etree.HTML(r.text)

    urls = []
    for a in root.xpath("//a"):
        href = a.get("href")
        if href.startswith(DIRNAME_PREFIX):
            urls.append(href)

    urls.sort()
    d = pathlib.Path(urls[-1])
    # store latest case number
    with open("latest_case", "w") as f:
        case_id = int(re.findall(r"\d+", str(d))[0])
        f.write(f"{case_id}")


if __name__ == "__main__":
    get_latest()
