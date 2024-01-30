from django.shortcuts import render,redirect,get_object_or_404
from .models import Message,TelegramUser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max,Count,Q,Prefetch,Sum
from django.contrib.auth.decorators import login_required
from django.contrib import auth,messages
from .models import User
from bot.models import Viloyatlar
from django.core.paginator import Paginator
from .forms import OperatorForm
from django.http import HttpResponseForbidden
from django.http import FileResponse
from telegram import Bot
from django.http import HttpResponse
import asyncio
from asgiref.sync import async_to_sync
from decouple import config

from django.views.decorators.csrf import csrf_protect

# Create your views here.

def chat2(request):
    return render(request,'operator/chat2.html')

@login_required(login_url='/accounts/login/')
def index(request):
    return render(request,'index.html')


@login_required(login_url='/accounts/login/')
def chat_operator(request):
    
    users = TelegramUser.objects.filter(operator = request.user)

    context ={
        'users':users,
        
    }
    return render(request,'operator/chat.html',context)




@login_required(login_url='/accounts/login/')
def chat_box(request, chat_box_name):
    # we will get the chatbox name from the url
    print(chat_box_name)
    return render(request, "chatbox.html", {"chat_box_name": chat_box_name})


@csrf_protect
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

def registration(request):
    if request.method == 'POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        if data['password'] != data['password2']:
            return HttpResponseForbidden('Password did\'nt match')
        user = User(
            username =data['username'],
            last_name =data['last_name'],
            email =data['email'],
            phone_number =data['phone_number'],
            role =role,
            viloyat =viloyat
            )
        
        
        user.save()
        user.set_password(data['password'])
        user.save()
        return redirect('login')
    viloyatlar = Viloyatlar.objects.all()
    context ={
        'viloyatlar':viloyatlar
    }
    return render(request,'accounts/registration.html',context)

@login_required(login_url='/accounts/login/')
def message_admin(request):
    
    return render(request,'admin/chat.html')

@login_required(login_url='/accounts/login/')
def message_show(request,id):
    
    teleg_user_id = request.GET.get('user_id',None)
    user = User.objects.get(id=id)
    users = TelegramUser.objects.filter(operator =user)
    messagess = None
    telegram_user = None
    if teleg_user_id:
        messagess = Message.objects.filter(user__user_id = int(teleg_user_id))
        telegram_user = TelegramUser.objects.get(user_id = int(teleg_user_id))

    
    context ={
        'users':users,
        'messages':messagess,
        'telegram_user':telegram_user,
        'operator_id':id
    }
    return render(request,'admin/chat.html',context)

@login_required(login_url='/accounts/login/')
def message_show_for_staff(request,id):
    
    teleg_user_id = request.GET.get('user_id',None)
    user = User.objects.get(id=id)
    users = TelegramUser.objects.filter(operator =user)
    messagess = None
    telegram_user = None
    if teleg_user_id:
        messagess = Message.objects.filter(user__user_id = int(teleg_user_id))
        telegram_user = TelegramUser.objects.get(user_id = int(teleg_user_id))

    
    context ={
        'users':users,
        'messages':messagess,
        'telegram_user':telegram_user,
        'operator_id':id
    }
    return render(request,'base_operator/chat.html',context)

@login_required(login_url='/accounts/login/')
def xodim_list(request):

    
    operators = User.objects.filter(viloyat__name =request.user.viloyat,is_active=True,role=3)
    

    paginator = Paginator(operators, 25)

    if request.GET.get('page') != None:
        page_number = request.GET.get('page')
    else:
        page_number=1
    
    page_obj = paginator.get_page(page_number)


     
    count_of_client = User.objects.filter(viloyat__name =request.user.viloyat,is_active=True,role=3).aggregate(clientt_count = Sum('client_count'))['clientt_count']

    if not count_of_client:
        count_of_client = 0
    viloyatlar = Viloyatlar.objects.all()
    context ={
        'operators': page_obj,
        'viloyatlar':viloyatlar,
        'count_of_client':count_of_client
    }
   
    return render(request,'base_operator/operator_list.html',context)


@login_required(login_url='/accounts/login/')
def teamlead_list(request):

    viloyat =request.GET.get('viloyat',None)
    if viloyat:
        operators = User.objects.filter(viloyat__name =viloyat,is_active=True,role=2)
    else:
        operators = User.objects.filter(role=2)

    paginator = Paginator(operators, 25)

    if request.GET.get('page') != None:
        page_number = request.GET.get('page')
    else:
        page_number=1
    
    page_obj = paginator.get_page(page_number)

    viloyatlar = Viloyatlar.objects.all()
    context ={
        'operators': page_obj,
        'viloyatlar':viloyatlar
    }
   
    return render(request,'admin/operator_list.html',context)

