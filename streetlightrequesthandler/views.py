import json
from django.http.response import HttpResponse
from streetlightrequesthandler.models import StreetLight

# Create your views here.
def store_data_from_streetlight(request):
    if request.method=='GET':
        payload=request.GET
        streetlightrecord = StreetLight(ID=payload.get('ID'), BV=payload.get('BV'),BI=payload.get('BI'),SV=payload.get('SV'),SI=payload.get('SI'),LV=payload.get('LV'),LI=payload.get('LI'),BA=payload.get('BA'),STATE=payload.get('STATE'),LAT=payload.get('LAT'),LON=payload.get('LON'),DRY_BIN=payload.get('DRY_BIN'),WET_BIN=payload.get('WET_BIN'))
        streetlightrecord.save()
        responses=json.dumps([{'Message' : 'Success'}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')

def get_all_data(request):
    if request.method=='GET':
        streetlights=[]
        for streetlight in StreetLight.objects.all():
            streetlights.append({"id":streetlight.id,"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"DRY_BIN":streetlight.DRY_BIN,"WET_BIN":streetlight.WET_BIN,"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':streetlights}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')
