from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
import requests
from core.models import Trope, Media, mediaCategories
import time
import re
from enum import Enum
from datetime import datetime
import pytz
from termcolor import colored


currTz = pytz.timezone('America/Los_Angeles')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('startingMedia', type=int)

    def handle(self, *args, **options):   

        startingMedia = options['startingMedia']  

        lastTime = [time.time() - 100]

        class LinkType(Enum):
            MEDIA = 0
            SUBPAGE = 1
            NEITHER = 2

        base = "https://tvtropes.org/pmwiki/pmwiki.php/"

        def maybeWait():
            currTime = time.time()
            timeElapsed = currTime - lastTime[0]
            if timeElapsed < 0.2:
                time.sleep(0.2 - timeElapsed)
            lastTime[0] = time.time()
            return


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
            # time.sleep(0.5)
            maybeWait()
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
                print(url)
                # time.sleep(0.5)
                maybeWait()
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
                else:
                    print("OOPS!")

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
            

        # tropes = Trope.objects.all()[startingMedia - 1:]
        # for trope in tropes:
        #     startTime = time.time()
        #     bfs(trope)
        #     endTime = time.time()
        #     elapsedTime = endTime - startTime
        #     currTime = datetime.now(currTz).strftime('%m-%d %H:%M:%S')
        #     print(colored(f"[{currTime}] Grabbed trope #{trope.id} {trope.displayName} in {elapsedTime:.4f} seconds", "red"))

        for i in range(100):
            currTime = time.time()
            # if i % 5 == 0:
            #     time.sleep(0.5)
            maybeWait()
            print("heyyy")
            print(time.time() - currTime)
   
                
