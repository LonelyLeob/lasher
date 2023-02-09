#main logistic file
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from adadb import FDatabase, user_exist
from service.customer.entity import Client
from service.customer.markup import ClientMarkup
from service.admin.entity import Admin
import os
from dotenv import load_dotenv
from utils.fsm import GuestState

load_dotenv()

bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())
driver = FDatabase(os.getenv("DB_NAME")).migration()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if user_exist(driver, message.from_user.id):
        await bot.send_message(message.from_user.id, f"Вы уже зарегистрированы, выберите запись на реснички:)", reply_markup=ClientMarkup().register())
        return
    await message.answer(f"Приветствую тебя {message.from_user.full_name}!\nЗдесь ты можешь записаться ко мне на реснички:)\nВведите реферальный код, если вас пригласил друг или /cancel, если вы просто хотите быть с нами;)")
    await GuestState().reffer_code.set()

if __name__ == '__main__':
    Client(driver=driver, bot=bot, admin=int(os.getenv("ADMIN_ID"))).register_handlers_client(dp=dp)
    Admin(id=int(os.getenv("ADMIN_ID")), bot=bot, driver=driver).register_handlers_admin(dp=dp)
    executor.start_polling(dp, skip_updates=True)