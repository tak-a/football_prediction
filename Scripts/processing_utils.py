# Created by taka the 2/3/21 at 7:54 PM

import requests
from bs4 import BeautifulSoup


def extract_from_url(url):
    """
    from an url, return the html code
    :param url:
    :return:
    """
    url_text = requests.get(url).text
    return BeautifulSoup(url_text, 'html.parser')
