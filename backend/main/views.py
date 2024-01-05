from django.shortcuts import render
from .models import Message,TelegramUser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    return render(request,'index.html')



def chat_operator(request):
    
    users = TelegramUser.objects.all()#filter(operator =request.user)
    context ={
        'users':users
    }
    return render(request,'operator/chat.html',context)





def chat_box(request, chat_box_name):
    # we will get the chatbox name from the url
    print(chat_box_name)
    return render(request, "chatbox.html", {"chat_box_name": chat_box_name})