from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from sqlite3 import OperationalError
from aiogram.utils.exceptions import BotBlocked
from adadb import ScheduleRepos, UserRepos
from utils.fsm import MailingState, SchedulerState
from service.admin.markup import AdminMarkup
from utils.funcs import normalize_to_unix



class Admin(object):
    def __init__(self, id, bot: Bot, driver):
        self.id = id
        self.bot = bot
        self.user = UserRepos(driver)
        self.schedule = ScheduleRepos(driver)
        self.markup = AdminMarkup().register()
    
    async def start_add_free_order(self, message: types.Message):
        await self.bot.send_message(message.from_user.id, "Введите дату, на которую можно записаться")
        await SchedulerState.date.set()

    async def end_add_free_order(self, message: types.Message, state: FSMContext):
        await state.finish()
        try:
            self.schedule.add_order(normalize_to_unix(message.text))
        except Exception:
            await self.bot.send_message(self.id, f"Что-то произошло при добавлении записи, пожалуйста, сообщите системному администратору", reply_markup=self.markup)
            return
        await self.bot.send_message(self.id, f"Запись добавлена на {message.text}", reply_markup=self.markup)

    async def delete_free_order(self, message:types.Message):
        await self.bot.send_message(message.from_user.id, "Эта функция пока не завершена")


    async def start_mailing_to_clients(self, message:types.Message):
        await self.bot.send_message(self.id, "Введите текст для рассылки")
        await MailingState.mail_text.set()

    async def end_mailing_to_clients(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["mailing"] = message.text
        mail = 0
        notmail = 0
        try:
            for item in self.user.get_all_users_id():
                mail += 1
                await self.bot.send_message(item[0], data["mailing"])
        except BotBlocked:
            notmail += 1
            pass
        except OperationalError:
                await self.bot.send_message(self.id, "Случилась непредвиденная ошибка, обратитесь к системному администратору")
        mail = mail - notmail

        await self.bot.send_message(self.id, f"Рассылка успешно отправлена {mail} человек" + (f", еще {notmail} человек рассылку не получили" if notmail > 0 else ""))
        await state.finish()
        await self.bot.send_message(self.id, "Выберите, что делать дальше", reply_markup=self.markup)

    def register_handlers_admin(self, dp:Dispatcher):
        dp.register_callback_query_handler(self.start_add_free_order, text='insert')
        dp.register_message_handler(self.end_add_free_order, state=SchedulerState.date)
        dp.register_callback_query_handler(self.delete_free_order, text='delete')
        dp.register_callback_query_handler(self.start_mailing_to_clients, text="mail")
        dp.register_message_handler(self.end_mailing_to_clients,state=MailingState.mail_text)