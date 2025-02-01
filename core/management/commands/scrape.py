from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
# import lxml
from core.models import Trope, Media
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
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
                    # print(link.string)
                    # print(link['href'])
                    displayName = link.string.strip()
                    urlSafeName = link['href'].split("/")[-1]
                    Trope.objects.create(urlSafeName=urlSafeName, displayName=displayName)
                return 0
            else:
                print("Couldn't retrieve page")
                return -1

        for i in range(1, numTropePages+1):
            if grab(i) < 0:
                print(f"Failed on page {i}")
            else:
                print(f"Grabbed page {i}")
            time.sleep(0.5)                 
                
                
           
                
