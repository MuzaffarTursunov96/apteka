from rest_framework import serializers
from main.models import TelegramUser,Message
from bot.models import Viloyatlar,User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','last_name']

class ViloyatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Viloyatlar
        fields = ['id','name']


class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = ['user_id','username','first_name','last_name','operator','image']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['chat_id','message_id','text','owner']


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = ['username','first_name','image','user_id']


class JoinedSerializer(serializers.Serializer):
    model_message = MessageSerializer()
    model_user = ClientSerializer()