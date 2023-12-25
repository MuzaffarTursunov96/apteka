from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from main import dp,bot
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

menu_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('🔎 Qidirish')
).add(
    KeyboardButton('👨‍💻 Operator bilan bog\'lanish'),
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

shaxarlar =['Toshkent','Namangan','Andijon','Fargona','Jizzax']

buttons2 = [types.KeyboardButton(option) for option in shaxarlar]

shaxar_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
  *buttons2 
)

tumanlar =['Norin','Pop','uchqorgon','vahokazo']

buttons3 = [types.KeyboardButton(option) for option in tumanlar]

tuman_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
  *buttons3 
)












