"""streetlightdashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from streetlightrequesthandler.views import get_all_data_without_pagination, get_all_states_with_lon_lat, store_data_from_streetlight, get_all_data, get_no_of_records,get_all_states,get_all_historical_data,get_all_historical_data_without_pagination

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/store',store_data_from_streetlight,name='store'),
    path('api/get_all',get_all_data,name='get_all'),
    path('api/get_no_of_records',get_no_of_records, name="get_no_of_records"),
    path('api/get_all_states',get_all_states,name='get_all_states'),
    path('api/get_all_states_with_lon_lat',get_all_states_with_lon_lat,name='get_all_states_with_lon_lat'),
    path('api/get_all_historical_data',get_all_historical_data,name='get_all_historical_data'),
    path('api/get_all_data_without_pagination',get_all_data_without_pagination,name="get_all_data_without_pagination"),
    path('api/get_all_historical_data_without_pagination',get_all_historical_data_without_pagination,name="get_all_historical_data_without_pagination"),
]
