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
import aiohttp
import os 
import string
import random
import requests as rq
from aiogram.types import ContentType
from decouple import config


from aiohttp import web

API_TOKEN = config('API_TOKEN')

loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN, loop=loop)





webhook_path = f'/{API_TOKEN}'

base_url ='https://f474-188-113-204-5.ngrok-free.app'
local_url ='http://127.0.0.1:8000'


websocket_connection = None
# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
app = web.Application()


STATES = {
    'LANG':'lan',
    'START': 'start',
    'LANGUAGE': 'lang',
    'MENU': 'menu',
    'VILOYAT': 'viloyat',
    'OPERATOR': 'operator',
    'BACK':'back',
    'FINISH':'finish'
}

user_states = {}
      



async def set_webhook():
    webhhok_uri =f'{base_url}{webhook_path}'
    await bot.set_webhook(
        webhhok_uri
    )
    

async def on_startup(_):
    await set_webhook()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
   
    # if message.from_user.id in operator_ids:
        # return await bot.send_message(text='<em>Assalomu alaykum hushkelibsiz!</em>',chat_id=message.chat.id,reply_markup=operator_menu,parse_mode='HTML')
    user_states[message.chat.id] = STATES['LANGUAGE']
    # await Form.lang.set()
    return await bot.send_message(text='<em>Assalomu alaykum bizning <b>apteka botga</b> hushkelibsiz,\n iltimos tilni tanlang</em>',chat_id=message.chat.id,reply_markup=lang_markup,parse_mode='HTML')
    
async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    
    if token == API_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp.process_update(update)
        return web.Response()

    else:
        return web.Response(status=403)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if raw_state is None:
        return
    await state.finish()
    await message.reply('Canceled.', reply_markup=types.ReplyKeyboardRemove())

real_operators={}
user_lang ={}

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # Includes uppercase letters, lowercase letters, and digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

