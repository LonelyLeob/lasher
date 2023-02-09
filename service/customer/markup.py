from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    def register(self):
        return super().add(self.telegram_link, self.instagram_link, self.developer_link)
