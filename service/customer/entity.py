#file to describe handlers
from aiogram import types, Dispatcher, Bot
from adadb import UserRepos, OrderRepos
from utils.funcs import generate_random_string, unix_to_normalize
from service.customer.inline import ClientMarkup, ContactsMarkup

class Client():
    def __init__(self, driver, bot: Bot, admin):
        self.user = UserRepos(driver)
        self.order = OrderRepos(driver)
        self.bot = bot
        self.admin = admin

    async def enter(self, message: types.Message):
        whoer = message.from_user
        code = generate_random_string(8)
        try:
            self.user.create_user(whoer.id, whoer.first_name, whoer.last_name, code)
            await self.bot.send_message(whoer.id,f"Вы успешно зарегистрированы!\n NOTE: приглашайте друзей и получайте скидку! Подробнее об этом в вашем профиле", reply_markup=ClientMarkup().register())
            await self.bot.send_message(self.admin, f"Зарегистрировался новый пользователь {whoer.full_name} с id {whoer.id}")
        except Exception as e:
            await self.bot.send_message(whoer.id, "Вы уже зарегистрированы! Выберите день для ресничек;)", reply_markup=ClientMarkup().register())
            await self.bot.send_message(self.admin, f"Пользователь с никнеймом {whoer.full_name} и id {whoer.id} вызвал ошибку внутри приложения, обратите внимание!")

    async def contacts(self, message: types.Message):
        whoer = message.from_user
        await self.bot.send_message(whoer.id, f"Контакты:\n+79534677673 - WhatsApp", reply_markup=ContactsMarkup().register())


    def register_handlers_client(self, dp:Dispatcher):
        dp.register_callback_query_handler(self.enter, text="enter")
        dp.register_callback_query_handler(self.contacts, text="contacts")
        # dp.register_callback_query_handler(self.schedule, text="schedule")
        # dp.register_callback_query_handler(self.refferal, text="refferal")