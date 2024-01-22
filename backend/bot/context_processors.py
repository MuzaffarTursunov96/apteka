ROLE_CHOICES ={
    1:'admin',
    2:'operator',
    3:'xodim',
    4:'client'
}

def get_user_role(request):
    if request.user.is_authenticated:
        user_role =request.user.role
        if user_role ==None:
            user_role='nan'
        else:
            user_role =ROLE_CHOICES[user_role]
    else:
        user_role ='nan'
    return {'user_role':str(user_role)}