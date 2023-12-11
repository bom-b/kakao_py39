from django.shortcuts import render


# 로그인 페이지로 이동
# Create your views here.
def login_page(request):
    return render(request, "member/login.html")


