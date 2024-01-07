from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework import authentication, permissions
from bot.models import User,Viloyatlar
from main.models import TelegramUser,Message
from .serializers import UserSerializer,ViloyatSerializer,TelegramUserSerializer,MessageSerializer,ClientSerializer
from django.http import JsonResponse
import requests as rq
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import websocket
import json
from datetime import datetime






def send_message_to_websocket(websocket_url,data):
    ws = websocket.WebSocket()
    ws.connect(websocket_url)
    ws.send(json.dumps(data))
    response = ws.recv()
    print(response)
    ws.close()

class ListOperators(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes =[permissions.AllowAny]

    def get(self,request,region_name):
        queryset = User.objects.filter(viloyat__name__icontains =region_name)
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
    
@csrf_exempt
def user_message_receive(request):
    websocket_url ='ws://127.0.0.1:8000/ws/messages/'
    if request.method =='POST':
        data = dict(request.POST)
        chat_id = 0
        message_id =0
        user_id =1
        text =''
        owner =3
        operator_id = 1
        if 'chat_id' in data:
            chat_id = data['chat_id'][0]
        if 'message_id' in data:
            message_id = data['message_id'][0]
        if 'user_id' in data:
            user_id = data['user_id'][0]
            user = TelegramUser.objects.get(user_id=user_id)
            user.updated_at =datetime.now()
            user.save()
        if 'text' in data:
            text = data['text'][0]
        

        message = Message(
            chat_id =chat_id,
            message_id=message_id,
            user=user,
            text=text,
            owner=owner
        )
        message.save()

        data ={
            'chat_id':chat_id,
            'message_id':message_id,
            'user_id':user_id,
            'text':text,
            'owner':owner,
            'image':str(user.image),
            'username':user.first_name
        }
        websocket_url +=str(user.operator.id)+'/'
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
            image = data['image'][0]

        if 'user_id' in data:
            user_exists = TelegramUser.objects.filter(user_id=data['user_id'][0]).exists()
            if user_exists:
                teleg_user = TelegramUser.objects.filter(user_id=data['user_id'][0])[:1].get()
                teleg_user.username =username
                teleg_user.first_name =first_name
                teleg_user.last_name =last_name
                teleg_user.image =image
                teleg_user.save()
                return JsonResponse({'msg':'User updated'})
            else:
                operator = User.objects.get(id=operator_id)
                TelegramUser(
                    user_id =data['user_id'][0],
                    username =username,
                    first_name=first_name,
                    last_name=last_name,
                    operator=operator,
                    image =image
                ).save()
                return JsonResponse({'msg':'User created'})
        
        else:
            return JsonResponse({'msg':'User not found.'})
    else:
        return JsonResponse({'msg':'get method not allowed.'})




def messages_all(request,id):
    
    messages =Message.objects.filter(user__user_id =id).order_by('-created_at')[:10][::-1]
    user = TelegramUser.objects.get(user_id = id)


    message_serializer = MessageSerializer(messages,many=True)
    client_serializer = ClientSerializer(user)

    return JsonResponse({'client':client_serializer.data,'messages':message_serializer.data})    
    

def get_operator_id(request,id):
    
    operator_id = TelegramUser.objects.get(user_id = id).operator.id

    return JsonResponse({'operator_id':operator_id})    

@csrf_exempt    
def send_message_to_client(request):
    if request.method =='POST':
        data = dict(request.POST)
        chat_id = Message.objects.filter(user__user_id =int(data['user_id'][0]))[:1].get().chat_id
        sended = send_message_to_aiogram(chat_id=chat_id,text=data['message'][0])
        if sended:
            return JsonResponse({'msg':True})
    return JsonResponse({'msg':False})

def send_message_to_aiogram(chat_id,text):
    bot_token = '6918479750:AAFm4eunDMv6IHZaAHv7w_YDup-VSL7YhHA'  
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    response = rq.post(url, json=payload)
    if response.status_code == 200:
        print('Message sent successfully')
        return True
    else:
        print('Failed to send message:', response.text)
        return False