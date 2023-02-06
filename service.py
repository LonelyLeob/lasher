#file to describe handlers
from aiogram import types, Bot
from adadb import FDatabase,Repos
import random
import string

def on_startup(inst:Bot, db_name:str, admin_id:int):
    global repos, bot, admin
    admin = admin_id
    bot = inst
    fdb = FDatabase(db_name)
    repos = Repos(fdb.migration())

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


async def send_welcome(message: types.Message):
    user = message.from_user
    code = generate_random_string(8)

    try:
        repos.create_user(user.id, user.first_name, user.last_name, code)
        await bot.send_message(admin, f"Зарегистрировался новый пользователь {user.full_name} с id {user.id}")
        await message.reply(f"Сообщение отправлено пользователю {user.first_name}")
    except Exception as e:
        await message.answer("Вы уже зарегистрированы! Выберите день для ресничек;)")
        await bot.send_message(admin, f"Пользователь с никнеймом {user.full_name} и id {user.id} вызвал ошибку внутри приложения, обратите внимание!")