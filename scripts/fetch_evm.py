import concurrent.futures
import re
import sys
import pathlib

import requests
from lxml import etree


BASE_URL = "http://192.168.33.180:8000"
CON_URL = "http://192.168.33.180:8080"
DATASET_PREFIX = "cascaded_dataset"
DOWNLOAD_DIR = f"data/{DATASET_PREFIX}"
DIRNAME_PREFIX = f"{DATASET_PREFIX}-capture_"
DIRNAME_SUFFIX = "-cascaded"


def down(req):
    uri, href, dirname = req
    r = requests.get(uri)
    with open(dirname / href, "wb") as f:
        f.write(r.content)


def download_dir(dirname):
    uri = f"{BASE_URL}/{dirname}"
    curi = f"{CON_URL}/{dirname}"
    r = requests.get(uri)
    root = etree.HTML(r.text)

    print(dirname)
    dirname = DOWNLOAD_DIR / dirname
    dirname.mkdir(parents=True, exist_ok=True)
    down_uris = []
    for a in root.xpath("//a"):
        href = a.get("href")
        down_uris.append((f"{curi}/{href}", href, dirname))

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        for (uri, href, dirname), _ in zip(down_uris, executor.map(down, down_uris)):
            print(href, _)


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
    download_dir(d)

    # store latest case number
    with open("latest_case", "w") as f:
        case_id = int(re.findall(r"\d+", str(d))[0])
        f.write(f"{case_id}")


def range_download(start, end):
    for i in range(start, end):
        d = pathlib.Path(f"cascaded_dataset-capture_{i:05d}-cascaded")
        download_dir(d)


if __name__ == "__main__":
    get_latest()
