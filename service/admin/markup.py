from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.callbacks import agreement
from utils.funcs import normalize_to_unix

class AdminMarkup(InlineKeyboardMarkup):
    do_order = InlineKeyboardButton(text="Добавить запись", callback_data="insert")
    delete_order = InlineKeyboardButton(text="Закрыть запись", callback_data="delete")
    do_mailing = InlineKeyboardButton(text="Сделать рассылку", callback_data="mail")
    
    def register(self):
        return self.add(self.do_order, self.delete_order, self.do_mailing)

class ApplyingMarkup(InlineKeyboardMarkup):
    yes = InlineKeyboardButton(text="Подтверждаю")
    no = InlineKeyboardButton(text="Отклоняю")

    def register(self, id:int, date:str):
        self.yes.callback_data = agreement.new(id=str(id), answer='yes', date=str(normalize_to_unix(date)))
        self.no.callback_data = agreement.new(id=str(id), answer='no', date="no")
        return self.add(self.yes, self.no)