from aiogram.utils.callback_data import CallbackData

schedule = CallbackData('sub','date', sep="-")
agreement = CallbackData('agree', 'answer', 'id', 'date', sep='-')
messaging = CallbackData('message', "agreement", sep='-')