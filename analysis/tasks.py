import json
import os
import time
from datetime import datetime
import requests
from celery import Celery

from kakao_py39.celery import app
from googletrans import Translator
from analysis.models import MyResNet50Model
from member.models import Members

UPLOAD_DIR = 'media/analysis/'

app = Celery('tasks', broker='redis://127.0.0.1:6379')


# analysis > tasks.py 파일임.
@app.task
# @csrf_exempt
def celery_analysis_picture(secure_urls_str, callback_url, plusfriend_user_key, meal_time_value):
    now = datetime.now()
    # datetime 객체를 초로 변환합니다.
    timestamp = str(int(now.timestamp()))

    response = requests.get(secure_urls_str)
    if response.status_code == 200:
        image_data = response.content

        save_path = os.path.join(UPLOAD_DIR, "{}.jpg".format(timestamp))

        with open(save_path, "wb") as f:
            f.write(image_data)

    else:
        print(f"Failed to download image. Status code: {response.status_code}")

    myModel = MyResNet50Model()
    top = myModel.myImagePredict(UPLOAD_DIR + "{}.jpg".format(timestamp))

    res = top[0][1]
    resProba = float(f"{top[0][2]:.3f}") * 100
    f_resProba = f"{resProba:.1f}"

    translator = Translator()
    ko_res = translator.translate(res, dest='ko', src='en').text

    # 응답 데이터 생성
    response_data = {
        "version": "2.0",
        "useCallback": True,
        "template": {
            "outputs": [
                {
                    "itemCard": {
                        "imageTitle": {
                            "title": f"{ko_res}",
                            "description": f"'{ko_res}'일 확률이 {f_resProba}%입니다."
                        },
                        "title": "",
                        "description": "",
                        "thumbnail": {
                            "imageUrl": secure_urls_str,
                            "width": 800,
                            "height": 800
                        },
                        "profile": {
                            "title": f"{meal_time_value}식단 분석"
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
                                "description": "포화지방: 10g\n트랜스지방: 0g"
                            },
                            {
                                "title": " ",
                                "description": "불포화지방: 10g"
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
                        "itemListAlignment": "right",
                        "buttonLayout": "vertical"
                    }
                },
                {
                    "textCard": {
                        "title": "제공한 데이터가 올바른가요?",
                        "description": '수정이 필요하다면 말씀해주세요.',
                        "buttons": [
                            {
                                "action": "message",
                                "label": "이대로 기록하기",
                                "messageText": "식단 기록하기",
                                "extra": {
                                    "plusfriend_user_key": plusfriend_user_key,
                                    "meal_time": meal_time_value,
                                    "calorie": "900",
                                    "protein": "20",
                                    "carbohydrate": "50",
                                    "fat": "10",
                                    "cholesterol": "121",
                                    "sodium": "1924"
                                }
                            },
                            {
                                "action": "message",
                                "label": "사진 다시 올리기",
                                "messageText": "식단 등록"
                            },
                        ]
                    }
                },
                {
                    "textCard": {
                        "title": " ",
                        "description": ' ',
                        "buttons": [
                            {
                                "action": "message",
                                "label": "사진 다시 분석하기",
                                "messageText": "사진 다시 분석하기"
                            },
                            {
                                "action": "message",
                                "label": "영양 정보만 수정하기",
                                "messageText": "영양 정보만 수정하기"
                            },
                            {
                                "action": "message",
                                "label": "모두 수동으로 입력하기",
                                "messageText": "모두 수동으로 입력하기"
                            }
                        ]
                    }
                }
            ]
        }
    }

    # POST 요청 보내기
    headers = {'Content-Type': 'application/json'}
    response = requests.post(callback_url, data=json.dumps(response_data), headers=headers)
    print('response status code : ', response.status_code)
    print('response text : ', response.text)
