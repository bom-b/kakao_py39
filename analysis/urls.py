from django.urls import path

from analysis import views

urlpatterns = [
    path('picture_test_form', views.resnet1_writer),
    path('analysis_picture', views.analysis_picture),
    path('recommend_menu', views.recommend_menu),
    path('test_analysis', views.test_analysis),
]