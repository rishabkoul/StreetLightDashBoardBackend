import json
from django.db.models import Q
from django.http.response import HttpResponse
from streetlightrequesthandler.models import StreetLight ,StreetLightHistory
import math

# Create your views here.
def store_data_from_streetlight(request):
    if request.method=='GET':
        payload=request.GET
        try:
            streetlightrecord = StreetLight.objects.get(ID=payload.get('ID'))
            streetlightrecordhistory=StreetLightHistory(ID=payload.get('ID'), BV=streetlightrecord.BV,BI=streetlightrecord.BI,SV=streetlightrecord.SV,SI=streetlightrecord.SI,LV=streetlightrecord.LV,LI=streetlightrecord.LI,BA=streetlightrecord.BA,STATE=streetlightrecord.STATE,LAT=streetlightrecord.LAT,LON=streetlightrecord.LON,DRY_BIN=streetlightrecord.DRY_BIN,WET_BIN=streetlightrecord.WET_BIN,DATE=streetlightrecord.DATE,TIME_STAMP=streetlightrecord.TIME_STAMP)
            streetlightrecordhistory.save()
            streetlightrecord.BV = payload.get('BV')
            streetlightrecord.BI = payload.get('BI')
            streetlightrecord.SV = payload.get('SV')
            streetlightrecord.SI = payload.get('SI')
            streetlightrecord.LV = payload.get('LV')
            streetlightrecord.LI = payload.get('LI')
            streetlightrecord.BA = payload.get('BA')
            streetlightrecord.STATE = payload.get('STATE')
            streetlightrecord.LAT = payload.get('LAT')
            streetlightrecord.LON = payload.get('LON')
            streetlightrecord.DRY_BIN = payload.get('DRY_BIN')
            streetlightrecord.WET_BIN = payload.get('WET_BIN')
            streetlightrecord.save()
        except:
            streetlightrecord = StreetLight(ID=payload.get('ID'), BV=payload.get('BV'),BI=payload.get('BI'),SV=payload.get('SV'),SI=payload.get('SI'),LV=payload.get('LV'),LI=payload.get('LI'),BA=payload.get('BA'),STATE=payload.get('STATE'),LAT=payload.get('LAT'),LON=payload.get('LON'),DRY_BIN=payload.get('DRY_BIN'),WET_BIN=payload.get('WET_BIN'))
            streetlightrecord.save()
        responses='SUCCESS'
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses)

def get_all_data(request):
    if request.method=='GET':
        payload=request.GET
        no_of_results_per_page=int(payload.get('no_of_results_per_page'))
        page_no=int(payload.get('page_no'))
        query=payload.get('query')
        total_results=StreetLight.objects.filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(DRY_BIN__icontains=query) | Q(WET_BIN__icontains=query) ).count()
        streetlights=[]
        for streetlight in StreetLight.objects.filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(DRY_BIN__icontains=query) | Q(WET_BIN__icontains=query) )[(page_no-1)*no_of_results_per_page:((page_no-1)*no_of_results_per_page)+no_of_results_per_page]:
            streetlights.append({"id":streetlight.id,"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"DRY_BIN":streetlight.DRY_BIN,"WET_BIN":streetlight.WET_BIN,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':streetlights,'no_of_results_per_page':no_of_results_per_page,'page_no':page_no,'total_results':total_results,'no_of_pages':math.ceil(total_results/no_of_results_per_page)}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')

def get_no_of_records(request):
    if request.method=='GET':
        total_results=StreetLight.objects.all().count()
        responses=json.dumps([{'total_results':total_results}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')

def get_all_states(request):
    if request.method=='GET':
        states=list(StreetLight.objects.all().values_list('STATE', flat=True))
        responses=json.dumps([{'states':states}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')

def get_all_states_with_lon_lat(request):
    if request.method=='GET':
        states_with_lon_lat=list(StreetLight.objects.all().values_list('LON', 'LAT','STATE'))
        responses=json.dumps([{'states_with_lon_lat':states_with_lon_lat}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')
