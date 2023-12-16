import json
import os
import re
import time
from datetime import datetime

from django.http import JsonResponse
from googletrans import Translator
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from analysis.models import MyResNet50Model
from member.models import Members
from .tasks import celery_analysis_picture

UPLOAD_DIR = 'media/analysis/'


# 테스트폼
def resnet1_writer(request):
    return render(request, "analysis/img_test.html")


# analysis > views.py 파일임.
# 이미지 분석 api
@csrf_exempt
def analysis_picture(request):
    load_json = json.loads(request.body.decode('utf8'))

    # 'secureimage' 키가 있는지 확인
    if 'secureimage' in load_json['action']['params']:
        secure_urls_str = json.loads(load_json['action']['params']['secureimage'])['secureUrls']
        secure_urls_str = secure_urls_str.replace('List(', '').replace(')', '')

    else:
        # 'secureimage' 키가 없는 경우의 처리
        secure_urls_str = json.loads(load_json['action']['params']['img'])['secureUrls']
        secure_urls_str = secure_urls_str.replace('List(', '').replace(')', '')

    # callbackUrl 추출
    callback_url = load_json['userRequest']['callbackUrl']

    # plusfriend_user_key 추출
    plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
        'plusfriend_user_key')

    # "meal_time" 값을 추출
    meal_time_value = load_json['action']['clientExtra']['meal_time']

    try:
        member = Members.objects.get(kakaotalk_cord=plusfriend_user_key)
        member_nickname = str(member.nickname)
        is_in = True

    except Members.DoesNotExist:
        is_in = False

    if is_in:
        msg = f"사진을 분석하는 동안 잠시 기다려 주세요!"
    else:
        msg = f"데이터를 저장 하시려면 회원가입을 해주세요.\n\n사진을 분석하는 동안 잠시 기다려 주세요!"

    # 비동기처리 - 사진분석 함수 호출
    celery_analysis_picture.apply_async(args=(secure_urls_str, callback_url, plusfriend_user_key, meal_time_value))

    return JsonResponse({
        "version": "2.0",
        "useCallback": True,
        "data": {
            "msg": msg,
            "load_json": str(load_json)
        }
    })


