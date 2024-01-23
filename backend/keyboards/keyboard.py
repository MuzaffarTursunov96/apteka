from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from main_bot import dp,bot
from aiogram import types







button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')

markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

markup4 = ReplyKeyboardMarkup().row(
    button1, button2, button3
)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)


lang_markup =ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(
    KeyboardButton('🇺🇿 Uz'),
    KeyboardButton('🇷🇺 Ru'),
    # KeyboardButton('Eng')  
)
start_markup =ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(
    KeyboardButton('/start'), 
)

menu_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('👨‍💻 Operator bilan bog\'lanish'),
    KeyboardButton('🔄 Tilni o\'zgartirish'),
)
menu_markup_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('👨‍💻 Свяжитесь с оператором'),
    KeyboardButton('🔄 Изменить язык'),
)

menu_markup2 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('🔄 Tilni o\'zgartirish'),
)
options =['🏛 Uyga qaytish','AAAAA','BBBBBB','CCCCCCCC','DDDDDDD']

buttons = [types.KeyboardButton(option) for option in options]

dorilar_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
  *buttons 
)



buyurtma_markup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    KeyboardButton('🛒 Buyurtma berish'),
    KeyboardButton('⬅️ Orqaga'),
)






operator_menu = InlineKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    InlineKeyboardButton(text='Yangi xabarlar',callback_data='a'),InlineKeyboardButton(text='O\'qilganlar',callback_data='b')
)








