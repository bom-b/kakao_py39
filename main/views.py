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
    # try:
    #     load_json = json.loads(request.body.decode('utf8'))
    #     logger.debug(str(load_json))
    # except json.JSONDecodeError as e:
    #     logger.error("Invalid JSON format: %s", e)
    #     return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "간단한 텍스트 요소입니다."
                    }
                }
            ]
        }
    })
