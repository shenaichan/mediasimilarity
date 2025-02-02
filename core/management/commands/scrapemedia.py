from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from core.models import Trope, Media, mediaCategories
import time
import re

class Command(BaseCommand):

    def handle(self, *args, **options):     

        tropePageBaseUrl = "https://tvtropes.org/pmwiki/pmwiki.php/Main/"

        def isMedia(namespace: str):
            # returns true if the namespace the page is under
            # matches any of the designated "media namespace" urls
            return any(category == namespace for category, _ in mediaCategories)
        
        def decompose(href: str):
            # returns the media type and name if the url is to a piece of media
            # otherwise just returns empty strings
            pattern = r"/pmwiki/pmwiki.php/([^/]+)/([^/]+)"
            match = re.match(pattern, href)
            if match:
                namespace, mediaName = match.groups()
                if isMedia(namespace):
                    return namespace, mediaName
            return "", ""

        def grab(pageName: str):
            url = tropePageBaseUrl + pageName
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "lxml")
                # goes into the "main-article" body and gets everything with the href attribute 
                # i.e. everything with a link
                for link in soup.find(id="main-article").find_all(href=True):
                    mediaType, mediaName = decompose(link["href"])
                    displayName = link.string
                    if mediaType and mediaName and displayName:
                        print(mediaType, mediaName, displayName)
                        # Media.objects.create(urlSafeTitle=mediaName, 
                        #                      urlMediaType=mediaType, 
                        #                      displayTitle=displayName)
                        
                return 0
            else:
                return -1
        
        def bfs(pageName: str):
            # should, given a trope's main page
            # search all its subpages and get the media connected to each of those
            # i think it should put the media into the database as it goes
            # some stopping conditions are like
            # if there's a piece of media in the header, then it's just a trope page
            # specifically for that piece of media
            # also if the trope page doesn't have any more subpages, i.e.
            # links of the form /pmwiki/pmwiki.php/{tropeName}/{foo}
            # yeah, so then we stop and return out
            # once we do that, we go onto the next like... page in our queue
            # also remember to push pages to explore to the queue, don't want to go all the way in
            # we're done when the queue is empty
            # so on each page we're looking for trope subpages (these are our "children")
            # and for media links (this is our "node content")
            # so maybe we just want a function that's like grab but it returns like
            # two lists: a list of subpages (children), and a list of media pages (content)
            
            
            return

        if grab("Narm") < 0:
            print(f"Something went wrong on trope")
        else:
            print(f"Grabbed trope")
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
           
                
