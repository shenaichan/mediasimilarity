from .models import Media, Trope
from django.db.models import Count
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class MediaSchema(Schema):
    urlSafeTitle: str
    urlMediaType: str
    displayTitle: str

class TropeSchema(Schema):
    urlSafeName: str
    displayName: str

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

@api.get("/compare", response=list[TropeSchema])
def search(request, title1: str, type1: str, title2: str, type2: str):
    med1 = Media.objects.filter(urlSafeTitle__iexact=title1, 
                                urlMediaType__iexact=type1).first()
    med2 = Media.objects.filter(urlSafeTitle__iexact=title2, 
                                urlMediaType__iexact=type2).first()
    print(med1.displayTitle)
    print(med2.displayTitle)
    tropes1 = med1.tropes.all()
    tropes2 = med2.tropes.all()
    overlap = []
    for trope in tropes1:
        if trope in tropes2:
            overlap.append((trope, trope.medias.count()))
    overlap.sort(key=lambda x: x[1])
    return list(map(lambda x: x[0], overlap))
    print(overlap)