import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from member.models import Members


# Create your views here.

@csrf_exempt
def record_meal(request):
    load_json = json.loads(request.body.decode('utf8'))

    # "clientExtra" 안의 값을 추출
    calorie = load_json['action']['clientExtra']['calorie']
    protein = load_json['action']['clientExtra']['protein']
    meal_time = load_json['action']['clientExtra']['meal_time']
    sodium = load_json['action']['clientExtra']['sodium']
    carbohydrate = load_json['action']['clientExtra']['carbohydrate']
    cholesterol = load_json['action']['clientExtra']['cholesterol']
    fat1 = load_json['action']['clientExtra']['fat1']
    fat2 = load_json['action']['clientExtra']['fat2']
    fat3 = load_json['action']['clientExtra']['fat3']
    plusfriend_user_key = load_json['action']['clientExtra']['plusfriend_user_key']
    food_name = load_json['action']['clientExtra']['food_name']

    # 현재 날짜를 가져오기
    formatted_date = datetime.now().strftime("%Y-%m-%d")

    try:
        member = Members.objects.get(kakaotalk_cord=plusfriend_user_key)
        member_nickname = str(member.nickname)

    except Members.DoesNotExist:
        return JsonResponse({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "데이터를 저장 하시려면 회원가입을 해주세요."
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
                        "text": "아래 내용을 기록합니다.\n\n" +
                        f"사용자 : {member_nickname}\n" +
                        f"날짜 : {formatted_date}\n" +
                        f"식사 시간 : {meal_time}\n\n" +

                        f"음식이름 : {food_name}\n" +
                        f"칼로리 : {calorie}\n" +
                        f"단백질 : {protein}\n" +
                        f"탄수화물 : {carbohydrate}\n" +
                        f"포화지방 : {fat1}\n" +
                        f"트렌스지방 : {fat2}\n" +
                        f"불포화지방 : {fat3}\n" +
                        f"콜레스테롤 : {cholesterol}\n" +
                        f"나트륨 : {sodium}\n"
                    }
                }
            ]
        }
    })
