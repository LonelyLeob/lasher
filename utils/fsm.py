from aiogram.dispatcher.filters.state import State, StatesGroup

class GuestState(StatesGroup):
    reffer_code = State()
    messaging_on = State()
    preset = State()

class SchedulerAddState(StatesGroup):
    date = State()

class SchedulerDeleteState(StatesGroup):
    date = State()

class MailingState(StatesGroup):
    mail_text = State()

class SubbingState(StatesGroup):
    agreement = State()