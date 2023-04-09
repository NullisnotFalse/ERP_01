from django.urls import path
from erp import views

app_name = 'erp'

urlpatterns = [
    path('', views.index, name='index'),
    path('inbound/', views.inbound, name='inbound'),
    path('outbound/', views.outbound, name='outbound'),
]
