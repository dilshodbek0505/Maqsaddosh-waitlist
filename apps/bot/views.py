import hashlib
import hmac
import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()

BOT_TOKEN = settings.BOT_TOKEN

def check_auth(data: dict) -> bool:
    check_hash = data.pop("hash")
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return h == check_hash

@csrf_exempt
def telegram_auth(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        if not check_auth(data.copy()):
            return JsonResponse({"error": "Invalid auth data"}, status=400)

        user, created = User.objects.get_or_create(
            telegram_id=data['id'],
            defaults={
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "username": data.get("username"),
                "image": data.get("photo_url"),
            }
        )

        return JsonResponse({
            "status": "ok",
            "user_id": user.id,
            "username": user.username
        })

    return JsonResponse({'error': "Invalid method"}, status=405)