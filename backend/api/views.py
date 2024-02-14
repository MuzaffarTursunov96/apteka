from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication, permissions
from bot.models import User,Viloyatlar
from main.models import TelegramUser,Message
from .serializers import UserSerializer,ViloyatSerializer,TelegramUserSerializer,MessageSerializer,ClientSerializer,OperatorSerializer
from django.http import JsonResponse
import requests as rq
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import websocket
import json
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import asyncio
from .forms import FileUploadForm
from PIL import Image
from config.settings import MEDIA_ROOT
import os
from django.core.files.base import ContentFile
from decouple import config

def hodimlar_save(APIView):
    serializer_class = OperatorSerializer
    queryset = User.objects.all()
    permission_classes =[permissions.AllowAny]

    def post(self,request):
        print(request.data)
        return Response({'data':'a'})
    

def operator_save(APIView):
    serializer_class = OperatorSerializer
    queryset = User.objects.all()
    permission_classes =[permissions.AllowAny]

    def post(self,request):
        print(request.data)
        return Response({'data':'a'})


def send_message_to_websocket(websocket_url,data):
    print(websocket_url)
    ws = websocket.WebSocket()
    ws.connect(websocket_url)
    ws.send(json.dumps(data))
    response = ws.recv()
    # print(response)
    ws.close()

class ListOperators(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes =[permissions.AllowAny]

    def get(self,request,region_name):
        queryset = User.objects.filter(viloyat__name__icontains =region_name,is_active=True,role=3)
        serializer= UserSerializer(queryset,many=True)
        return Response(data=serializer.data)


class ListViloyatlar(APIView):
    serializer_class = ViloyatSerializer
    queryset = Viloyatlar.objects.all()
    permission_classes =[permissions.AllowAny]

    def get(self,request):
        queryset = Viloyatlar.objects.all()
        serializer= ViloyatSerializer(queryset,many=True)
        return Response(data=serializer.data)

import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))
    
   
@csrf_exempt
def user_message_receive(request):
    websocket_url ='ws://54.210.252.107:8001/ws/messages/'
    # websocket_url =config('WEBSOCKET_URL')
    #config('WEBSOCKET_URL')
    
    if request.method =='POST':
        data = dict(request.POST)
        chat_id = 0
        message_id =0
        user_id =1
        text =''
        owner =3
       
        

        if 'chat_id' in data:
            chat_id = data['chat_id'][0]
        if 'message_id' in data:
            message_id = data['message_id'][0]
        if 'user_id' in data:
            user_id = data['user_id'][0]
            user = TelegramUser.objects.get(user_id=user_id)
            user.count_message_saw += 1
            user.updated_at =datetime.now()
            user.save()
        if 'text' in data:
            text = data['text'][0]
        
        
        
        
        if 'file' in data:
            file_path =data['file'][0]
            bot_token = config('API_TOKEN')
            file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
            response = rq.get(file_url)
           
            message = Message(
                chat_id =chat_id,
                message_id=message_id,
                user=user,
                text=text,
                owner=owner,
                msg_type=data['msg_type'][0]
            )
            message.save()
            message.file.save(str(randomword(10))+str(file_path.split('/')[-1]), ContentFile(response.content), save=True)
        else:
            message = Message(
                chat_id =chat_id,
                message_id=message_id,
                user=user,
                text=text,
                owner=owner,
                msg_type=data['msg_type'][0]
            )
            message.save()
        
        
        data ={
            'chat_id':chat_id,
            'message_id':message_id,
            'user_id':user_id,
            'text':text,
            'msg_type':data['msg_type'][0],
            'owner':owner,
            'image':str(user.image),
            'username':user.first_name,
            'file':str(message.file)
        }
        print(data,'<<<<<<'*10)
        websocket_url +=str(user.operator.id)+'/'
        print(websocket_url)
        send_message_to_websocket(websocket_url,data=data)
        
        return JsonResponse({'message':'Successfully saved!'})

    else:
        return JsonResponse({'msg':'GET method not allowed!'})



