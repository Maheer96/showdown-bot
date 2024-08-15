# This file contains all synchronous news-related functions

import requests
from config import NEWS_API
import re

def fetch_news_data():
    response = requests.get(NEWS_API)
    if response.status_code == 200:
        return response.json()
    return {}

# There's issue with HTML literals appearing when calling news, so I am going to remove them
def clean_html(raw_html):
    # Rm HTML tags
    clean_text = re.sub(r'<.*?>', '', raw_html)
    return clean_text

def convert_html_links(raw_html):
    # Convert <a href="URL">text</a> to [text](URL)
    clean_text = re.sub(r'<a href="(.*?)".*?>(.*?)</a>', r'[\2](\1)', raw_html)
    return clean_text