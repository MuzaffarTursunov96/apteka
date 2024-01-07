from django.shortcuts import render,redirect
from .models import Message,TelegramUser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.contrib import auth,messages

# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request,'index.html')


@login_required(login_url='/accounts/login/')
def chat_operator(request):
    
    users = TelegramUser.objects.all().order_by('-created_at')#filter(operator =request.user)
    
    for user in users:
        print(user.messages,'&&&&&&&&&&&')
        # for mes in user.messages:
        #     print(mes,user.id)

    context ={
        'users':users,
        
    }
    return render(request,'operator/chat.html',context)





def chat_box(request, chat_box_name):
    # we will get the chatbox name from the url
    print(chat_box_name)
    return render(request, "chatbox.html", {"chat_box_name": chat_box_name})



def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    elif request.method =='POST':
        email =request.POST.get('email',None)
        password =request.POST.get('password',None)
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Password or e-mail incorrect!')
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')