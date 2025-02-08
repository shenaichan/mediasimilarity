from django.core.management.base import BaseCommand
from core.models import Media


class Command(BaseCommand):

    def handle(self, *args, **options): 
        matilda = Media.objects.get(urlSafeTitle="Matilda", urlMediaType="Film")
        print(len(matilda.tropes.all()))
        print([trope.urlSafeName for trope in matilda.tropes.all()])