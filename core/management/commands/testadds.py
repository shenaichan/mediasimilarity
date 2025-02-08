from django.core.management.base import BaseCommand
from core.models import Media


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('search', type=str)

    def handle(self, *args, **options): 

        search = options['search']
        med = Media.objects.filter(displayTitle__icontains=search).first()
        print(med.displayTitle)
        print(len(med.tropes.all()))
        tropes = [(trope.displayName, trope.medias.count()) for trope in med.tropes.all()]
        tropes.sort(key=lambda x: x[1])
        print(tropes)