@dp.message_handler(content_types=[ContentType.TEXT,ContentType.PHOTO,ContentType.DOCUMENT])
async def operator_start(message: types.Message):
    
    global real_operators
    state = user_states.get(message.chat.id)
    global user_lang
    
    

    if state == None:
        await bot.send_message(text='<em>Iltimos start buyrug\'ini bosing</em>',chat_id=message.chat.id,reply_markup=start_markup,parse_mode='HTML')
        
    if message.chat.id not in user_lang:
        user_lang[message.chat.id] ='uz'
        
    if state == STATES['LANGUAGE']:
        if message.text =='🇺🇿 Uz' or message.text =='🇷🇺 Ru':
            user_states[message.chat.id] = STATES['MENU']
            if message.text =='🇺🇿 Uz':
                user_lang[message.chat.id] = 'uz'
                await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan <b>menu</b>ingizni tanlang.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
            else:
                user_lang[message.chat.id] = 'ru'
                await bot.send_message(text='<em>Пожалуйста, выберите свое <b>меню</b> из списка ниже.</em>',chat_id=message.chat.id,reply_markup=menu_markup_ru,parse_mode='HTML')

        else:
            await bot.send_message(text='<em>Iltimos tilni tanlang</em>',chat_id=message.chat.id,reply_markup=lang_markup,parse_mode='HTML')
    if user_lang[message.chat.id] =='uz':
        if state == STATES['MENU']:
            # Process the age input and transition to the next state
            if message.text =='🔄 Tilni o\'zgartirish':
                user_states[message.chat.id] = STATES['LANGUAGE']
                await bot.send_message(text='<em>Iltimos tilni tanlang</em>',chat_id=message.chat.id,reply_markup=lang_markup,parse_mode='HTML')
            elif message.text =='🇺🇿 Uz' or message.text =='🇷🇺 Ru':
                await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan <b>menu</b>ingizni tanlang.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
            elif message.text =='👨‍💻 Operator bilan bog\'lanish':
                user_states[message.chat.id] = STATES['VILOYAT']
                viloyatlar2 = await get_viloyatlar()
                await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan <b>viloyat</b>ingizni tanlang.</em>',chat_id=message.chat.id,reply_markup=get_viloyat_markup(viloyatlar2),parse_mode='HTML')
            else:
                await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan <b>menu</b>ingizni tanlang.</em>',chat_id=message.chat.id,reply_markup=menu_markup,parse_mode='HTML')
        elif state == STATES['VILOYAT']:
            # Process the age input and transition to the next state
            
            viloyatlar2 = await get_viloyatlar()
            
            shaxarlar =[ vil['name'] for vil in viloyatlar2]
            if message.text in shaxarlar:
                operatorss = await operators(vil_name=message.text)
                
                if len(operatorss) < 1:
                    user_states[message.chat.id] = STATES['MENU']
                    return await bot.send_message(text='👩‍🚀 operator topilmadi, iltimos adminga murojat qilib ko\'ring.',chat_id=message.chat.id,reply_markup=menu_markup)

                
                operators_new ={}
                for o in operatorss:
                    operators_new[o['username']+'##'+o['last_name']]=o['id']
                real_operators[message.chat.id] = operators_new
                user_states[message.chat.id] = STATES['OPERATOR']

                await bot.send_message(text='Iltimos 👩‍🚀 operatorni tanlang.',chat_id=message.chat.id,reply_markup=get_operators(operatorss))
            else:
                await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan <b>viloyat</b>ingizni tanlang.</em>',chat_id=message.chat.id,reply_markup=get_viloyat_markup(viloyatlar2),parse_mode='HTML')
        elif state == STATES['OPERATOR']:
            user_key = message.text.split(' ')
            if len(user_key) >=2:
                name = user_key[0] +'##'+ user_key[1]
            else:
                name = user_key[0] +'##'+ 'qwerty'
            if name in real_operators[message.chat.id]:
                user_states[message.chat.id]=STATES['FINISH']
                UserProfilePhotos = await bot.get_user_profile_photos(user_id=message.from_user.id)
                img_path = 'uploads/images/man.png'
                if UserProfilePhotos.total_count > 0:
                    first_photo = UserProfilePhotos.photos[0][0]
                    file_id = first_photo.file_id

                    file = await bot.get_file(file_id)
                    file_path = file.file_path
                    
                    random_string =generate_random_string(10)
                    current_directory = os.getcwd()+f'\\media\\uploads\\images\\{message.from_user.id}{random_string}.jpg'
                    img_path =f'uploads\\images\\{message.from_user.id}{random_string}.jpg'
                    await bot.download_file(file_path, current_directory)
                teleg_user = message.from_user
                data ={
                    'user_id':teleg_user.id,
                    'username':teleg_user.username,
                    'first_name':teleg_user.first_name,
                    'last_name':teleg_user.last_name,
                    'operator_id':real_operators[message.chat.id][name],
                    'image':img_path
                }
                await telegram_user_save(data=data)
                remove_keyboard = ReplyKeyboardRemove()
                await bot.send_message(text="<em>Savollaringiz bolsa 👇 pastga yozing.</em>",chat_id=message.chat.id,reply_markup=remove_keyboard,parse_mode='HTML')
            else:
                if len(get_operators(real_operators[message.chat.id],older=True).keyboard) > 0:
                    await bot.send_message(text='Iltimos 👩‍🚀 operatorni tanlang.',chat_id=message.chat.id,reply_markup=get_operators(real_operators[message.chat.id],older=True))
                else:
                    user_states[message.chat.id] = STATES['MENU']
                    await bot.send_message(text='👩‍🚀 operator topilmadi, iltimos adminga murojat qilib ko\'ring.',chat_id=message.chat.id,reply_markup=menu_markup)
        elif state == STATES['FINISH']:
    
            file_type ='text'
            file_path =''
            if message.content_type == types.ContentType.TEXT:
                text = message.text
                
            elif message.photo:
                file_type ='photo'
                # Handle document/file message
                photo = message.photo[-1]
                text = photo.file_id

                file_info = await bot.get_file(photo.file_id)
                file_path =file_info.file_path
                # print(f"Received document/file with file_path: {file_path}")
                # You can use the file_id to download and save the file if needed
            elif message.document:
                file_type ='document'

                text = message.document.file_id
            

                file_info = await bot.get_file(message.document.file_id)
                file_path = file_info.file_path
                # Handle other content types as needed
                # print(f"Received message with content type: {file_path}")

        
            data ={
                'chat_id':message.chat.id,
                'message_id':message.message_id,
                'user_id':message.from_user.id,
                'text':text,
                'msg_type':file_type,
                'file':str(file_path),
            }
            await user_message_save(data=data) 
    
    else:
        if state == STATES['MENU']:
            # Process the age input and transition to the next state
            if message.text =='🔄 Изменить язык':
                user_states[message.chat.id] = STATES['LANGUAGE']
                await bot.send_message(text='<em>Пожалуйста, выберите язык</em>',chat_id=message.chat.id,reply_markup=lang_markup,parse_mode='HTML')
            elif message.text =='🇺🇿 Uz' or message.text =='🇷🇺 Ru':
                await bot.send_message(text='<em>Пожалуйста, выберите свое <b>меню</b> из списка ниже.</em>',chat_id=message.chat.id,reply_markup=menu_markup_ru,parse_mode='HTML')
            elif message.text =='👨‍💻 Свяжитесь с оператором':
                user_states[message.chat.id] = STATES['VILOYAT']
                viloyatlar2 = await get_viloyatlar()
                await bot.send_message(text='<em>Пожалуйста, выберите свою <b>регион</b> из списка ниже.</em>',chat_id=message.chat.id,reply_markup=get_viloyat_markup(viloyatlar2),parse_mode='HTML')
            else:
                await bot.send_message(text='<em>Пожалуйста, выберите свое <b>меню</b> из списка ниже.</em>',chat_id=message.chat.id,reply_markup=menu_markup_ru,parse_mode='HTML')
        elif state == STATES['VILOYAT']:
            # Process the age input and transition to the next state
            
            viloyatlar2 = await get_viloyatlar()
            
            shaxarlar =[ vil['name'] for vil in viloyatlar2]
            if message.text in shaxarlar:
                operatorss = await operators(vil_name=message.text)
                
                if len(operatorss) < 1:
                    user_states[message.chat.id] = STATES['MENU']
                    return await bot.send_message(text='👩‍🚀 Оператор не найден, обратитесь к администратору.',chat_id=message.chat.id,reply_markup=menu_markup_ru)

                
                operators_new ={}
                for o in operatorss:
                    operators_new[o['username']+'##'+o['last_name']]=o['id']
                real_operators[message.chat.id] = operators_new
                user_states[message.chat.id] = STATES['OPERATOR']

                await bot.send_message(text='Пожалуйста, выберите оператора 👩‍🚀.',chat_id=message.chat.id,reply_markup=get_operators(operatorss))
            else:
                await bot.send_message(text='<em>Пожалуйста, выберите свою <b>регион</b> из списка ниже.</em>',chat_id=message.chat.id,reply_markup=get_viloyat_markup(viloyatlar2),parse_mode='HTML')
        elif state == STATES['OPERATOR']:
            user_key = message.text.split(' ')
            if len(user_key) >=2:
                name = user_key[0] +'##'+ user_key[1]
            else:
                name = user_key[0] +'##'+ 'qwerty'
            if name in real_operators[message.chat.id]:
                user_states[message.chat.id]=STATES['FINISH']
                UserProfilePhotos = await bot.get_user_profile_photos(user_id=message.from_user.id)
                img_path = 'uploads/images/man.png'
                if UserProfilePhotos.total_count > 0:
                    first_photo = UserProfilePhotos.photos[0][0]
                    file_id = first_photo.file_id

                    file = await bot.get_file(file_id)
                    file_path = file.file_path
                    
                    random_string =generate_random_string(10)
                    current_directory = os.getcwd()+f'\\media\\uploads\\images\\{message.from_user.id}{random_string}.jpg'
                    img_path =f'uploads\\images\\{message.from_user.id}{random_string}.jpg'
                    await bot.download_file(file_path, current_directory)
                teleg_user = message.from_user
                data ={
                    'user_id':teleg_user.id,
                    'username':teleg_user.username,
                    'first_name':teleg_user.first_name,
                    'last_name':teleg_user.last_name,
                    'operator_id':real_operators[message.chat.id][name],
                    'image':img_path
                }
                await telegram_user_save(data=data)
                remove_keyboard = ReplyKeyboardRemove()
                await bot.send_message(text="<em>Если у вас есть вопросы, напишите их ниже.👇</em>",chat_id=message.chat.id,reply_markup=remove_keyboard,parse_mode='HTML')
            else:
                if len(get_operators(real_operators[message.chat.id],older=True).keyboard) > 0:
                    await bot.send_message(text='Пожалуйста, выберите оператора 👩‍🚀.',chat_id=message.chat.id,reply_markup=get_operators(real_operators[message.chat.id],older=True))
                else:
                    user_states[message.chat.id] = STATES['MENU']
                    await bot.send_message(text='👩‍🚀оператор не найден, обратитесь к администратору.',chat_id=message.chat.id,reply_markup=menu_markup_ru)
        elif state == STATES['FINISH']:
    
            file_type ='text'
            file_path =''
            if message.content_type == types.ContentType.TEXT:
                text = message.text
                
            elif message.photo:
                file_type ='photo'
                # Handle document/file message
                photo = message.photo[-1]
                text = photo.file_id

                file_info = await bot.get_file(photo.file_id)
                file_path =file_info.file_path
                # print(f"Received document/file with file_path: {file_path}")
                # You can use the file_id to download and save the file if needed
            elif message.document:
                file_type ='document'

                text = message.document.file_id
            

                file_info = await bot.get_file(message.document.file_id)
                file_path = file_info.file_path
                # Handle other content types as needed
                # print(f"Received message with content type: {file_path}")

        
            data ={
                'chat_id':message.chat.id,
                'message_id':message.message_id,
                'user_id':message.from_user.id,
                'text':text,
                'msg_type':file_type,
                'file':str(file_path),
            }
            await user_message_save(data=data) 
    


