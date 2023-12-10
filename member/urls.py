from django.urls import path

from member import views

urlpatterns = [
    path('login_page', views.login_page),
]