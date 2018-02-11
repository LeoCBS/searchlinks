# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def get_links(body):
    soup = BeautifulSoup(body, "html.parser")
    divs_result = soup.find_all(
        'div',
        {'class': 'links_main links_deep result__body'}
    )
    links = []
    for d in divs_result:
        a = d.find('a', {'class': 'result__a'})
        links.append(a['href'])
    return links
