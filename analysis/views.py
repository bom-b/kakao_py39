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
from .tasks import celery_analysis_picture

UPLOAD_DIR = 'static/images/'


# 테스트폼
def resnet1_writer(request):
    return render(request, "analysis/img_test.html")


# analysis > views.py 파일임.
# 이미지 분석 api
@csrf_exempt
def analysis_picture(request):
    load_json = json.loads(request.body.decode('utf8'))
    print(str(load_json))
    print('**********')

    # 'secureimage' 키가 있는지 확인
    if 'secureimage' in load_json['action']['params']:
        secure_urls_str = json.loads(load_json['action']['params']['secureimage'])['secureUrls']
        secure_urls_str = secure_urls_str.replace('List(', '').replace(')', '')

    else:
        # 'secureimage' 키가 없는 경우의 처리
        secure_urls_str = json.loads(load_json['action']['params']['img'])['secureUrls']
        secure_urls_str = secure_urls_str.replace('List(', '').replace(')', '')

    print(secure_urls_str)
    # print(f'타입 : {type(secure_urls_str)}')

    # callbackUrl 추출
    callback_url = load_json['userRequest']['callbackUrl']
    print('callback_url : ', callback_url)

    # 비동기처리 - 사진분석 함수 호출
    celery_analysis_picture.apply_async(args=(secure_urls_str, callback_url,))

    print('처음 받았던 요청에 응답 보내기')
    return JsonResponse({
        "version": "2.0",
        "useCallback": True,
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
