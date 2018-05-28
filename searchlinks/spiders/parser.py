# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def get_links(body):
    soup = BeautifulSoup(body, "html.parser")
    divs_result = soup.find_all(
        'div',
        {'class': 'links_main links_deep result__body'}
    )
    outputs = []
    for d in divs_result:
        print(d.find('a', {'class': 'result__snippet'}))
        a = d.find('a', {'class': 'result__a'})
        outputs.append({'url': a['href']})
    return outputs
