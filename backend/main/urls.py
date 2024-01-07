
from django.urls import path
from . import views

urlpatterns = [

    #admin
    path('',views.index,name='index'),




    #operator
    path('messages',views.chat_operator,name='chat_operator'),
   



    #chat
    path("chat/<str:chat_box_name>/", views.chat_box, name="chat"),

    ######authentications########

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout')




]
