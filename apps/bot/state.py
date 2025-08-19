from aiogram.fsm.state import State, StatesGroup


class MessageStateGroup(StatesGroup):
    text = State()