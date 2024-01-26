
from django.urls import path
from . import views

urlpatterns = [

    #admin
    path('',views.index,name='index'),
    path('message-admin',views.message_admin,name='message_admin'),
    path('operator-list',views.operatorlist,name='operator_list'),
    path('viloyat-add',views.viloyat_add,name='viloyat_add'),
    path('viloyat-list',views.viloyat_show,name='viloyat_show'),
    path('operator-save',views.operator_save_view,name='operator_save_view'),
    path('operator-update/<int:id>',views.operator_update,name='operator_update'),
    path('operator-delete/<int:id>',views.operator_delete,name='operator_delete'),
    path('viloyat-delete/<int:id>',views.viloyat_delete,name='viloyat_delete'),
    path('messages-admin/<int:id>',views.message_show,name='message_show'),
    path('hodim-edit/<int:id>',views.hodim_edit,name='hodim_edit'),

    ########## team lead >>> operator#######
    path('teamlead-list',views.teamlead_list,name='teamlead_list'),
    path('xodim-edit/<int:id>',views.xodim_edit,name='xodim_edit'),
    path('xodim-save',views.xodim_save_view,name='hodim_save'),
    path('xodim-delete/<int:id>',views.hodim_delete,name='hodim_delete'),
    path('messages-operator/<int:id>',views.message_show_for_staff,name='message_show_for_operator'),
    path('xodimlar-royxati',views.xodim_list,name='hodim_list'),
    path('teamlead-edit/<int:id>',views.teamlead_edit,name='teamlead_edit'),
    path('teamlead-save',views.teamlead_save_view,name='teamlead_save_view'),
    path('teamlead-delete/<int:id>',views.teamlead_delete,name='teamlead_delete'),


    #operator
    path('messages',views.chat_operator,name='chat_operator'),
   

    #######client#######
    path('client-list',views.client_list,name='client_list'),
    path('client-edit/<int:id>',views.client_edit,name='client_edit'),
    path('client-delete/<int:id>',views.client_delete,name='client_delete'),

    #chat
    path("chat/<str:chat_box_name>/", views.chat_box, name="chat"),
    path('download/<file_id>', views.download_file, name='download_file'),    

    ######authentications########

    path('accounts/login/',views.login,name='login'),
    path('registration',views.registration,name='registration'),
    path('logout/',views.logout,name='logout'),



    ##################aaditional
    path('chat2',views.chat2,name='chat2')
]
