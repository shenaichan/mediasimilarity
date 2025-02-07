from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
import requests
from core.models import Trope, Media, mediaCategories
import time
import re
from enum import Enum



class Command(BaseCommand):

    def handle(self, *args, **options):     

        class LinkType(Enum):
            MEDIA = 0
            SUBPAGE = 1
            NEITHER = 2

        base = "https://tvtropes.org/pmwiki/pmwiki.php/"

        def isMedia(namespace: str) -> bool: 
            # returns true if the namespace the page is under
            # matches any of the designated "media namespace" urls
            return any(category == namespace for category, _ in mediaCategories)
        
        def decode(href: str, tropeName: str) -> tuple[LinkType, str, str]:
            # returns the media type and name if the url is to a piece of media
            # otherwise just returns empty strings
            pattern = r"/pmwiki/pmwiki.php/([^/]+)/([^/]+)"
            match = re.match(pattern, href)
            if match:
                namespace, pageName = match.groups()
                if isMedia(namespace):
                    return LinkType.MEDIA, namespace, pageName
                if namespace == tropeName:
                    return LinkType.SUBPAGE, namespace, pageName
                
            return LinkType.NEITHER, "", ""

        def earlyStop(soup: BeautifulSoup):
            header = soup.find(itemprop="headline")
            if link := header.find(href=True):
                linkType, nameSpace, pageName = decode(link["href"], "")
                if linkType == LinkType.MEDIA:
                    return nameSpace, pageName, link.string

            return "", "", ""
        
        def grab(url: str, trope: Trope):
            # should go into ANY page, so like it should take in a full url actually
            time.sleep(0.25)
            response = requests.get(url)
            subpages, media = [], []
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "lxml")

                nameSpace, pageName, displayName = earlyStop(soup)
                if nameSpace and pageName and displayName:
                    # print("early stop!")
                    media.append((nameSpace, pageName, displayName))
                else:
                    # goes into the "main-article" body and gets everything with the href attribute 
                    # i.e. everything with a link
                    for link in soup.find(id="main-article").find_all(href=True):
                        linkType, nameSpace, pageName = decode(link["href"], trope.urlSafeName)
                        displayName = link.string
                        if displayName:
                            if linkType == LinkType.MEDIA:
                                media.append((nameSpace, pageName, displayName))
                            elif linkType == LinkType.SUBPAGE:
                                subpages.append(nameSpace + "/" + pageName) # make these names more accurate lol
            else:
                print("OOPS!")
            return subpages, media
        
        def insert(trope: Trope, mediaType: str, mediaName: str, displayName: str):
            # if media url exists already, then get it, otherwise make it
            mediaEntry, created = Media.objects.get_or_create(urlSafeTitle=mediaName, urlMediaType=mediaType)
            # if we just made it, add a display title
            # we didn't query on it initially just in case the html element's string
            # was different this time -- would rather err on the side of caution
            # and not accidentally duplicate media entries
            if created:
                mediaEntry.displayTitle = displayName
                mediaEntry.save()
            elif mediaEntry.displayTitle != displayName and not mediaEntry.displayIsDefinitive:
                # print(f"replacing title... old was {mediaEntry.displayTitle} and new might be {displayName}")
                url = base + mediaType + "/" + mediaName
                # print(url)
                time.sleep(0.25)
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "lxml")
                    title = soup.find(itemprop="headline")
                    for desc in title.descendants:
                        # print(desc)
                        if isinstance(desc, NavigableString) and desc.strip():
                            # print(f"new is {desc}")
                            mediaEntry.displayTitle = desc.strip()
                            mediaEntry.displayIsDefinitive = True
                            mediaEntry.save()
                            break

            mediaEntry.tropes.add(trope) # won't duplicate the trope relationship if it's already there
            
        def insertList(media: list[Media], trope: Trope) -> bool:
            for m in media:
                insert(trope, m[0], m[1], m[2]) # make this less ugly...

        
        def bfs(trope: Trope):

            
            seen = set()
            queue = ["Main/" + trope.urlSafeName]

            while queue:
                # print(queue)
                curr = queue[0]
                queue = queue[1:]
                
                print(base + curr)

                subpages, media = grab(base + curr, trope)
                # print(subpages, media)
                insertList(media, trope)
                for subpage in subpages:
                    if subpage not in seen:
                        queue.append(subpage)
                        seen.add(subpage)
                            
            return
            



            
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

        # Media.objects.all().delete()
        # narm = Trope.objects.get(urlSafeName="Narm")
        # print(narm)
        # insert(narm, "music", "stuff", "stuff")
        # music = Media.objects.get(urlSafeTitle="stuff")
        # print([trope for trope in music.tropes.all()] )
        
        for trope in Trope.objects.all():
            bfs(trope)
            print(f"Grabbed trope #{trope.id} {trope.displayName}")
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
           
                
