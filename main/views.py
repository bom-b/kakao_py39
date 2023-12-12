import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from member.models import Members


# Create your views here.
def mymain(request):
    return render(request, "main/main.html")


logger = logging.getLogger(__name__)


@csrf_exempt
def communication_test(request):
    load_json = json.loads(request.body.decode('utf8'))

    plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
        'plusfriend_user_key')

    try:
        member = Members.objects.get(kakaotalk_cord=plusfriend_user_key)
        member_nickname = str(member.nickname)

    except Members.DoesNotExist:
        print("해당하는 멤버가 존재하지 않습니다.")
        return JsonResponse({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "회원가입 기록이 없습니다. 회원가입 해주세요!"
                        }
                    }
                ]
            }
        })

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{member_nickname}님, 안녕하세요."
                    }
                }
            ]
        }
    })
