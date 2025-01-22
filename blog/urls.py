from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index, name='index'),
    path('details/<str:slug>', views.Details, name='details'),
    path('contacts', views.Contact, name='contacts'),
    path('about_us', views.About, name='about_us'),
    path('register', views.Register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password')
]