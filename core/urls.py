from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('organizations/', views.organization_list, name='organization_list'),
    path('ao/', views.ao_landing, name='ao_landing'),
]