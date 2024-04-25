from django.contrib import admin
from django.urls import path, include
from .views import PortalView, AboutView, BillCreationView

urlpatterns = [
    path('', PortalView, name='portal'),
    path('about/', AboutView.as_view(), name='about'),
    path('bill_creation/', BillCreationView, name='bill-creation'),
    path('bill_creation/<str:location_name>/', BillCreationView, name='bill-creation'),
    path('kiosk/<str:location_name>/', PortalView, {'kiosk': True}, name='kiosk'),
    path('<str:location_name>/', PortalView, name='location'),
]