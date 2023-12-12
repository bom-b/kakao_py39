from django.urls import path

from member import views

urlpatterns = [
    # 페이지 이동
    path('login_page', views.login_page),
    path('join_page', views.join_page),
    path('success_page', views.success_page),
    # 로직 수행
    path('member_join', views.member_join),
    path('check', views.check),
    # 카카오 요청
    path('request_join', views.request_join),
    path('request_member_del', views.request_member_del),
]