import json
from django.db.models import Q
from django.http.response import HttpResponse
from streetlightrequesthandler.models import StreetLight ,StreetLightHistory
import math
from shapely.geometry import MultiPoint
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def store_data_from_streetlight(request):
    if request.method=='GET':
        payload=request.GET
        try:
            streetlightrecord = StreetLight.objects.get(ID=payload.get('ID'))
            streetlightrecordhistory=StreetLightHistory(ID=payload.get('ID'), BV=streetlightrecord.BV,BI=streetlightrecord.BI,SV=streetlightrecord.SV,SI=streetlightrecord.SI,LV=streetlightrecord.LV,LI=streetlightrecord.LI,BA=streetlightrecord.BA,STATE=streetlightrecord.STATE,LAT=streetlightrecord.LAT,LON=streetlightrecord.LON,CHARGING_STATUS=streetlightrecord.CHARGING_STATUS,DAY_NIGHT=streetlightrecord.DAY_NIGHT,BW=streetlightrecord.BW,SW=streetlightrecord.SW,LW=streetlightrecord.LW,DATE=streetlightrecord.DATE,TIME_STAMP=streetlightrecord.TIME_STAMP)
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
            streetlightrecord.BW = float(payload.get('BV'))*float(payload.get('BI'))
            streetlightrecord.SW = float(payload.get('SV'))*float(payload.get('SI'))
            streetlightrecord.LW = float(payload.get('LV'))*float(payload.get('LI'))
            streetlightrecord.CHARGING_STATUS = payload.get('CHARGING_STATUS')
            streetlightrecord.DAY_NIGHT = payload.get('DAY_NIGHT')
            streetlightrecord.save()
        except:
            streetlightrecord = StreetLight(ID=payload.get('ID'), BV=payload.get('BV'),BI=payload.get('BI'),SV=payload.get('SV'),SI=payload.get('SI'),LV=payload.get('LV'),LI=payload.get('LI'),BA=payload.get('BA'),STATE=payload.get('STATE'),LAT=payload.get('LAT'),LON=payload.get('LON'),BW=float(payload.get('BV'))*float(payload.get('BI')),SW=float(payload.get('SV'))*float(payload.get('SI')),LW=float(payload.get('LV'))*float(payload.get('LI')),CHARGING_STATUS=payload.get('CHARGING_STATUS'),DAY_NIGHT=payload.get('DAY_NIGHT'))
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
        results=StreetLight.objects.filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(CHARGING_STATUS__icontains=query) | Q(DAY_NIGHT__icontains=query) ).order_by("-DATE","-TIME_STAMP")
        total_results=results.count()
        streetlights=[]
        for streetlight in results[(page_no-1)*no_of_results_per_page:((page_no-1)*no_of_results_per_page)+no_of_results_per_page]:
            streetlights.append({"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"CHARGING_STATUS":streetlight.CHARGING_STATUS,"DAY_NIGHT":streetlight.DAY_NIGHT,"BW":streetlight.BW,"SW":streetlight.SW,"LW":streetlight.LW,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':streetlights,'no_of_results_per_page':no_of_results_per_page,'page_no':page_no,'total_results':total_results,'no_of_pages':math.ceil(total_results/no_of_results_per_page)}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')

def get_all_data_without_pagination(request):
    if request.method=='GET':
        payload=request.GET
        query=payload.get('query')
        results=StreetLight.objects.filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(CHARGING_STATUS__icontains=query) | Q(DAY_NIGHT__icontains=query) ).order_by("-DATE","-TIME_STAMP")
        total_results=results.count()
        # streetlights=[]
        # for streetlight in results:
        #     streetlights.append({"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"CHARGING_STATUS":streetlight.CHARGING_STATUS,"DAY_NIGHT":streetlight.DAY_NIGHT,"BW":streetlight.BW,"SW":streetlight.SW,"LW":streetlight.LW,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':list(results.values()),'total_results':total_results}],cls=DjangoJSONEncoder)
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])

    return HttpResponse(responses,content_type='text/json')

