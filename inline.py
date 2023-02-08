from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class GuestMarkup(InlineKeyboardMarkup):
    enter = InlineKeyboardButton(text='Войти', callback_data='enter')
    def register(self):
        return super().add(self.enter)