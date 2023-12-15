import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def record_meal(request):
    load_json = json.loads(request.body.decode('utf8'))
    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(load_json)
                    }
                }
            ]
        }
    })
