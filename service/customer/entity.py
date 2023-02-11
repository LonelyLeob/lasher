#file to describe handlers
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from adadb import UserRepos, ScheduleRepos
from utils.fsm import GuestState
from utils.funcs import generate_random_string
from service.customer.markup import ClientMarkup, ContactsMarkup, ScheduleMarkup
from service.admin.markup import ApplyingMarkup
import time

class Client():
    def __init__(self, driver, bot: Bot, admin, coord:tuple):
        self.user = UserRepos(driver)
        self.schedule = ScheduleRepos(driver)
        self.bot = bot
        self.admin = admin
        self.markup = ClientMarkup().register()
        self.contacts = ContactsMarkup().register()
        self.coordinates = coord

    async def preset_user(self, message: types.Message, state: FSMContext):
        whoer = message.from_user
        code = generate_random_string(8)
        async with state.proxy():
            if message.text == "/cancel":
                self.user.create_user(whoer.id, whoer.first_name, whoer.last_name, code)
                await self.bot.send_message(whoer.id,f"Вы успешно зарегистрированы!\n NOTE: приглашайте друзей и получайте скидку! Подробнее об этом в вашем профиле", reply_markup=ClientMarkup().register())
                await self.bot.send_message(self.admin, f"Зарегистрировался новый пользователь {whoer.full_name} с id {whoer.id}")
                await state.finish()
                return
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
        await self.bot.send_message(whoer.id, f"Мы в соц.сетях", reply_markup=self.contacts)

    async def maps(self, message:types.Message):
        await self.bot.send_location(chat_id=message.from_user.id, latitude=self.coordinates[0], longitude=self.coordinates[1])

    async def profile(self, message: types.Message):
        whoer = message.from_user
        profile = self.user.profile(whoer.id)
        await self.bot.send_message(whoer.id, f"👤Профиль\nВаше имя: {profile[1]}\nЗаписей сделано: 0\nРеферальный код: {profile[3]}\nПриглашенных друзей: {profile[4]}", reply_markup=self.markup)

    async def schedule_buttons(self, call: types.CallbackQuery):
        print(call.data)
        await self.bot.send_message(call.from_user.id, "Выберите день для записи", reply_markup=ScheduleMarkup().schedule(self.schedule.get_free_order_list(int(time.time()))))

    async def do_sub(self, call:types.CallbackQuery):
        date_sub = call.data.split("-")
        if len(date_sub)>0 & len(date_sub)<2:
            date_sub = date_sub[1]
            print(date_sub)
        await self.bot.send_message(self.admin, f"Пользователь {call.from_user.full_name} с id {call.from_user.id} хочет записаться на {date_sub}.\nВы подтверждаете запись?", reply_markup=ApplyingMarkup().register(call.from_user.id, date_sub))\

    async def end_do_sub(self, call:types.CallbackQuery):
        agree=call.data.split("-")
        if agree[1] == "yes":
            try:
                self.schedule.do_sub(agree[3], agree[2])
                print(agree[2], agree[3])
                await self.bot.send_message(agree[2],"Запись подтверждена!")
            except Exception as e:
                print(e)
                await self.bot.send_message(self.admin, f"Вызвана ошибка, обратитесь к системному администратору")
        else: await self.bot.send_message(agree[2],"Запись отклонена!"); return

    def register_handlers_client(self, dp:Dispatcher):
        dp.register_message_handler(self.preset_user,state=GuestState().reffer_code)
        dp.register_callback_query_handler(self.contactmarkup, text="contacts")
        dp.register_callback_query_handler(self.maps, text="maps")
        dp.register_callback_query_handler(self.schedule_buttons, text="schedule")
        dp.register_callback_query_handler(self.profile, text="profile")
        dp.register_callback_query_handler(self.do_sub, text_contains="sub")
        dp.register_callback_query_handler(self.end_do_sub, text_contains="agree")