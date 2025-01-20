from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index, name='index'),
    path('details/<str:slug>', views.Details, name='details'),
    path('contacts', views.Contact, name='contacts'),
    path('aboutus', views.About, name='aboutus')
]