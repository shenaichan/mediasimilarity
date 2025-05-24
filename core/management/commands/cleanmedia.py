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

base = "https://tvtropes.org/pmwiki/pmwiki.php/"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('startingMedia', type=int)
    
    def handle(self, *args, **options):  

        startingMedia = options['startingMedia']  

        lastTime = [time.time() - 100]

        def maybeWait():
            currTime = time.time()
            timeElapsed = currTime - lastTime[0]
            if timeElapsed < 0.25:
                time.sleep(0.25 - timeElapsed)
            lastTime[0] = time.time()
            return 

        to_delete_ids = []

        medias = Media.objects.filter(id__gte=startingMedia).order_by('id')
        try:
            for media in medias:
                print(media.id)
                url = base + media.urlMediaType + "/" + media.urlSafeTitle
                # maybeWait()
                response = requests.get(url)

                if response.status_code != 200:
                    print(response.status_code)
                    if response.status_code == 404:
                        to_delete_ids.append(media.id)
                        print(f"deleted {media.displayTitle}")
                        continue
                    # 403 is access denied because i spammed too hard!
                    elif response.status_code == 403:
                        print("i got rate limited...")
                        while response.status_code != 200:
                            print("waiting...")
                            time.sleep(60)
                            response = requests.get(url)
                    

                if response.url != url:
                    print(response.url, url)
                    # don't count the "?" i.e. the "?from=..."
                    pattern = r"https://tvtropes.org/pmwiki/pmwiki.php/([^/]+)/([^/?#]+)"
                    match = re.match(pattern, response.url)

                    if not match:
                        print("what???")
                        break
                    
                    mediaType, mediaName = match.groups()

                    url_is_present = Media.objects.filter(urlSafeTitle__iexact=mediaName, 
                                                        urlMediaType__iexact=mediaType)
                    
                    if len(url_is_present) > 1:
                        print("why are there multiple???")
                        break
                    
                    if len(url_is_present) == 1:
                        print(url_is_present[0], media)
                        url_is_present[0].tropes.add(*media.tropes.all())
                        to_delete_ids.append(media.id)
                        continue
                    else:
                        print(mediaType, mediaName)
                        media.urlMediaType = mediaType
                        media.urlSafeTitle = mediaName
                        media.save()
                
                if not media.displayIsDefinitive:
                    soup = BeautifulSoup(response.content, "lxml")
                    title = soup.find(itemprop="headline")
                    for desc in title.descendants:
                        # print(desc)
                        if isinstance(desc, NavigableString) and desc.strip():
                            print(f"new is {desc}")
                            media.displayTitle = desc.strip()
                            media.displayIsDefinitive = True
                            media.save()
                            break
        except KeyboardInterrupt:
            print("Control C'ing out of this bitch")
            print(to_delete_ids)
            Media.objects.filter(id__in=to_delete_ids).delete()

        Media.objects.filter(id__in=to_delete_ids).delete()


        '''
        ids_to_delete = []
        for media in medias:
            go to the page and follow redirects
            if it's bad, then add it to the list of media to delete
            and then continue

            if the page redirects:

                if the redirect takes you to a url that's in the database
                    then take the current media's tropes
                    and add it to the og media's tropes
                    then add it to the list of media to delete
                    and then continue
                else
                    just rename the url
            
            if the media's display title hasn't been checked:
                check and update it
                set display title to be checked
        abort that thang
        '''

        return

                
