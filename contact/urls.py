from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact_view'),
    path('thank-you/', views.contact_success, name='contact_success'),
]