from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class AdminMarkup(InlineKeyboardMarkup):
    do_order = InlineKeyboardButton(text="Добавить запись", callback_data="insert")
    delete_order = InlineKeyboardButton(text="Закрыть запись", callback_data="delete")
    do_mailing = InlineKeyboardButton(text="Сделать рассылку", callback_data="mail")
    
    def register(self):
        return self.add(self.do_order, self.delete_order, self.do_mailing)

class ApplyingMarkup(InlineKeyboardMarkup):
    yes = InlineKeyboardButton(text="Подтверждаю", callback_data="123")
    no = InlineKeyboardButton(text="Отклоняю", callback_data="345")

    def register(self):
        return self.add(self.yes, self.no)