from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
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
                    displayName = link.string
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

'''
go to tvtropes
go through all 61 of these
https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page=1
grab each link
go into page, first try to open all folders --> don't have to bc the text is already loaded onto the page lol
get each HTML <a> element and check if the link doesn't involve /Main/ (i.e. it's a media)
also check if links involve the link itself, then it's a subpage, and repeat the process here
get the URL, check if it's in the DB already, and if not, add to the DB
once you've made a list of all media, go to each page and get the actual name
'''        
           
                
