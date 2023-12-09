import json
import os
import re
from datetime import datetime

from django.http import JsonResponse
from googletrans import Translator
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from analysis.models import MyResNet50Model

UPLOAD_DIR = 'static/images/'


# 테스트폼
def resnet1_writer(request):
    return render(request, "analysis/img_test.html")


# 이미지 분석 api
@csrf_exempt
def analysis_picture(request):
    load_json = json.loads(request.body.decode('utf8'))
    # print(str(load_json))
    secureimage_str = load_json.get('action').get('params').get("secureimage", '{}')
    # print(secureimage_str)
    match = re.search(r'"secureUrls":"(List\(.+?\))"', secureimage_str)
    secure_urls_str = match.group(1)[5:-1]
    # print(secure_urls_str)

    now = datetime.now()
    # datetime 객체를 초로 변환합니다.
    timestamp = str(int(now.timestamp()))

    response = requests.get(secure_urls_str)
    myModel = MyResNet50Model()

    if response.status_code == 200:
        image_data = response.content

        save_path = os.path.join(UPLOAD_DIR, f"{timestamp}.jpg")

        with open(save_path, "wb") as f:
            f.write(image_data)

    else:
        print(f"Failed to download image. Status code: {response.status_code}")

    top = myModel.myImagePredict(UPLOAD_DIR + f"{timestamp}.jpg")

    res = top[0][1]
    resProba = float(f"{top[0][2]:.3f}") * 100
    f_resProba = f"{resProba:.1f}"

    # res2 = top[1][1]
    # resProba2 = float(f"{top[1][2]:.3f}") * 100
    # f_resProba2 = f"{resProba2:.1f}"
    #
    # res3 = top[2][1]
    # resProba3 = float(f"{top[2][2]:.3f}") * 100
    # f_resProba3 = f"{resProba3:.1f}"

    translator = Translator()
    ko_res = translator.translate(res, dest='ko').text
    # ko_res2 = translator.translate(res2, dest='ko').text
    # ko_res3 = translator.translate(res3, dest='ko').text

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"예측 결과 : {ko_res}",
                        "description": f"'{ko_res}'일 확률이 {f_resProba}%입니다.",
                        # "description": f"'{ko_res}'일 확률이 {f_resProba}%입니다. \n\n(후보)\n'{ko_res2}'일 확률이 {f_resProba2}%\n'{ko_res3}'일 확률이 {f_resProba3}%",
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
