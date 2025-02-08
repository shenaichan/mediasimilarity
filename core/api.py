from .models import Media, Trope
from django.db.models import Count
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class MediaSchema(Schema):
    urlSafeTitle: str
    urlMediaType: str
    displayTitle: str

@api.get("/search", response=list[MediaSchema])
def search(request, q: str):
    medias = Media.objects.filter(displayTitle__icontains=q).annotate(tropeCount=Count('tropes')).filter(tropeCount__gt=10).order_by('-tropeCount')
    print([(med.urlSafeTitle, med.urlMediaType, med.displayTitle, med.tropes.count()) for med in medias])
    # print([trope.id for trope in medias[0].tropes.all()])
    # print([trope.medias.all() for trope in medias[1].tropes.all()])


    # print(med.displayTitle)
    # print(len(med.tropes.all()))
    # tropes = [(trope.displayName, trope.medias.count()) for trope in med.tropes.all()]
    # # tropes.sort(key=lambda x: x[1])
    # print(tropes)
    return medias[:min(len(medias), 20)]