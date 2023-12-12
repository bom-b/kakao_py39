import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from member.models import Members


# 로그인 페이지로 이동
# Create your views here.
def login_page(request):
    return render(request, "member/login.html")


def join_page(request):
    return render(request, "member/join.html")


def success_page(request):
    return render(request, "member/success.html")


def check(request):
    kakaotalk_cord = request.POST['kakaotalk_cord']

    try:
        member = Members.objects.get(kakaotalk_cord=kakaotalk_cord)
        is_sing = 1

    except Members.DoesNotExist:
        is_sing = 0

    return JsonResponse({'is_sing': is_sing})


def member_join(request):
    is_success = 0
    dto = Members(
        nickname=request.POST['nickname'],
        kakaotalk_cord=request.POST['kakaotalk_cord']
    )
    dto.save()
    is_success = 1
    return JsonResponse({'is_sing': is_success})


@csrf_exempt
def request_member_del(request):
    load_json = json.loads(request.body.decode('utf8'))
    plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
        'plusfriend_user_key')

    try:
        member = Members.objects.get(kakaotalk_cord=plusfriend_user_key)
        member.delete()

    except Members.DoesNotExist:
        print("해당하는 멤버가 존재하지 않습니다.")
        return JsonResponse({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "회원가입 기록이 없습니다."
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
                        "text": "탈퇴가 정상적으로 처리되었습니다."
                    }
                }
            ]
        }
    })


@csrf_exempt
def request_join(request):
    load_json = json.loads(request.body.decode('utf8'))

    plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
        'plusfriend_user_key')

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "textCard": {
                        "title": f"회원가입 코드 : {plusfriend_user_key}",
                        "description": "코드를 회원가입시 입력해주세요.\n",
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "회원가입",
                                "webLinkUrl": "http://http://15.164.252.196/member/join_page"
                            }
                        ]
                    }
                }
            ]
        }
    })
