"""
    This program is to scrape data from TED talk page. The data is the number of views of a speech, the place that the speech was held. Then save it to csv file.
"""

import datetime
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from tqdm import tqdm
import time


def scrape(speech_id, url):
    # get the page from url
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get the number of views
    spans = soup.find_all("span")

    try:
        views = [span.text.replace('views', '').strip()
                 for span in spans if 'views' in span.text]
        views = [view for view in views if view !=
                 ''][0].replace("\"", '').replace(',', '')

        # get the date as timestamp
        scripts = soup.find_all("script")
        scripts = [
            script for script in scripts if "__INITIAL_DATA__" in script.text]
        published = re.findall(
            r"\"published\"\:([0-9]*)", str(scripts[0]), re.IGNORECASE)
        published = [elem for elem in published if elem != ''][0]

        # get the place of speech
        place = re.search("\"event\"\:\"(.*)\"",
                          str(scripts[0])).group(1).split('\",')[0]

        # result data
        data = list(
            map(lambda x: str(x), [speech_id, views, place, published]))

        return data
    except:
        print(spans)
        return [speech_id]


today = datetime.date.today().strftime("%Y%m%d")

speech_types = ['so', 'nso']
for speech_type in speech_types:
    url_csv = f'/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/url/{speech_type}_urls.csv'

    df = pd.read_csv(url_csv, header=None)
    speech_ids = df[0]
    speech_urls = df[1]

    with open(f'/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/view/{speech_type}/{today}.csv', 'w') as f:
        writer = csv.writer(f)
        for id, url in zip(speech_ids, speech_urls):
            data = scrape(id, url)
            print(scrape(id, url))
            writer.writerow(data)
            time.sleep(2)
