#file to describe handlers
from aiogram import types, Bot
from adadb import FDatabase, UserRepos, OrderRepos
from utils import generate_random_string, unix_to_normalize

def on_startup(inst:Bot, db_name:str, admin_id:int):
    global user, order, bot, admin
    admin = admin_id
    bot = inst
    fdb = FDatabase(db_name).migration()
    user = UserRepos(fdb)
    order = OrderRepos(fdb)

async def welcome(message: types.Message):
    whoer = message.from_user
    code = generate_random_string(8)

    try:
        user.create_user(whoer.id, whoer.first_name, whoer.last_name, code)
        await bot.send_message(admin, f"Зарегистрировался новый пользователь {whoer.full_name} с id {whoer.id}")
        await message.reply(f"")
    except Exception as e:
        await message.answer("Вы уже зарегистрированы! Выберите день для ресничек;)")
        await bot.send_message(admin, f"Пользователь с никнеймом {user.full_name} и id {user.id} вызвал ошибку внутри приложения, обратите внимание!")

async def add_order(message: types.Message):
    pass

async def cancel_order():
    pass

async def get_order_list(message: types.Message):
    for row in order.get_order_list():
        await message.answer(unix_to_normalize(row[1]))

async def add_free_order(message: types.Message):
    order.add_order(1675722615)
    if message.from_user.id == admin:
        await message.answer(f"Запись успешно создана!")
        return
    await message.answer("К сожалению, вы не админ;(")