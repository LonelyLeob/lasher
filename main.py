#main logistic file
from aiogram import Bot, Dispatcher, executor, types
from adadb import FDatabase
from service.customer.entity import Client
from service.admin.entity import Admin
from inline import GuestMarkup
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f"Приветствую тебя {message.from_user.full_name}! Здесь ты можешь записаться ко мне на реснички:)", reply_markup=GuestMarkup().register())

if __name__ == '__main__':
    driver = FDatabase(os.getenv("DB_NAME")).migration()
    Client(driver=driver, bot=bot, admin=int(os.getenv("ADMIN_ID"))).register_handlers_client(dp)
    Admin(id=int(os.getenv("ADMIN_ID")), bot=bot, driver=driver)
    executor.start_polling(dp, skip_updates=True)