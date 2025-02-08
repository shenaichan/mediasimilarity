from django.core.management.base import BaseCommand
from core.models import Media


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('search1', type=str)
        parser.add_argument('search2', type=str)

    def handle(self, *args, **options): 

        search1 = options['search1']
        search2 = options['search2']
        med1 = Media.objects.filter(displayTitle__icontains=search1).first()
        med2 = Media.objects.filter(displayTitle__icontains=search2).first()
        print(med1.displayTitle)
        print(med2.displayTitle)
        tropes1 = med1.tropes.all()
        tropes2 = med2.tropes.all()
        overlap = []
        for trope in tropes1:
            if trope in tropes2:
                overlap.append((trope.displayName, trope.medias.count()))
        overlap.sort(key=lambda x: x[1])
        print(overlap)