async def operators(vil_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/operators/'+vil_name) as response:
            data = await response.json()
    return data




async def user_message_save(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/user-message-receive',data=data) as response:
            data = await response.json()
    return data



async def telegram_user_save(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/telegram-user-save',data=data) as response:
            data = await response.json()
    return data



async def get_viloyatlar():
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/viloyatlar') as response:
            data = await response.json()
    return data

def get_viloyat_markup(viloyatlar)->ReplyKeyboardMarkup:
    shaxarlar =[ vil['name'] for vil in viloyatlar]
    buttons2 = [types.KeyboardButton(option) for option in shaxarlar]
    viloyat_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
    *buttons2 
    )
    return viloyat_markup




def get_operators(operatorlar,older=False)->ReplyKeyboardMarkup:
    if older:
        oper =[  key.replace('##',' ') for key,val in operatorlar.items()]
        buttons3 = [types.KeyboardButton(option) for option in oper]
        operator_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
        *buttons3 
        )
        return operator_markup
    else:
        oper =[ op['username'] +' ' +op['last_name'] for op in operatorlar]
        buttons3 = [types.KeyboardButton(option) for option in oper]
        operator_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
        *buttons3 
        )
        return operator_markup




app.router.add_post(f'/{API_TOKEN}',handle_webhook)


if __name__ == '__main__':
    # app.on_startup.append(on_startup)

    # web.run_app(
    #     app,
    #     host='0.0.0.0',
    #     port=8080
    # )
    executor.start_polling(dp, loop=loop, skip_updates=True)

