from django.urls import path, include

from main import views

urlpatterns = [
    path('', views.mymain),
    path('communication_test', views.communication_test),
]