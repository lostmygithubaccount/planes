# imports
import os
import time
import requests

from tqdm import tqdm

import pandas as pd

# setup

# constants
URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
IMG_DIR = "images"
MAX_RPM = 80
MAX_RETRIES = 5

# globals
downloaded = []

# dbt model
def model(dbt, session):

    # dbt config
    dbt.config(materialized="incremental")

    # setup stuff
    os.makedirs(f"{IMG_DIR}", exist_ok=True)

    # get dependent data
    df = dbt.ref("stg_met_objects").df()

    # get list of object ids
    objects = list(df.object_id)

    # setup variables
    rs = 0
    rpm = 0
    idx = 0
    start = time.time()

    # find out the last downloaded object
    imgs = os.listdir(IMG_DIR)
    print(imgs)

    if len(imgs) > 0:
        idx = objects.index(int(sorted(imgs)[-1].split(".")[0])) - 1

    print("hello")
    # for each object
    for obj in tqdm(objects[idx:]):

        rs += 1

        # calculate rpm
        rpm = calculate_rpm(rs, start, time.time())

        while rpm > MAX_RPM:
            rpm = calculate_rpm(rs, start, time.time())

        tqdm.write(f"requests: {rs:07}, obj: {obj:07}, rpm: {rpm:06.02f}")
        r = requests.get(f"{URL}/{obj}")
        rj = r.json()

        # if there's an image
        try:
            if (url := rj["primaryImage"]) != "":
                rs += 1
                tqdm.write(f"primary image found, downloading...")
                img = requests.get(url).content
                ext = get_extension(url)
                with open(f"{IMG_DIR}/{obj:07}.{ext}", "wb") as f:
                    f.write(img)
                downloaded.append(obj)

            if (urls := rj["additionalImages"]) != []:
                for idx, url in enumerate(urls):
                    rs += 1
                    tqdm.write(f"additional image found, downloading...")
                    img = requests.get(url).content
                    ext = get_extension(url)
                    with open(f"{IMG_DIR}/{obj:07}-{idx:02}.{ext}", "wb") as f:
                        f.write(img)
        except:
            pass

    # return model
    return pd.DataFrame(downloaded, columns=["downloaded"])


def calculate_rpm(rss, start, now):
    return (60 * rss) / (now - start)


def get_extension(url):
    return url.split(".")[-1]
