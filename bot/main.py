import asyncio
from typing import Optional
import aiogram
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from keyboards.keyboard import *
from string import ascii_letters

API_TOKEN = '6918479750:AAHcV4liDF29Y10uIqxVDTD0-PsBOkZFXY8'

loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN, loop=loop)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    lang = State()
    menu = State()  
    dori_nomi = State() 
    addresslar = State()  

class Address(StatesGroup):
    shaxar = State()
    tuman = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.lang.set()
    return await bot.send_message(text='<em>Assalomu alaykum bizning <b>apteka botga</b> hushkelibsiz,\n iltimos tilni tanlang</em>',chat_id=message.chat.id,reply_markup=lang_markup,parse_mode='HTML')
    

@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if raw_state is None:
        return
    await state.finish()
    await message.reply('Canceled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.lang)
async def process_name(message: types.Message, state: FSMContext):
    print('lang')
    async with state.proxy() as data:
        data['lang'] = message.text

    await Form.next()
    await bot.send_message(text='<em>Iltimos dorini <b>nomini</b> qidirish uchun yozing \n yoki 📱 <b>menu</b>ni tanlang.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')



@dp.message_handler(lambda message: True if message.text not in ['🔎 Qidirish','🔄 Tilni o\'zgartirish','👨‍💻 Operator bilan bog\'lanish','⚧ Joylashuv'] and (not isinstance(message.text , str)) else False , state=Form.menu)
async def failed_process_age(message: types.Message):
    return await bot.send_message(text='<em>📱 Iltimos <b>menu</b> bolimidan tanlang yoki dorini <b>nomini</b> kiriting.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')

@dp.message_handler(state=Form.menu)
async def process_name(message: types.Message, state: FSMContext):
    print('menu')
    async with state.proxy() as data:
        if message.text in ['🔄 Tilni o\'zgartirish','👨‍💻 Operator bilan bog\'lanish','⚧ Joylashuv']:
            if message.text =='🔄 Tilni o\'zgartirish':
                await Form.lang.set()
                return await bot.send_message(text='Tilni tanlang',chat_id=message.chat.id,reply_markup=lang_markup)
            elif message.text =='👨‍💻 Operator bilan bog\'lanish':
                return await bot.send_message(text='Hurmatli foydalanuvchi, ushbu bot orqali taklif va mulohazalaringizni yo\'llashingiz mumkin. <b>👉@fargona_apteka_bot</b>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
            elif message.text =='⚧ Joylashuv':
                await Address.shaxar.set()
                return await bot.send_message(text='<b>Shaxarni</b> tanlang',chat_id=message.chat.id,reply_markup=shaxar_markup,parse_mode='HTML')
        else:
            data['dorini_nomi'] = message.text
            if message.text =='🔎 Qidirish':
                await Form.menu.set()
                await message.reply('Iltimos dorini <b>nomini</b> kiriting!',reply_markup=menu_markup,parse_mode='HTML')
            else:
                await Form.dori_nomi.set()
                return await bot.send_message(text='Qidiruvdan chiqgan natija',chat_id=message.chat.id,reply_markup=dorilar_markup)




# @dp.message_handler(lambda message: isinstance(message.text,str) , state=Form.dori_nomi)
# async def failed_process_dorini_nomi(message: types.Message):
#     return await bot.send_message(text='Iltimos menu dan tanlang yoki dorini nomini kiriting.',chat_id=message.chat.id,reply_markup=menu_markup)

@dp.message_handler(state=Form.dori_nomi)
async def process_age(message: types.Message, state: FSMContext):
    print('dori_nomi')
    if message.text =='🏛 Uyga qaytish':
        await Form.previous()
        return await bot.send_message(text='<em>📱 Iltimos <b>menu</b> bolimidan dan tanlang yoki dorini <b>nomini</b> kiriting.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
    else:
        async with state.proxy() as data:
            if ('shaxar' not in data) or  ('tuman' not in data):
                await Address.shaxar.set()
                # return await bot.send_message(text='<b>Shaxarni</b> tanlang',chat_id=message.chat.id,reply_markup=shaxar_markup,parse_mode='HTML')
                return await bot.send_message(text='<b>Manzilni kiriting.</b>',chat_id=message.chat.id,reply_markup=buyurtma_markup,parse_mode='HTML')
            else:
                await Form.menu.set()
                await message.reply("Qidiruvdan chiqgan natija", reply_markup=dorilar_markup)




@dp.message_handler(state=Address.shaxar)
async def process_shaxar(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['shaxar'] = message.text
        # if message.text =='Locatsiyani jonatish':
        #     # await bot.send_location(chat_id=message.chat.id)
        #     print(message.text)
    await Address.tuman.set()
    return await bot.send_message(text='<em>📱 Iltimos menu bolimidan dan tanlang yoki dorini <b>nomini</b> kiriting.</em>',chat_id=message.chat.id,reply_markup=tuman_markup,parse_mode='HTML')

@dp.message_handler(state=Address.tuman)
async def process_tuman(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tuman'] = message.text
    await state.finish()
    await Form.menu.set()
    return await bot.send_message(text='<em>📱 Iltimos <b>menu</b> dan tanlang yoki dorini <b>nomini</b> kiriting.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
    
# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     print('gender')
#     async with state.proxy() as data:
#         data['gender'] = message.text

#         # Remove keyboard
#         markup = types.ReplyKeyboardMarkup().add(KeyboardButton('🏛 Uyga qaytish'))

#         # And send message
#         await bot.send_message(message.chat.id, md.text(
#             md.text('Hi! Nice to meet you,', md.bold(data['dori_nomi'])),
#             # md.text('Age:', data['age']),
#             # md.text('Gender:', data['gender']),
#             sep='\n'), reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

#         # Finish conversation
#         data.state = None




if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)