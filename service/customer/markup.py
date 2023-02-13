from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.funcs import unix_to_normalize
from utils.callbacks import schedule, messaging

class ClientMarkup(InlineKeyboardMarkup):
    schedule = InlineKeyboardButton(text='Расписание', callback_data='schedule')
    contacts = InlineKeyboardButton(text='Контакты', callback_data='contacts')
    profile = InlineKeyboardButton(text='Профиль', callback_data='profile')
    def register(self):
        self.row_width=3
        return self.add(self.schedule, self.contacts, self.profile)

class ProfileMarkup(InlineKeyboardMarkup):
    messaging_on = InlineKeyboardButton(text='Включить рассылку')
    messaging_off = InlineKeyboardButton(text='Выключить рассылку')
    def register(self):
        self.row_width=1
        self.messaging_on.callback_data = messaging.new("on")
        self.messaging_off.callback_data = messaging.new("off")
        return self.add(self.messaging_on, self.messaging_off)

class ContactsMarkup(InlineKeyboardMarkup):
    telegram_link = InlineKeyboardButton(text='Мой телеграмм', url="google.com")
    instagram_link = InlineKeyboardButton(text='Мой инстаграмм', url="google.com")
    developer_link = InlineKeyboardButton(text='Разработчик', url="google.com")
    maps_link = InlineKeyboardButton(text='Мы на картах', callback_data="maps")
    def register(self):
        self.row_width=2
        return self.add(self.telegram_link, self.instagram_link, self.developer_link, self.maps_link)

class ScheduleMarkup(InlineKeyboardMarkup):
    def schedule(self, buttons:list):
        self.row_width = 1
        for button in buttons:
            self.add(InlineKeyboardButton(text=unix_to_normalize(button[0]), callback_data=schedule.new(date=unix_to_normalize(button[0]))))
        return self