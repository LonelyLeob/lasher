from aiogram.dispatcher.filters.state import State, StatesGroup

class GuestState(StatesGroup):
    reffer_code = State()

class SchedulerState(StatesGroup):
    date = State()

class MailingState(StatesGroup):
    mail_text = State()