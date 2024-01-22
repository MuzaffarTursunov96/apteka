from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path

from . import views



urlpatterns = [

    path('operators/<region_name>',views.ListOperators.as_view(),name='operators'),
    path('viloyatlar',views.ListViloyatlar.as_view(),name='viloyatlar'),
    path('telegram-user-save',views.TelegramUserSave,name='telegram_user_save'),

    path('user-message-receive',views.user_message_receive,name='user_message_receive'),
    path('hodimlar-save',views.hodimlar_save,name='operator_save'),



    ########## messages #######
    path('user-message-get/<int:id>',views.messages_all,name='messages_all'),

    path('receive-operator-message',views.send_message_to_client,name='send_message_to_client'),




   
]
