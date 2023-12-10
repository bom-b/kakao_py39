import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def mymain(request):
    return render(request, "main/main.html")


logger = logging.getLogger(__name__)


@csrf_exempt
def communication_test(request):
    load_json = json.loads(request.body.decode('utf8'))
    # print(str(load_json))
    plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
        'plusfriend_user_key', None)

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"서버 연결 상태: 정상 \n접속 유저 : {plusfriend_user_key}"
                    }
                }
            ]
        }
    })
