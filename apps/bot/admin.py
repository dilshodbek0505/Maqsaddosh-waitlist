from django.contrib import admin

from apps.bot.models import SmsPenndingBot, TelegramUser

admin.site.register(SmsPenndingBot)

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "telegram_id")
    list_display_links = ("id", "first_name")