@login_required(login_url='/accounts/login/')
def client_list(request):


    viloyat =request.GET.get('viloyat',None)
    username =request.GET.get('username',None)
    firma_nomi =request.GET.get('firma',None)
    operator =request.GET.get('operator',None)

    clients = TelegramUser.objects.all()
    
    if viloyat:
        clients = clients.filter(operator__viloyat__name =viloyat)

    if username:
        clients = clients.filter(Q(username__icontains = username)|Q(first_name__icontains =username)|Q(last_name__icontains =username))
    
    if firma_nomi:
        clients = clients.filter(firma_name__icontains =firma_nomi)

    if operator:
        clients = clients.filter(operator__username__icontains =firma_nomi)

        

    paginator = Paginator(clients, 25)

    if request.GET.get('page') != None:
        page_number = request.GET.get('page')
    else:
        page_number=1
    
    page_obj = paginator.get_page(page_number)

    operator_list = User.objects.filter(role=3,is_active=True)

    viloyatlar = Viloyatlar.objects.all()
    context ={
        'clients': page_obj,
        'viloyatlar':viloyatlar,
        'operator_list':operator_list
    }
   
    return render(request,'admin/client_list.html',context)

@login_required(login_url='/accounts/login/')
def xodim_edit(request,id):
    user = get_object_or_404(User,id=id)
    if request.method =='POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        active = request.POST.get('is_active',None)
         
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        
        user.username =data['username']
        user.last_name =data['last_name']
        user.email =data['email']
        user.phone_number =data['phone_number']
        user.role =int(role)
        if active:
            if active =='checked' or active =='on':
                user.is_active =True
        else:
            user.is_active =False

        user.viloyat =viloyat
        user.save()
        
        return redirect('hodim_list')
    context ={
        'user':user,
        'viloyatlar':Viloyatlar.objects.all()
    }

    return render(request,'base_operator/hodim_edit.html',context)

@login_required(login_url='/accounts/login/')
def hodim_edit(request,id):
    user = get_object_or_404(User,id=id)
    if request.method =='POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        active = request.POST.get('is_active',None)
         
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        
        user.username =data['username']
        user.last_name =data['last_name']
        user.email =data['email']
        user.phone_number =data['phone_number']
        user.role =int(role)
        if active:
            if active =='checked' or active =='on':
                user.is_active =True
        else:
            user.is_active =False

        user.viloyat =viloyat
        user.save()
        
        return redirect('operator_list')
    context ={
        'user':user,
        'viloyatlar':Viloyatlar.objects.all()
    }

    return render(request,'admin/hodim_edit.html',context)

@login_required(login_url='/accounts/login/')
def teamlead_edit(request,id):
    user = get_object_or_404(User,id=id)
    if request.method =='POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        active = request.POST.get('is_active',None)
         
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        
        user.username =data['username']
        user.last_name =data['last_name']
        user.email =data['email']
        user.phone_number =data['phone_number']
        user.role =int(role)
        if active:
            if active =='checked' or active =='on':
                user.is_active =True
        else:
            user.is_active =False

        user.viloyat =viloyat
        user.save()
        return redirect('teamlead_list')
    context ={
        'user':user,
        'viloyatlar':Viloyatlar.objects.all()
    }

    return render(request,'admin/teamlead_edit.html',context)


async def get_file_path(file_id):
    
    API_TOKEN = config('API_TOKEN')
    bot = Bot(token=API_TOKEN)
    file_info = await bot.get_file(file_id)
    return file_info.file_path


async def download_file(request, file_id):
    file_path = await get_file_path(file_id)
    import requests as rq
    file_response = rq.get(file_path)

    if file_response.ok:
        # Return the file as a Django HttpResponse
        response = HttpResponse(file_response.content, content_type=file_response.headers['Content-Type'])
        response['Content-Disposition'] = f'attachment; filename="{file_path.split("/")[-1]}"'
        return response
    else:
        return HttpResponse(f"Error downloading file: {file_response.status_code}", status=500)





@login_required(login_url='/accounts/login/')
def client_edit(request,id):
    user = get_object_or_404(TelegramUser,user_id=id)
    if request.method =='POST':
        last_name = request.POST.get('last_name',None)
        username = request.POST.get('username',None)
        firma_name = request.POST.get('firma_name')
        operator_id = request.POST.get('operator')
         
        operator = User.objects.get(id =int(operator_id) )
        user.last_name =last_name
        user.username =username
        user.firma_name =firma_name
        user.operator = operator
        user.save()
        return redirect('client_list')
    operators = User.objects.filter(role =3)
    context ={
        'user':user,
        'operators':operators
    }

    return render(request,'admin/client_edit.html',context)


