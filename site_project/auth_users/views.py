from django.shortcuts import render, redirect
from .forms import AuthForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django_auth_ldap.backend import LDAPBackend #, populate_user
from django.contrib.auth.models import Group
from decouple import config


def login_view(request):
    if request.method == 'POST':    # для POST пытаемся аутентифицировать пользователя
        auth_form = AuthForm(request.POST)

        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']

            auth = LDAPBackend()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    if user.is_superuser:
                        # добавляем пользователю группу 'Admin'
                        django_group = Group.objects.get(name=config("USER_GROUP_ADMIN"))                    
                        django_group.user_set.add(user)
                    
                    if user.is_staff:
                        # добавляем пользователю группу 'Staf'
                        django_group = Group.objects.get(name=config("USER_GROUP_STAF"))
                        django_group.user_set.add(user)
                    
                    # добавляем пользователю группу 'Active'
                    django_group = Group.objects.get(name=config("USER_GROUP_ACTIVE"))                    
                    django_group.user_set.add(user)

                    login(request, user)
                    return redirect('/')                
                
                else:
                    # print("-"*35)
                    # print('Error auth_users 1')
                    # print("-"*35)
                    auth_form.add_error('__all__','Успешная авторизация, но пользователь отключен, либо нет необходимых групп.')

            else:                                   
                # print("-"*35)
                # print('Error auth_users 2')
                # print("-"*35)
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность логина и пароля.')

    else:   # для всех остальных запросов просто отображаем форму, в .т.ч. с ошибками
        auth_form = AuthForm()

    context = {
        'form': auth_form
    }
    return render(request, 'auth_users/login.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=('/'))