@csrf_exempt
def recommend_menu(request):
    load_json = json.loads(request.body.decode('utf8'))

    try:
        # plusfriend_user_key 추출
        plusfriend_user_key = load_json.get('userRequest', {}).get('user', {}).get('properties', {}).get(
            'plusfriend_user_key')

        member = Members.objects.get(kakaotalk_cord=plusfriend_user_key)
        member_nickname = str(member.nickname)

    except:
        return JsonResponse({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "회원가입을 해주세요."
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
                        "text": "저녁 식단을 추천해드릴게요!"
                    }
                },
                {
                    "simpleText": {
                        "text": f"{member_nickname}님의 하루 식단을 분석한 결과" +
                        " 하루 권장 섭취량 기준, \n\n" +
                        "칼로리 35% 부족,\n" +
                        "단백질 20% 부족,\n" +
                        "나트륨 10% 과섭취"
                    }
                },
                {
                    "carousel": {
                        "type": "itemCard",
                        "items": [

                            {
                                "imageTitle": {
                                    "title": "삼계탕",
                                    "description": "1인분 기준"
                                },
                                "title": "",
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "https://www.chuksannews.co.kr/data/photos/20210414/art_16177684990221_d040c6.jpg",
                                    "width": 800,
                                    "height": 800
                                },
                                "itemList": [
                                    {
                                        "title": "칼로리",
                                        "description": "900kcal"
                                    },
                                    {
                                        "title": "단백질",
                                        "description": "20g"
                                    },
                                    {
                                        "title": "탄수화물",
                                        "description": "50g"
                                    },
                                    {
                                        "title": "지방",
                                        "description": "포화지방: 10g\n트랜스지방: 0g\n불포화지방: 10g"
                                    },
                                    {
                                        "title": "콜레스테롤",
                                        "description": "121mg"
                                    },
                                    {
                                        "title": "나트륨",
                                        "description": "1924mg"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "자세히 보기",
                                        "messageText": "고마워"
                                    }
                                ],
                                "itemListAlignment": "right",
                                "buttonLayout": "vertical"
                            },

                            {
                                "imageTitle": {
                                    "title": "밥, 무국, 김치, 시금치무침",
                                    "description": "1인분 기준"
                                },
                                "title": "",
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "https://mblogthumb-phinf.pstatic.net/MjAxODAyMjRfMjk0/MDAxNTE5NDQwMTg1OTU2.JKq0-d5KiA2gjilMpNrxuPZ86HHtgnlge_aroIMq3jog.N9lBjy-ORkGnLNnHtozpPccDaw0Q_56afp2VLUJewegg.JPEG.valueyey/%EC%95%84%EC%B9%A8%EC%8B%9D%ED%83%81.JPG?type=w800",
                                    "width": 800,
                                    "height": 800
                                },
                                "itemList": [
                                    {
                                        "title": "칼로리",
                                        "description": "900kcal"
                                    },
                                    {
                                        "title": "단백질",
                                        "description": "20g"
                                    },
                                    {
                                        "title": "탄수화물",
                                        "description": "50g"
                                    },
                                    {
                                        "title": "지방",
                                        "description": "포화지방: 10g\n트랜스지방: 0g\n불포화지방: 10g"
                                    },
                                    {
                                        "title": "콜레스테롤",
                                        "description": "121mg"
                                    },
                                    {
                                        "title": "나트륨",
                                        "description": "1924mg"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "자세히 보기",
                                        "messageText": "고마워"
                                    }
                                ],
                                "itemListAlignment": "right",
                                "buttonLayout": "vertical"

                            },

                            {
                                "imageTitle": {
                                    "title": "삼겹살",
                                    "description": "200g 기준"
                                },
                                "title": "",
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "https://i.namu.wiki/i/0NPS6g2Cxk8YDk-W9yRJrBMX-pgsItemO1f2qckU3CkBGmFicbTIQ9hP67XeEDpqIA9ec7ceGgiBVL86BcQmx2knVRobflKV1V_uZQDF31vGwCMo2Crd-rj9yXL-1xYvFuNPTGHIelmxXKtVsnfdEg.webp",
                                    "width": 800,
                                    "height": 800
                                },
                                "itemList": [
                                    {
                                        "title": "칼로리",
                                        "description": "661kcal"
                                    },
                                    {
                                        "title": "단백질",
                                        "description": "34.47g"
                                    },
                                    {
                                        "title": "탄수화물",
                                        "description": "1.18g"
                                    },
                                    {
                                        "title": "지방",
                                        "description": "포화지방: 19.342g\n트랜스지방: 0g\n불포화지방: 25.512g"
                                    },
                                    {
                                        "title": "콜레스테롤",
                                        "description": "121mg"
                                    },
                                    {
                                        "title": "나트륨",
                                        "description": "1924mg"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "자세히 보기",
                                        "messageText": "고마워"
                                    }
                                ],
                                "itemListAlignment": "right",
                                "buttonLayout": "vertical"

                            },

                            {
                                "imageTitle": {
                                    "title": "샐러드 식단",
                                    "description": "1인분 기준"
                                },
                                "title": "",
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "https://mblogthumb-phinf.pstatic.net/MjAxODAyMTBfMjkg/MDAxNTE4MTkzMjEyNDM0.3Ue2J07GN7V06QsXCClc8gl_v6PZgOI_7W8twpr5OVYg.PUR96dsqG0gEQMtAUhlSRmXnMr0PuEwyB97WN-wbkSYg.JPEG.hnojkm/image_8899831471518193179987.jpg?type=w800",
                                    "width": 800,
                                    "height": 800
                                },
                                "itemList": [
                                    {
                                        "title": "칼로리",
                                        "description": "900kcal"
                                    },
                                    {
                                        "title": "단백질",
                                        "description": "20g"
                                    },
                                    {
                                        "title": "탄수화물",
                                        "description": "50g"
                                    },
                                    {
                                        "title": "지방",
                                        "description": "포화지방: 10g\n트랜스지방: 0g\n불포화지방: 10g"
                                    },
                                    {
                                        "title": "콜레스테롤",
                                        "description": "121mg"
                                    },
                                    {
                                        "title": "나트륨",
                                        "description": "1924mg"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "자세히 보기",
                                        "messageText": "고마워"
                                    }
                                ],
                                "itemListAlignment": "right",
                                "buttonLayout": "vertical"

                            }
                        ]
                    }
                }
            ]
        }
    })


# 테스트용
@csrf_exempt
def test_analysis(requset):
    file = requset.FILES['file1']
    # multipart/form-data => requset.FILES['']
    # file의 _name, file_size 함께 전송되어 온다.

    print('requset.FILES["file1"] => ', requset.FILES['file1'])
    print('file_name => ', file._name)
    print('file_size =>', file.size)

    if 'file1' in requset.FILES:
        file = requset.FILES['file1']
        file_name = file._name
        fp = open(UPLOAD_DIR + file_name, 'wb')
        # 'wb' = write binary = 파일을 쓰겠다는거임 1바이트씩 받아서
        # chunk() : 1바이트 단위로 읽어들이는 함수
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        imagePath = UPLOAD_DIR + file_name
        myModel = MyResNet50Model()

        top = myModel.myImagePredict(imagePath)
        print(f"예측결과:{top[0][1]}일 확률이 {top[0][2]:2f}%")
        resProba = f"{top[0][2]:2f}"
        resJson = {"res": top[0][1], "probability": resProba}

    return JsonResponse(resJson, json_dumps_params={'ensure_ascii': False}, safe=False)
