from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('form/', views.form_page, name='form'),
    path('special/', views.special_page, name='special')
]