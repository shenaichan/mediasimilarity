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
    
    def handle(self, *args, **options):   

        to_delete_ids = []

        medias = Media.objects.all()
        for media in medias:
            print(media.id)
            if media.id in to_delete_ids:
                continue

            duplicates = Media.objects.filter(urlSafeTitle__iexact=media.urlSafeTitle, 
                                              urlMediaType__iexact=media.urlMediaType)
            
            if len(duplicates) == 1:
                continue

            # print(duplicates)

            for duplicate in duplicates:
                if duplicate.id != media.id:
                    # print([trope for trope in media.tropes.all()])
                    # print([trope for trope in duplicate.tropes.all()])
                    media.tropes.add(*duplicate.tropes.all())
                    # print([trope for trope in media.tropes.all()])
                    to_delete_ids.append(duplicate.id)
                    # return
        
        Media.objects.filter(id__in=to_delete_ids).delete()

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

                
