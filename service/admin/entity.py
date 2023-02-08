from aiogram import types, Dispatcher
from adadb import OrderRepos



class Admin(object):
    def __init__(self, id, bot, driver):
        self.id = id
        self.bot = bot
        self.order = OrderRepos(driver)
    
    async def add_free_order(self, message: types.Message):
        self.order.add_order(1675722615)
        if message.from_user.id == self.id:
            await message.answer(f"Запись успешно создана!")
            return
        await message.answer("К сожалению, вы не админ;(")

    def register_handlers_admin(self, dp:Dispatcher):
        dp.register_message_handler(self.add_free_order, text='free')