from django import forms
from main.models import *


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = Message
        fields =['chat_id','file','message_id','owner','user','text','msg_type']