import re

from asgiref.sync import sync_to_async
from django.conf import settings

from aiogram.exceptions import TelegramBadRequest
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, CommandObject

from apps.bot.models import SmsPenndingBot, ForwardMessage
from apps.bot.state import MessageStateGroup

router = Router()
GROUP_ID = settings.GROUP_ID



async def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    phone = re.sub(r"\D", "", phone)  
    
    if phone.startswith("998"):
        return f"+{phone}"
    return f"+{phone}" if not phone.startswith("+") else phone


@router.message(CommandStart(deep_link=True))
async def start_command(message: types.Message, command: CommandObject, state: FSMContext):
    await state.clear()

    token = command.args
    await state.set_data({"token": token})
    
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Telefon raqam 📱", request_contact=True)]
        ]
    , resize_keyboard=True)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)


@router.message(F.contact)
async def get_contact(message: types.Message, state: FSMContext):
    import secrets
    data = await state.get_data()
    
    token = data.get("token")
    phone = message.contact.phone_number.strip()
    phone = await normalize_phone(phone)

    generate_code = str(secrets.randbelow(9000) + 1000)

    try: 
        updated = await sync_to_async(
            lambda: SmsPenndingBot.objects.filter(uuid=token, phone=phone).update(code=generate_code)
        )()
    except Exception as err:
        await message.answer("Xatolik sodir bo'ldi!")
        print("Xatolik: ", str(err))
        return 
    
    if not updated:
        await message.answer("Telefon raqam yoki token mos kelmadi!")
        return
    
    await message.answer(f"Tasdiqlash kodingiz: <b>{generate_code}</b>", parse_mode="HTML")


@router.message(F.chat.type.in_(["private"]), CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Maqsaddosh loyhasining support botiga xush kelibsiz!. Savollaringiz bo'lsa yozib qoldiring:")
    await state.set_state(MessageStateGroup.text)

@router.message(MessageStateGroup.text)
async def help_message(message: types.Message, state: FSMContext):
    sent = await message.send_copy(chat_id=GROUP_ID)

    await ForwardMessage.objects.acreate(
        user_id=message.chat.id,
        user_message_id=message.message_id,
        group_message_id=sent.message_id,
        group_id=GROUP_ID
    )

    await message.answer("Xabaringiz yuborildi. Tez orqada javob beramiz.")

@router.message(F.chat.type.in_(["group", "supergroup"]))
async def handle_group_messages(message: types.Message):
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ("administrator", "creator"):
        await message.reply("Sizda bu amalni bajarish uchun ruxsat yo‘q.")
        return

    if not message.reply_to_message:
        return

    try:
        entry = await ForwardMessage.objects.aget(
            group_message_id=message.reply_to_message.message_id,
            group_id=GROUP_ID
        )
        try:
            await message.send_copy(
                chat_id=entry.user_id,
                reply_to_message_id=entry.user_message_id
            )
        except TelegramBadRequest:
            await message.reply("Foydalanuvchiga xabar yuborib bo‘lmadi.")
    
    except ForwardMessage.DoesNotExist:
        pass