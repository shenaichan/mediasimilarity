from bs4 import BeautifulSoup
import requests
import lxml
from core.models import Trope, Media

numTropePages = 61
# 500 tropes per page.......
tropeIndexBaseUrl = "https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page="


def grab(pageNum: int):
    url = tropeIndexBaseUrl+str(pageNum)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        # print(soup.prettify())
        for row in soup.find_all("td"):
            link = row.find("a")
            print(link.string)
            print(link.href)
        return 0
    else:
        print("Couldn't retrieve page")
        return -1

for i in range(1, numTropePages+1):
    if grab(i) < 0:
        print(f"Failed on page {i}")