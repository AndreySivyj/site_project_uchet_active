from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404#, HttpResponse, HttpRequest
from .models import *
from .forms import *
from .filters import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decouple import config
import ldap
from django.contrib import messages



def index(request):    
    
    title_text = "Index"
    context = {
            'user_login': request.user,
            'title_text':title_text,
        }    
    
    return render(request, 'base.html', context)


# ###########################################################################################################################################################
# Вспомогательные функции
# ###########################################################################################################################################################

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Получение данных из AD

def select_user_data_ldap(user_name):

    try:
        lconn = ldap.initialize(config("AUTH_LDAP_SERVER_URI"))   # домен
        lconn.protocol_version = ldap.VERSION3  # версия протокола
        lconn.set_option(ldap.OPT_REFERRALS, 0) # не используем рефералы
        lconn.simple_bind_s(config("AUTH_LDAP_BIND_DN"),config("AUTH_LDAP_BIND_PASSWORD"))  # учетные данные
        # print('Connect to AD succesfull')

        base = config("base_find_container")  # начальный контейнер, с которого начинаем поиск объектов
        scope = ldap.SCOPE_SUBTREE  # область поиска, SCOPE_SUBTREE - ищем в дочерних объектах        
        filter = "(&(sAMAccountName=%s))" % user_name  # фильтр, ищем объекты
        attrs = ['displayname','title','mail','sAMAccountName','givenName', 'company', 'extensionAttribute2', 'mobile', 'telephoneNumber']     # атрибуты искомых объектов ('displayname','title','mail','sAMAccountName','givenName')
        
        result_set = []     # массив с полученным результатом
        
        ldap_result_id = lconn.search_ext(base, scope, filter, attrs)   # идентификатор поиска объектов в каталоге

        try:
            while 1:
                result_type, result_data = lconn.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        # print("*"*55)
                        # print(result_data)
                        # print("*"*55)

                        fio = result_data[0][0].split(',')[0].split('=')[1] 
                        login = result_data[0][1].get('sAMAccountName')[0].decode("utf-8")
                        mail =  "" if result_data[0][1].get('mail', "") == "" else result_data[0][1].get('mail')[0].decode("utf-8")
                        distinguishedName = result_data[0][0]
                        company = "" if result_data[0][1].get('company', "") == "" else result_data[0][1].get('company')[0].decode("utf-8")
                        company_position = "" if result_data[0][1].get('extensionAttribute2', "") == "" else result_data[0][1].get('extensionAttribute2')[0].decode("utf-8")
                        mobile = "" if result_data[0][1].get('mobile', "") == "" else result_data[0][1].get('mobile')[0].decode("utf-8")
                        telephoneNumber = "" if result_data[0][1].get('telephoneNumber', "") == "" else result_data[0][1].get('telephoneNumber')[0].decode("utf-8")
                        
                        result_set.append({"fio":fio, "login":login, "mail":mail, "distinguishedName":distinguishedName,
                                            "company":company, "company_position":company_position,
                                            "mobile":mobile, "telephoneNumber":telephoneNumber,})

        except ldap.SIZELIMIT_EXCEEDED:
            print("ldap.SIZELIMIT_EXCEEDED")

        # for item in result_set:
        #     print(item)        
        return result_set     # массив с полученным результатом
    
    except ldap.SERVER_DOWN:
        print('Error connection to AD')


# ###########################################################################################################################################################
# Справочники
# ###########################################################################################################################################################


# ***********************************************************************************************************************************************************
# Model Type_active / Типы активов


# # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# @login_required
# @permission_required(perm='uchet_active.view_type_active', raise_exception=True)
# def type_active_list_view(request):
#     dataset = Type_active.objects.all() # Получаем все записи
#     count_dataset = dataset.count()

#     page = request.GET.get('page', 1)
#     paginator = Paginator(dataset, 10)  #  paginate_by 10
#     try:
#         dataset = paginator.page(page)
#     except PageNotAnInteger:
#         dataset = paginator.page(1)
#     except EmptyPage:
#         dataset = paginator.page(paginator.num_pages) 