@login_required(login_url='/accounts/login/')
def operatorlist(request):

    viloyat =request.GET.get('viloyat',None)
    operator_id =request.GET.get('operator_id',None)
    if viloyat:
        operators =User.objects.filter(role=3,viloyat__name =viloyat)
    else:
        operators = User.objects.filter(role =3)

    if operator_id:
        operator = User.objects.get(id =int(operator_id))
        operators = operators.filter(viloyat =operator.viloyat) 
    count_of_client = operators.aggregate(clientt_count = Sum('client_count'))['clientt_count']

    paginator = Paginator(operators, 25)

    if request.GET.get('page') != None:
        page_number = request.GET.get('page')
    else:
        page_number=1
    
    page_obj = paginator.get_page(page_number)

    viloyatlar = Viloyatlar.objects.all()
    context ={
        'operators': page_obj,
        'viloyatlar':viloyatlar,
        'count_of_client':count_of_client
    }
   
    return render(request,'admin/user_list.html',context)



@login_required(login_url='/accounts/login/')
def operator_save_view(request):
    if request.method == 'POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        if data['password'] != data['password2']:
            return HttpResponseForbidden('Password did\'nt match')
        user = User(
            username =data['username'],
            last_name =data['last_name'],
            email =data['email'],
            phone_number =data['phone_number'],
            role =role,
            viloyat =viloyat
            )
        print(data)
        
        user.save()
        user.set_password(data['password'])
        user.save()
    
    return redirect('operator_list')

@login_required(login_url='/accounts/login/')
def xodim_save_view(request):
    if request.method == 'POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        if data['password'] != data['password2']:
            return HttpResponseForbidden('Password did\'nt match')
        user = User(
            username =data['username'],
            last_name =data['last_name'],
            email =data['email'],
            phone_number =data['phone_number'],
            role =role,
            viloyat =viloyat
            )
        print(data)
        
        user.save()
        user.set_password(data['password'])
        user.save()
    
    return redirect('hodim_list')

@login_required(login_url='/accounts/login/')
def teamlead_save_view(request):
    if request.method == 'POST':
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        if data['password'] != data['password2']:
            return HttpResponseForbidden('Password did\'nt match')
        user = User(
            username =data['username'],
            last_name =data['last_name'],
            email =data['email'],
            phone_number =data['phone_number'],
            role =role,
            viloyat =viloyat
            )
        
        user.save()
        user.set_password(data['password'])
        user.save()
    
    return redirect('teamlead_list')

@login_required(login_url='/accounts/login/')
def operator_update(request,id):
    if request.method == 'POST':
        operator = User.objects.get(id = id)
        form = OperatorForm(request.POST)
        viloyat_id = request.POST.get('viloyat')
        role = request.POST.get('role')
        viloyat = Viloyatlar.objects.get( id = int(viloyat_id))
        data =form.data 
        if data['password'] != data['password2']:
            return HttpResponseForbidden('Password did\'nt match')
        user = User(
            username =data['username'],
            last_name =data['last_name'],
            email =data['email'],
            phone_number =data['phone_number'],
            role =role,
            viloyat =viloyat,
            is_active =True
            )
        
        user.save()
        user.set_password(data['password'])
        user.save()
    
    return redirect('operator_list')

@login_required(login_url='/accounts/login/')
def viloyat_add(request):
    if request.method == 'POST':
        name = request.POST.get('viloyat')
        viloyat = Viloyatlar(name = name)
        viloyat.save()
        
    return redirect('viloyat_show')

@login_required(login_url='/accounts/login/')
def viloyat_show(request):
    viloyatolar = Viloyatlar.objects.all()

    paginator = Paginator(viloyatolar, 10)

    if request.GET.get('page') != None:
        page_number = request.GET.get('page')
    else:
        page_number=1
    
    page_obj = paginator.get_page(page_number)

    context ={
        'viloyatlar':page_obj
    }
    return render(request,'admin/viloyat_list.html',context)

@login_required(login_url='/accounts/login/')
def operator_delete(request,id):
    if User.objects.filter(id = id).exists():
        user =User.objects.get(id =id)
        user.delete()
    return redirect('operator_list')

@login_required(login_url='/accounts/login/')
def hodim_delete(request,id):
    if User.objects.filter(id = id).exists():
        user =User.objects.get(id =id)
        user.delete()
    return redirect('hodim_list')

@login_required(login_url='/accounts/login/')
def teamlead_delete(request,id):
    if User.objects.filter(id = id).exists():
        user =User.objects.get(id =id)
        user.delete()
    return redirect('teamlead_list')

@login_required(login_url='/accounts/login/')
def client_delete(request,id):
    if TelegramUser.objects.filter(user_id = id).exists():
        user =TelegramUser.objects.get(user_id =id)
        user.delete()
    return redirect('client_list')

@login_required(login_url='/accounts/login/')
def viloyat_delete(request,id):
    if Viloyatlar.objects.filter(id = id).exists():
        vil =Viloyatlar.objects.get(id =id)
        vil.delete()
    return redirect('viloyat_show')


