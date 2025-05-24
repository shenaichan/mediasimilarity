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

'''
dict_keys(['characters', 'medianotes', 'reddeadredemption', 'recap', 'creator', 'usefulnotes', 'standardsnippet', 'pinball', 'derivativeworks', 'justforfun', 'script', 'samuraijack', 'darthwiki'])
'''
'''
Hercules (1997) at Main/Hercules
Ultimate Spider-Man » at Main/UltimateSpiderMan
Gossip Girl at Main/GossipGirl
Iron Man at Main/IronMan
Cube at Main/TheCube
Fallout at Main/Fallout
Twilight at Main/Twilight
'''

currTz = pytz.timezone('America/Los_Angeles')

urlMediaTypes = list(map(lambda x: x[0], mediaCategories))

print(urlMediaTypes)

class Command(BaseCommand):
    
    def handle(self, *args, **options):   

        # Media.objects.exclude(urlMediaType__in=urlMediaTypes).delete()
        
        # mains = Media.objects.filter(urlMediaType="Main")

        # for m in mains:
        #     if m.tropes.count() > 100:
        #         print(m)

        srcType = "main"
        srcTitle = "twilight"
        dstType = "literature"
        dstTitle = "thetwilightsaga"

        src = Media.objects.get(urlMediaType__iexact=srcType, urlSafeTitle__iexact=srcTitle)
        print(src)
        srcTropes = src.tropes.all()
        print(src.tropes.count())
        # src.displayTitle = "Cube (1997)"
        # src.urlMediaType = "Film"
        # src.urlSafeTitle = "Cube1997"
        # src.save()
        # print(src)
        # print(srcTropes)
        dst = Media.objects.get(urlMediaType__iexact=dstType, urlSafeTitle__iexact=dstTitle)
        # dst = Media.objects.create(displayTitle="Cube (1997)", urlMediaType=dstType, urlSafeTitle=dstTitle)
        print(dst)
        print(dst.tropes.count())
        dst.tropes.add(*srcTropes)
        print(dst.tropes.count())
        src.delete()
        
        
        # print([m for m in to_delete])
        # namespaces = dict()

        # medias = Media.objects.all()
        # for media in medias:
        #     mt = media.urlMediaType.lower()
        #     if mt not in urlMediaTypes:
        #         # print(media)
        #         if mt in namespaces:
        #             namespaces[mt].append(media)
        #         else:
        #             namespaces[mt] = [media]

        #         # pass
        # print(namespaces.keys())
        # for key, val in namespaces.items():
        #     for m in val:
        #       # if m.tropes.count() > 100:
        #         print(key, m, m.tropes.count())
        # print(namespaces["main"])
        # print(len(namespaces["main"]))

        '''
        create list of media to delete

        for media in medias
        if this is a media to delete, then continue onto the next media
        get all medias which match "urlsafetitle" and "urlmediatype" case insensitive

        if that number is just one, then continue onto the next media

        otherwise...
        add all future (not this one's id? --> figure out some way to check this) 
        instances to the list of media to delete
        then go through all the medias to delete and add their tropes to 
        the og media's list
        '''

        return

                
