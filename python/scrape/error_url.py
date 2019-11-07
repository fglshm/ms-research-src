"""
    Find the reasons why it can't extract the number of views from some speeches.
"""

import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import time
import csv
import pandas as pd


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


url_path = '/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/url/so_urls.csv'
df = pd.read_csv(url_path, header=None)
ids = df[0]
urls = df[1]

results_df = pd.read_csv('so_scrape_results.csv', header=None)
nan_so_id = results_df.loc[results_df[1].isnull()]

error_urls = []

for id in nan_so_id[0]:
    url = df.loc[df[0] == id][1].values[0]
    error_urls.append([str(id), url])
    data = scrape(id, url)
    data = {idx: value for idx, value in enumerate(data)}
    results_df = results_df.append(data, ignore_index=True)

results_df.to_csv('so_scrape_results.csv', header=None, index=False)
