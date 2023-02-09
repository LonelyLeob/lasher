#file to describe handlers
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from adadb import UserRepos, ScheduleRepos
from utils.fsm import GuestState
from utils.funcs import generate_random_string, unix_to_normalize
from service.customer.markup import ClientMarkup, ContactsMarkup

class Client():
    def __init__(self, driver, bot: Bot, admin):
        self.user = UserRepos(driver)
        self.order = ScheduleRepos(driver)
        self.bot = bot
        self.admin = admin
        self.markup = ClientMarkup().register()
        self.contacts = ContactsMarkup().register()

    async def preset_user(self, message: types.Message, state: FSMContext):
        whoer = message.from_user
        code = generate_random_string(8)
        async with state.proxy() as data:
            if message.text == "/cancel":
                await self.bot.send_message(whoer.id, f"Добро пожаловать:)", reply_markup=self.markup)
                await state.finish()
                return
            data[whoer.id] = message.text
        try:
            self.user.create_user(whoer.id, whoer.first_name, whoer.last_name, code)
            await self.bot.send_message(whoer.id,f"Вы успешно зарегистрированы!\n NOTE: приглашайте друзей и получайте скидку! Подробнее об этом в вашем профиле", reply_markup=ClientMarkup().register())
            await self.bot.send_message(self.admin, f"Зарегистрировался новый пользователь {whoer.full_name} с id {whoer.id}")
        except Exception:
            await self.bot.send_message(whoer.id, "Вы уже зарегистрированы! Выберите день для ресничек;)", reply_markup=self.markup)
            await self.bot.send_message(self.admin, f"Пользователь с никнеймом {whoer.full_name} и id {whoer.id} вызвал ошибку внутри приложения, обратите внимание!")
        await state.finish()

    async def contactmarkup(self, message: types.Message):
        whoer = message.from_user
        await self.bot.send_message(whoer.id, f"Контакты:\n+79534677673 - WhatsApp", reply_markup=self.contacts)

    async def profile(self, message: types.Message):
        whoer = message.from_user
        profile = self.user.profile(whoer.id)
        await self.bot.send_message(whoer.id, f"👤Профиль\nВаше имя: {profile[1]}\nЗаписей сделано: 0\nРеферальный код: {profile[3]}\nПриглашенных друзей: {profile[4]}", reply_markup=self.markup)

    def register_handlers_client(self, dp:Dispatcher):
        dp.register_message_handler(self.preset_user,state=GuestState().reffer_code)
        dp.register_callback_query_handler(self.contactmarkup, text="contacts")
        # dp.register_callback_query_handler(self.schedule, text="schedule")
        dp.register_callback_query_handler(self.profile, text="profile")