from django.urls import path

from record import views

urlpatterns = [
    path('record_meal', views.record_meal),
]