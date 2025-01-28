from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.Index, name='index'),
    path('details/<str:slug>', views.Details, name='details'),
    path('contacts', views.Contact, name='contacts'),
    path('about_us', views.About, name='about_us'),
    path('register', views.Register, name='register'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>', views.reset_password, name='reset_password'),
    path('new_post', views.new_post, name='new_post'),
    path('edit_post/<str:slug>', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('publish_post/<int:post_id>', views.publish_post, name='publish_post')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)