#     title_text = "Типы активов (список записей)"
#     context = {
#             # 'user_login': request.user,            
#             'dataset': dataset,      
#             'count_dataset': count_dataset,      
#             'title_text':title_text,
#             'user_group_admin': config("USER_GROUP_ADMIN"),  
#             'user_group_staf': config("USER_GROUP_STAF"),
#             'url_delete_view': 'uchet_active:type_active_delete',
#             'url_update_view': 'uchet_active:type_active_update',          
#         }    
#     return render(request, 'uchet_active/type_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_type_active', raise_exception=True)
def type_active_list_view(request):
    dataset = Type_active.objects.all() # Получаем все записи
    dataset_filter = Type_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')
    
    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Типы активов (список записей)"
    context = {
            # 'user_login': request.user,
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:type_active_delete',
            'url_update_view': 'uchet_active:type_active_update',
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',
        }    
    return render(request, 'uchet_active/type_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_type_active', raise_exception=True)
def type_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Type_active.objects.get(id=id)
        title_text = "Тип актива"
        context = {
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:type_active_delete',
            'url_update_view': 'uchet_active:type_active_update',
        }
    except Type_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/type_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_type_active', raise_exception=True)    
def type_active_create(request):
    title_text = "Тип актива (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Type_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:type_active_list_view')
    else:
        form =Type_active_Form()
    context = {
            # 'user_login': request.user,
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_type_active', raise_exception=True)
def type_active_update(request, id):
    try:
        old_data = get_object_or_404(Type_active, id=id)
        title_text = "Тип актива (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Type_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/type_active/{id}')
    else:
        form = Type_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_type_active', raise_exception=True)
def type_active_delete(request, id):
    try:
        data = get_object_or_404(Type_active, id=id)
        title_text = "Тип актива (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
 
    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:type_active_list_view')
    else:
        return render(request, 'uchet_active/type_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Name_active / Модели активов


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_name_active', raise_exception=True)
def name_active_list_view(request):
    dataset = Name_active.objects.all().select_related("type_active",) # Получаем все записи
    dataset_filter = Name_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')
    
    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Модели активов (список записей)"
    context = {
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_active_delete',
            'url_update_view': 'uchet_active:name_active_update', 
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',           
        }    
    return render(request, 'uchet_active/name_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_name_active', raise_exception=True)
def name_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Name_active.objects.get(id=id)
        title_text = "Модель актива"
        context = {
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_active_delete',
            'url_update_view': 'uchet_active:name_active_update',
        }
    except Name_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/name_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_name_active', raise_exception=True)    
def name_active_create(request):
    title_text = "Модель актива (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Name_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:name_active_list_view')
    else:
        form =Name_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_name_active', raise_exception=True)
def name_active_update(request, id):
    try:
        old_data = get_object_or_404(Name_active, id=id)
        title_text = "Модель актива (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Name_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/name_active/{id}')
    else:
        form = Name_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_name_active', raise_exception=True)
def name_active_delete(request, id):
    try:
        data = get_object_or_404(Name_active, id=id)
        title_text = "Модель актива (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
 
    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:name_active_list_view')
    else:
        return render(request, 'uchet_active/name_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Inventory_number / Инвентарные номера


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_inventory_number', raise_exception=True)
def inventory_number_list_view(request):
    dataset = Inventory_number.objects.all() # Получаем все записи
    dataset_filter = Inventory_number_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Инвентарные номера (список записей)"
    context = {
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:inventory_number_delete',
            'url_update_view': 'uchet_active:inventory_number_update',   
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',       
        }    
    return render(request, 'uchet_active/inventory_number_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_inventory_number', raise_exception=True)
def inventory_number_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Inventory_number.objects.get(id=id)
        title_text = "Инвентарный номер"
        context = {            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:inventory_number_delete',
            'url_update_view': 'uchet_active:inventory_number_update',
        }
    except Inventory_number.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/inventory_number_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_inventory_number', raise_exception=True)    
def inventory_number_create(request):
    title_text = "Инвентарный номер (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Inventory_number_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:inventory_number_list_view')
    else:
        form =Inventory_number_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_inventory_number', raise_exception=True)
def inventory_number_update(request, id):
    try:
        old_data = get_object_or_404(Inventory_number, id=id)
        title_text = "Инвентарный номер (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Inventory_number_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/inventory_number/{id}')
    else:
        form = Inventory_number_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_inventory_number', raise_exception=True)
def inventory_number_delete(request, id):
    try:
        data = get_object_or_404(Inventory_number, id=id)
        title_text = "Инвентарный номер (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:inventory_number_list_view')
    else:
        return render(request, 'uchet_active/inventory_number_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Owner_active / Владелецы активов


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_owner_active', raise_exception=True)
def owner_active_list_view(request):
    dataset = Owner_active.objects.all() # Получаем все записи
    dataset_filter = Owner_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')
    
    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Владелецы активов (список записей)"
    context = {
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:owner_active_delete',
            'url_update_view': 'uchet_active:owner_active_update',
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',
        }    
    return render(request, 'uchet_active/owner_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_owner_active', raise_exception=True)
def owner_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Owner_active.objects.get(id=id)
        title_text = "Владелец актива"
        context = {
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:owner_active_delete',
            'url_update_view': 'uchet_active:owner_active_update',
        }
    except Owner_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/owner_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_owner_active', raise_exception=True)    
def owner_active_create(request):
    title_text = "Владелец актива (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Owner_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:owner_active_list_view')
    else:
        form = Owner_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_owner_active', raise_exception=True)
def owner_active_update(request, id):
    try:
        old_data = get_object_or_404(Owner_active, id=id)
        title_text = "Владелец актива (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Owner_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/owner_active/{id}')
    else:
        form = Owner_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_owner_active', raise_exception=True)
def owner_active_delete(request, id):
    try:
        data = get_object_or_404(Owner_active, id=id)
        title_text = "Владелец актива (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:owner_active_list_view')
    else:
        return render(request, 'uchet_active/owner_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Location_active / Локация/Склад


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_location_active', raise_exception=True)
def location_active_list_view(request):
    dataset = Location_active.objects.all().select_related("owner_active",) # Получаем все записи
    dataset_filter = Location_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Локация/Склад (список записей)"
    context = {        
            'filter': dataset_filter,  
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:location_active_delete',
            'url_update_view': 'uchet_active:location_active_update',     
            'url_return_to_the_list_view': 'uchet_active:location_active_list_view',       
        }    
    return render(request, 'uchet_active/location_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_location_active', raise_exception=True)
def location_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Location_active.objects.get(id=id)
        title_text = "Локация/Склад"
        context = { 
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:location_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:location_active_delete',
            'url_update_view': 'uchet_active:location_active_update',
        }
    except Location_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/location_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_location_active', raise_exception=True)    
def location_active_create(request):
    title_text = "Локация/Склад (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Location_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:location_active_list_view')
    else:
        form = Location_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:location_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_location_active', raise_exception=True)
def location_active_update(request, id):
    try:
        old_data = get_object_or_404(Location_active, id=id)
        title_text = "Локация/Склад (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Location_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/location_active/{id}')
    else:
        form = Location_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:location_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_location_active', raise_exception=True)
def location_active_delete(request, id):
    try:
        data = get_object_or_404(Location_active, id=id)
        title_text = "Локация/Склад (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:location_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:location_active_list_view')
    else:
        return render(request, 'uchet_active/location_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Status_active / Статусы


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_status_active', raise_exception=True)
def status_active_list_view(request):
    dataset = Status_active.objects.all() # Получаем все записи
    dataset_filter = Status_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Статусы (список записей)"
    context = {
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text, 
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:status_active_delete',
            'url_update_view': 'uchet_active:status_active_update',
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',
        }    
    return render(request, 'uchet_active/status_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_status_active', raise_exception=True)
def status_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Status_active.objects.get(id=id)
        title_text = "Статус"
        context = {          
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',           
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:status_active_delete',
            'url_update_view': 'uchet_active:status_active_update',
        }
    except Status_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/status_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_status_active', raise_exception=True)    
def status_active_create(request):
    title_text = "Статус (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Status_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:status_active_list_view')
    else:
        form = Status_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_status_active', raise_exception=True)
def status_active_update(request, id):
    try:
        old_data = get_object_or_404(Status_active, id=id)
        title_text = "Статус (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Status_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/status_active/{id}')
    else:
        form = Status_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_status_active', raise_exception=True)
def status_active_delete(request, id):
    try:
        data = get_object_or_404(Status_active, id=id)
        title_text = "Статус (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:status_active_list_view')
    else:
        return render(request, 'uchet_active/status_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Name_quantity_active / Единицы измерения


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_name_quantity_active', raise_exception=True)
def name_quantity_active_list_view(request):
    dataset = Name_quantity_active.objects.all() # Получаем все записи    
    dataset_filter = Name_quantity_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Единицы измерения (список записей)"
    context = {  
            'filter': dataset_filter,
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_quantity_active_delete',
            'url_update_view': 'uchet_active:name_quantity_active_update',       
            'url_return_to_the_list_view': 'uchet_active:name_quantity_active_list_view',
        }    
    return render(request, 'uchet_active/name_quantity_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_name_quantity_active', raise_exception=True)
def name_quantity_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Name_quantity_active.objects.get(id=id)
        title_text = "Единица измерения"
        context = {           
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_quantity_active_list_view',    
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_quantity_active_delete',
            'url_update_view': 'uchet_active:name_quantity_active_update',       
        }
    except Name_quantity_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/name_quantity_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_name_quantity_active', raise_exception=True)    
def name_quantity_active_create(request):
    title_text = "Единица измерения (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Name_quantity_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():
            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:name_quantity_active_list_view')
    else:
        form = Name_quantity_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:name_quantity_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_name_quantity_active', raise_exception=True)
def name_quantity_active_update(request, id):
    try:
        old_data = get_object_or_404(Name_quantity_active, id=id)
        title_text = "Единица измерения (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Name_quantity_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/name_quantity_active/{id}')
    else:
        form = Name_quantity_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_quantity_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_name_quantity_active', raise_exception=True)
def name_quantity_active_delete(request, id):
    try:
        data = get_object_or_404(Name_quantity_active, id=id)
        title_text = "Единица измерения (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_quantity_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:name_quantity_active_list_view')
    else:
        return render(request, 'uchet_active/name_quantity_active_delete.html', context)


# ###########################################################################################################################################################
# Реестры
# ###########################################################################################################################################################


# ***********************************************************************************************************************************************************
# Model Details_document_active / Реквизиты документов


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_details_document_active', raise_exception=True)
def details_document_active_list_view(request):
    dataset = Details_document_active.objects.all().select_related("creator_account",) # Получаем все записи
    dataset_filter = Details_document_active_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Реквизиты документов (список записей)"
    context = {        
            'filter': dataset_filter,  
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:details_document_active_delete',
            'url_update_view': 'uchet_active:details_document_active_update',     
            'url_return_to_the_list_view': 'uchet_active:details_document_active_list_view',       
        }    
    return render(request, 'uchet_active/details_document_active_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_details_document_active', raise_exception=True)
def details_document_active_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Details_document_active.objects.get(id=id)
        title_text = "Реквизиты документа"
        context = { 
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:details_document_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:details_document_active_delete',
            'url_update_view': 'uchet_active:details_document_active_update',
        }
    except Details_document_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/details_document_active_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_details_document_active', raise_exception=True)    
def details_document_active_create(request):
    title_text = "Реквизиты документа (добавление записи)"
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Details_document_active_Form(request.POST)
        # Проверяем правильность введенных данных
        if form.is_valid():

            form.instance.creator_account = request.user # записываем в скрытое поле "creator_account" данные по авторизированному пользователю (Кем изменено/создано)

            # сохраняем в базу
            form.save()
            # переадресуем на listview
            return redirect('uchet_active:details_document_active_list_view')
    else:
        form = Details_document_active_Form()
    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:details_document_active_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_details_document_active', raise_exception=True)
def details_document_active_update(request, id):
    try:
        old_data = get_object_or_404(Details_document_active, id=id)
        title_text = "Реквизиты документа (обновление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    # Если метод POST, то это обновленные данные
    # Остальные методы - возврат данных для изменения
    if request.method =='POST':
        form = Details_document_active_Form(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/details_document_active/{id}')
    else:
        form = Details_document_active_Form(instance = old_data)
    context ={            
            'form':form,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:details_document_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_details_document_active', raise_exception=True)
def details_document_active_delete(request, id):
    try:
        data = get_object_or_404(Details_document_active, id=id)
        title_text = "Реквизиты документа (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:details_document_active_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:details_document_active_list_view')
    else:
        return render(request, 'uchet_active/details_document_active_delete.html', context)


# ***********************************************************************************************************************************************************
# Model Profile_AD / Профили пользователей (AD)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_profile_ad', raise_exception=True)
def profile_ad_list_view(request):
    dataset = Profile_AD.objects.all() # Получаем все записи
    dataset_filter = Profile_AD_Filter(request.GET, queryset=dataset)

    count_dataset = dataset_filter.qs.count()

    dataset = dataset_filter.qs
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    page_number = request.GET.get('page')

    try:
        dataset = paginator.page(page_number)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Профили пользователей AD (список записей)"
    context = {        
            'filter': dataset_filter,  
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:profile_ad_delete',
            'url_update_view': 'uchet_active:profile_ad_update',     
            'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',       
        }    
    return render(request, 'uchet_active/profile_ad_listview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_profile_ad', raise_exception=True)
def profile_ad_detail_view(request, id):
    try:
        # Получаем запись по-определенному id
        data = Profile_AD.objects.get(id=id)
        title_text = "Профиль пользователя AD"
        context = { 
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:profile_ad_delete',
            'url_update_view': 'uchet_active:profile_ad_update',
        }
    except Profile_AD.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/profile_ad_detailview.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.add_profile_ad', raise_exception=True)    
def profile_ad_create(request):
    title_text = "Профиль пользователя AD (добавление записи)"
    
    # Проверяем, что запрос на добавление записи (POST) или просто на получение формы
    if request.method == 'POST':
        # Получаем из запроса только те данные которые использует форма
        form = Profile_AD_Form(request.POST)
        
        # Проверяем правильность введенных данных
        if form.is_valid():
            result_user_data = select_user_data_ldap(form.instance.account)   # получаем информацию из AD по имени пользователя
            
            # проверяем, что поле учетной записи не пустое (пользователь найден в AD)
            if result_user_data != []:               
                        
                # если 'Профиль пользователя AD' уже существует
                if Profile_AD.objects.filter(account__iexact=form.instance.account.lower()).exists():
                    try:
                        # обновляем запись (возможна смена фамилии/должности)                           
                        profile_ad = get_object_or_404(Profile_AD, account__iexact=form.instance.account.lower()) 

                        profile_ad.fio = result_user_data[0]['fio']
                        profile_ad.email = result_user_data[0]['mail']
                        profile_ad.distingished_name = result_user_data[0]['distinguishedName']
                        profile_ad.company = result_user_data[0]['company']
                        profile_ad.company_position = result_user_data[0]['company_position']
                        profile_ad.mobile = result_user_data[0]['mobile']
                        profile_ad.telephone_number = result_user_data[0]['telephoneNumber']
                        profile_ad.save()

                    except Profile_AD.DoesNotExist:
                        raise Http404('Такой записи не существует')
                    
                # 'Профиль пользователя AD' не существует в БД            
                else:
                    form.instance.fio = result_user_data[0]['fio']                    
                    form.instance.email = result_user_data[0]['mail']
                    form.instance.distingished_name = result_user_data[0]['distinguishedName']
                    form.instance.company = result_user_data[0]['company']
                    form.instance.company_position = result_user_data[0]['company_position']
                    form.instance.mobile = result_user_data[0]['mobile']
                    form.instance.telephone_number = result_user_data[0]['telephoneNumber']                

                    # сохраняем в базу        
                    result_object = form.save()

                # # ---------------------------------------------------------------------------
                # # логируем операцию создания записи Reestr_TMTS_Model и добавления ее в Arhiv_Reestr_TMTS_Model
                # # created_dateTime=datetime.datetime.now()
                # # updated_dateTime=datetime.datetime.now()
                # action = 'создание'                    
                # create_user = request.user
                # # reestr_tmts_logging_CRUD_operations(result_object, created_dateTime, updated_dateTime, action, create_user)
                # reestr_tmts_logging_CRUD_operations(result_object, action, create_user)
                # # ---------------------------------------------------------------------------

                # # messages.success(request, "Запись успешно записана в БД.")
                

                
                # переадресуем на listview
                return redirect('uchet_active:profile_ad_list_view')
            
            else:
                # form.add_error('__all__', 'Ошибка! Проверьте правильность логина и пароля.')
                messages.error(request, 'Ошибка! Проверьте правильность учетной записи.')
                messages.error(request, form.errors)
                form = Profile_AD_Form(request.POST)    
                        
        else:
            messages.error(request, 'Ошибка! Проверьте правильность учетной записи.')
            messages.error(request, form.errors)
            form = Profile_AD_Form(request.POST)

    else:
        form = Profile_AD_Form()

    context = {
            'form': form,
            'title_text': title_text,
            'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),          
        }        
    return render(request, 'uchet_active/create.html', context)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.change_profile_ad', raise_exception=True)
def profile_ad_update(request, id):
    try:
        # Получаем запись по-определенному id
        old_data = Profile_AD.objects.get(id=id)
        title_text = "Профиль пользователя AD (обновление записи)"        
    except Profile_AD.DoesNotExist:
        raise Http404('Такой записи не существует')
    
    context = { 
            'data': old_data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }
    
    if request.method == 'POST':
        result_user_data = select_user_data_ldap(old_data.account)   # получаем информацию из AD по имени пользователя
            
        # проверяем, что поле учетной записи не пустое (пользователь найден в AD)
        if result_user_data != []:               

            try:
                # обновляем запись (возможна смена фамилии/должности)                           
                profile_ad = get_object_or_404(Profile_AD, id=id) 

                profile_ad.fio = result_user_data[0]['fio']
                profile_ad.email = result_user_data[0]['mail']
                profile_ad.distingished_name = result_user_data[0]['distinguishedName']
                profile_ad.company = result_user_data[0]['company']
                profile_ad.company_position = result_user_data[0]['company_position']
                profile_ad.mobile = result_user_data[0]['mobile']
                profile_ad.telephone_number = result_user_data[0]['telephoneNumber']
                profile_ad.save()

            except Profile_AD.DoesNotExist:
                raise Http404('Такой записи не существует')
        else:
            messages.error(request, 'Ошибка! Проверьте правильность учетной записи (отсутствует в AD).')

        return redirect(f'/profile_ad/{id}')

    else:
        return render(request, 'uchet_active/profile_ad_update.html', context)






# @login_required
# @permission_required(perm='uchet_active.change_profile_ad', raise_exception=True)
# def profile_ad_update(request, id):
#     try:
#         old_data = get_object_or_404(Profile_AD, id=id)
#         title_text = "Профиль пользователя AD (обновление записи)"
#     except Exception:
#         raise Http404('Такой записи не существует')
    
#     # Если метод POST, то это обновленные данные
#     # Остальные методы - возврат данных для изменения
#     if request.method =='POST':
#         form = Profile_AD_Form(request.POST, instance=old_data)
#         if form.is_valid():
#             form.save()
#             return redirect(f'/profile_ad/{id}')
#     else:
#         form = Profile_AD_Form(instance = old_data)
#     context ={            
#             'form':form,
#             'title_text':title_text,
#             'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',
#             'user_group_admin': config("USER_GROUP_ADMIN"),  
#             'user_group_staf': config("USER_GROUP_STAF"),
#         }
#     return render(request, 'uchet_active/update.html', context)
    

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.delete_profile_ad', raise_exception=True)
def profile_ad_delete(request, id):
    try:
        data = get_object_or_404(Profile_AD, id=id)
        title_text = "Профиль пользователя AD (удаление записи)"
    except Exception:
        raise Http404('Такой записи не существует')
    
    context ={
            'data': data,
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:profile_ad_list_view',
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
        }

    if request.method == 'POST':
        data.delete()
        return redirect('uchet_active:profile_ad_list_view')
    else:
        return render(request, 'uchet_active/profile_ad_delete.html', context)









