from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('organizations/', views.organization_list, name='organization_list'),
]