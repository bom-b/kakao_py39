from django.shortcuts import render


# Create your views here.
def mymain(request):
    return render(request, "main/main.html")
