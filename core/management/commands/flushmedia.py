from django.core.management.base import BaseCommand
from core.models import Media
from django.db import connection


class Command(BaseCommand):

    def handle(self, *args, **options):   
        Media.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='core_media';")

