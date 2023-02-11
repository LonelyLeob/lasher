from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.funcs import unix_to_normalize
from utils.callbacks import schedule

class ClientMarkup(InlineKeyboardMarkup):
    schedule = InlineKeyboardButton(text='Расписание', callback_data='schedule')
    contacts = InlineKeyboardButton(text='Контакты', callback_data='contacts')
    profile = InlineKeyboardButton(text='Профиль', callback_data='profile')
    def register(self):
        self.row_width=3
        return self.add(self.schedule, self.contacts, self.profile)

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
            print(schedule.new(date=unix_to_normalize(button[0])))
        return self