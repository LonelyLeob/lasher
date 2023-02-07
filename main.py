#main logistic file
from aiogram import Bot, Dispatcher, executor
from service import *
import os
from dotenv import load_dotenv
load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot)

def register_handlers(dp:Dispatcher):
    dp.register_message_handler(welcome, commands=['start'])
    dp.register_message_handler(get_order_list, commands=['lst'])
    dp.register_message_handler(add_free_order, commands=['add'])

if __name__ == '__main__':
    on_startup(bot, os.getenv("DB_NAME"), int(os.getenv("ADMIN_ID")))
    register_handlers(dp=dp)
    executor.start_polling(dp, skip_updates=True)