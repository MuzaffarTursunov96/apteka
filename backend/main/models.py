from django.db import models
from bot.models import User
import uuid
# Create your models here.
class TelegramUser(models.Model):
    user_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,blank=True)
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    operator = models.ForeignKey(User,on_delete= models.CASCADE)
    image = models.ImageField(upload_to='uploads/images/',default='uploads/images/man.png')
    count_message_saw = models.SmallIntegerField(default=0)
    firma_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.last_name !=None and self.last_name!='None':
            if self.firma_name:
                return f'{self.first_name} {self.last_name} {self.firma_name}'
            else:
                return f'{self.first_name} {self.last_name}'
        else:
            if self.firma_name:
                return f'{self.first_name} {self.firma_name}'
            return self.first_name


MESSAGE_OWNER =(
    (1,'admin'),
    (2,'operator'),
    (1,'client'),
) 

class Message(models.Model):
    chat_id = models.IntegerField()
    message_id = models.IntegerField()
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE,related_name='messages')
    text = models.TextField(blank=True,null=True,default='')
    file = models.FileField(blank=True,null=True,upload_to='uploads/')
    owner = models.SmallIntegerField()
    saw = models.SmallIntegerField(default=0)
    msg_type = models.CharField(max_length =255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'