def get_all_historical_data_without_pagination(request):
    if request.method=='GET':
        payload=request.GET
        query=payload.get('query')
        light_id=payload.get('light_id')
        results=StreetLight.objects.filter(ID=light_id).filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(CHARGING_STATUS__icontains=query) | Q(DAY_NIGHT__icontains=query) ).order_by("-DATE","-TIME_STAMP")
        results_history=StreetLightHistory.objects.filter(ID=light_id).filter(Q(ID__icontains=query) | Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(CHARGING_STATUS__icontains=query) | Q(DAY_NIGHT__icontains=query) ).order_by("-DATE","-TIME_STAMP")
        total_results=results.count()+results_history.count()
        # streetlights=[]
        # for streetlight in results:
        #     streetlights.append({"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"CHARGING_STATUS":streetlight.CHARGING_STATUS,"DAY_NIGHT":streetlight.DAY_NIGHT,"BW":streetlight.BW,"SW":streetlight.SW,"LW":streetlight.LW,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        # for streetlight in results_history:
        #     streetlights.append({"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"CHARGING_STATUS":streetlight.CHARGING_STATUS,"DAY_NIGHT":streetlight.DAY_NIGHT,"BW":streetlight.BW,"SW":streetlight.SW,"LW":streetlight.LW,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':list(results.values())+list(results_history.values()),'total_results':total_results}],cls=DjangoJSONEncoder)
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])

    return HttpResponse(responses,content_type='text/json')

def get_all_historical_data(request):
    if request.method=='GET':
        payload=request.GET
        no_of_results_per_page=int(payload.get('no_of_results_per_page'))
        page_no=int(payload.get('page_no'))
        query=payload.get('query')
        light_id=payload.get('light_id')
        latest_data=StreetLight.objects.filter(ID=light_id)[0]
        latest_data={"ID":latest_data.ID, "BV":latest_data.BV,"BI":latest_data.BI,"SV":latest_data.SV,"SI":latest_data.SI,"LV":latest_data.LV,"LI":latest_data.LI,"BA":latest_data.BA,"STATE":latest_data.STATE,"LAT":latest_data.LAT,"LON":latest_data.LON,"CHARGING_STATUS":latest_data.CHARGING_STATUS,"DAY_NIGHT":latest_data.DAY_NIGHT,"BW":latest_data.BW,"SW":latest_data.SW,"LW":latest_data.LW,"DATE":str(latest_data.DATE),"TIME_STAMP":str(latest_data.TIME_STAMP)}
        results=StreetLightHistory.objects.filter(ID=light_id).filter(Q(STATE__icontains=query) | Q(LAT__icontains=query)| Q(LON__icontains=query) | Q(CHARGING_STATUS__icontains=query) | Q(DAY_NIGHT__icontains=query) ).order_by("-DATE","-TIME_STAMP")
        total_results=results.count()
        streetlights=[]
        for streetlight in results[(page_no-1)*no_of_results_per_page:((page_no-1)*no_of_results_per_page)+no_of_results_per_page]:
            streetlights.append({"ID":streetlight.ID, "BV":streetlight.BV,"BI":streetlight.BI,"SV":streetlight.SV,"SI":streetlight.SI,"LV":streetlight.LV,"LI":streetlight.LI,"BA":streetlight.BA,"STATE":streetlight.STATE,"LAT":streetlight.LAT,"LON":streetlight.LON,"CHARGING_STATUS":streetlight.CHARGING_STATUS,"DAY_NIGHT":streetlight.DAY_NIGHT,"BW":streetlight.BW,"SW":streetlight.SW,"LW":streetlight.LW,"DATE":str(streetlight.DATE),"TIME_STAMP":str(streetlight.TIME_STAMP)})
        responses=json.dumps([{'Streetlights':streetlights,'latest_data':latest_data,'no_of_results_per_page':no_of_results_per_page,'page_no':page_no,'total_results':total_results,'no_of_pages':math.ceil(total_results/no_of_results_per_page)}])
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
        lon_lats=[]
        states_with_lon_lat=list(StreetLight.objects.all().values_list('LON', 'LAT','STATE'))
        for lon_lat in list(StreetLight.objects.all().values_list('LON', 'LAT')):
            lon_lats.append((float(lon_lat[0].replace("'",'')),float(lon_lat[1].replace("'",''))))

        points = MultiPoint(lon_lats)
        responses=json.dumps([{'states_with_lon_lat':states_with_lon_lat,'centroid':list(points.centroid.coords)}])
    else:
        responses=json.dumps([{'Error':'Only Get Request Allowed'}])   

    
    return HttpResponse(responses,content_type='text/json')
