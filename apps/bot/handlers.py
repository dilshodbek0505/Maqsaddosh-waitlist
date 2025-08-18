from asgiref.sync import sync_to_async

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart, CommandObject

from apps.bot.models import SmsPenndingBot


router = Router()


@router.message(CommandStart(deep_link=True))
async def start_command(message: types.Message, command: CommandObject, state: FSMContext):
    token = command.args
    await state.set_data({"token": token})
    
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Telfon raqam 📱", request_contact=True)]
        ]
    , resize_keyboard=True)
    await message.answer("Telfon raqamingizni yuboring:", reply_markup=kb)


@router.message(F.contact)
async def get_contact(message: types.Message, state: FSMContext):
    import secrets
    data = await state.get_data()
    
    token = data.get("token")
    phone = message.contact.phone_number.strip()

    try: 
        pending = await sync_to_async(
        lambda: SmsPenndingBot.objects.filter(uuid=token, phone=phone).first()
        )()
    except Exception as err:
        await message.answer("Xatolik sodir bo'ldi!")
        print("Xatolik: ", str(err))
        return 
    
    if not pending:
        await message.answer("Telfon raqam yoki token mos kelmadi!")
        return
    
    generate_code = str(secrets.randbelow(9000) + 1000) 
    pending.code = generate_code
    await sync_to_async(pending.save)(update_fields=['code'])


    await message.answer("Tasdiqlash kodingiz: <b>{}</b>".format(generate_code), parse_mode="HTML")