from django.urls import path
from apps.bot.views import telegram_auth


urlpatterns = [
    path("auth/Telegram/", telegram_auth, name="telegram-auth"),
]