@csrf_exempt
def TelegramUserSave(request):
    if request.method =='POST':
        data = dict(request.POST)
        username =''
        first_name =''
        last_name =''
        operator_id = 1
        image = ''
        if 'username' in data:
            username = data['username'][0]
        if 'first_name' in data:
            first_name = data['first_name'][0]
        if 'last_name' in data:
            last_name = data['last_name'][0]
        if 'operator_id' in data:
            operator_id = data['operator_id'][0]
        if 'image' in data:
            # image = data['image'][0]
            
            file_path =data['image'][0]
            bot_token = config('API_TOKEN')
            file_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
            response = rq.get(file_url)

        if 'user_id' in data:
            user_exists = TelegramUser.objects.filter(user_id=data['user_id'][0]).exists()
            if user_exists:
                teleg_user = TelegramUser.objects.filter(user_id=data['user_id'][0])[:1].get()
                teleg_user.username =username
                teleg_user.first_name =first_name
                teleg_user.last_name =last_name
                teleg_user.save()
                if 'man.png' not in file_path:
                    teleg_user.image.save(str(randomword(10))+str(file_path.split('/')[-1]), ContentFile(response.content), save=True)
                else:
                    teleg_user.image.save(str(file_path.split('/')[-1]), ContentFile(response.content), save=True)
                return JsonResponse({'msg':'User updated'})
            else:
                operator = User.objects.get(id=operator_id)
                operator.client_count +=1
                operator.save()
                user =TelegramUser(
                    user_id =data['user_id'][0],
                    username =username,
                    first_name=first_name,
                    last_name=last_name,
                    operator=operator
                )
                user.save()
                if 'man.png' not in file_path:
                    user.image.save(str(randomword(10))+str(file_path.split('/')[-1]), ContentFile(response.content), save=True)
                else:
                    user.image.save(str(file_path.split('/')[-1]), ContentFile(response.content), save=True)
                return JsonResponse({'msg':'User created'})
        
        else:
            return JsonResponse({'msg':'User not found.'})
    else:
        return JsonResponse({'msg':'get method not allowed.'})




def messages_all(request,id):
    
    messages =Message.objects.filter(user__user_id =id).order_by('-created_at')[:10][::-1]
    user = TelegramUser.objects.get(user_id = id)
    user.count_message_saw = 0
    user.save()

    message_serializer = MessageSerializer(messages,many=True)
    client_serializer = ClientSerializer(user)

    return JsonResponse({'client':client_serializer.data,'messages':message_serializer.data})    
    

def get_operator_id(request,id):
    
    operator_id = TelegramUser.objects.get(user_id = id).operator.id

    return JsonResponse({'operator_id':operator_id})   

def is_photo(file_path):
    try:
        # Open the file using Pillow
        img = Image.open(file_path)

        # Check if the file is a recognized image format
        return img.format is not None

    except Exception as e:
        # Handle the case where the file is not a photo or cannot be opened
        print(f"Error checking file: {e}")
        return False 
    

@csrf_exempt    
def send_message_to_client(request):
    if request.method =='POST':
        data = request.POST
        _mutable = data._mutable

        data._mutable = True
        chat = Message.objects.filter(user__user_id =int(data['user_id']))[:1].get()
        data['chat_id'] = chat.chat_id
        data['message_id'] = chat.message_id
        data['user'] = chat.user
        data['owner'] = 2
        if 'file' in request.FILES:
            uploaded_file = str(request.FILES['file'])

            path = os.path.join(MEDIA_ROOT,uploaded_file)
            check_photo = is_photo(path)
            if check_photo:
                msg_type ='photo'
            else:
                msg_type ='document'
            text =uploaded_file
        else:
            text =data['text']
            msg_type ='text'

        data['msg_type'] = msg_type
        

        data._mutable = _mutable
        form = FileUploadForm(data,request.FILES)
        file_form =None
        if form.is_valid():
            print('valid')
            file_form = form.save()
        else:
            print('helllo',form.errors)
        send_message_to_aiogram(request,data['chat_id'],data['text'],msg_type,file_form.file)
        
    return JsonResponse({'msg':False,'text':text,'msg_type':msg_type})


def send_message_to_aiogram(request,chat_id,text,smg_type,file_path=None):

    bot_token = config('API_TOKEN')
    if smg_type =='text':
        if request.user.get_role() =='admin': 
            text ='<em><b>Admin:</b></em>\n' +text
        elif request.user.get_role() =='operator':
            text ='<em><b>Asosiy operator:</b></em>\n' +text
        else:
            text =f'<em>{text}</em>'

        payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode':'HTML'
        }
        
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        response = rq.post(url, json=payload)
    else:
        url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
        with open(os.path.join(MEDIA_ROOT,str(file_path)), 'rb') as file:
            files = {'document': file}
            data = {'chat_id': chat_id, 'caption': ''}

            response = rq.post(url, files=files, data=data)

    
    if response.status_code == 200:
        print('Message sent successfully')
        return True
    else:
        return False
    

    