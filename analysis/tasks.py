import json
import os
import time
from datetime import datetime
import requests
from celery import Celery

from kakao_py39.celery import app
from googletrans import Translator
from analysis.models import MyResNet50Model

UPLOAD_DIR = 'media/analysis/'

app = Celery('tasks', broker='redis://127.0.0.1:6379')
# analysis > tasks.py 파일임.
@app.task
# @csrf_exempt
def celery_analysis_picture(secure_urls_str, callback_url):

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
    ko_res = translator.translate(res, dest='ko').text

    # 응답 데이터 생성
    response_data = {
        "version": "2.0",
        "useCallback": True,
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"예측 결과 : {ko_res}",
                        "description": f"'{ko_res}'일 확률이 {f_resProba}%입니다.",
                        "thumbnail": {
                            "imageUrl": secure_urls_str
                        },
                        "buttons": [
                            {
                                "action": "webLink",
                                "label": "크게보기",
                                "webLinkUrl": secure_urls_str
                            }
                        ]
                    }
                }
            ]
        }
    }

    print('유알엘로 다시 보내기')
    # POST 요청 보내기
    headers = {'Content-Type': 'application/json'}
    response = requests.post(callback_url, data=json.dumps(response_data), headers=headers)
    print('response status code : ', response.status_code)
    print('response text : ', response.text)
