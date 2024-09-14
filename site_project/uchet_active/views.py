from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404#, HttpResponse, HttpRequest
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decouple import config



def index(request):    
    
    title_text = "Index"
    context = {
            'user_login': request.user,
            'title_text':title_text,
        }    
    
    return render(request, 'base.html', context)

# ***********************************************************************************************************************************************************
# Model Type_active / Типы активов


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
@login_required
@permission_required(perm='uchet_active.view_type_active', raise_exception=True)
def type_active_list_view(request):
    dataset = Type_active.objects.all() # Получаем все записи
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Типы активов (список записей)"
    context = {
            # 'user_login': request.user,            
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:type_active_delete',
            'url_update_view': 'uchet_active:type_active_update',          
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
    dataset = Name_active.objects.all() # Получаем все записи
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Модели активов (список записей)"
    context = {
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_active_delete',
            'url_update_view': 'uchet_active:name_active_update',            
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
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Инвентарные номера (список записей)"
    context = {
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,  
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:inventory_number_delete',
            'url_update_view': 'uchet_active:inventory_number_update',          
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
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Владелецы активов (список записей)"
    context = {
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:owner_active_delete',
            'url_update_view': 'uchet_active:owner_active_update',
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
    dataset = Location_active.objects.all() # Получаем все записи
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Локация/Склад (список записей)"
    context = {          
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:location_active_delete',
            'url_update_view': 'uchet_active:location_active_update',            
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
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Статусы (список записей)"
    context = {
            # 'user_login': request.user,            
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text, 
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:status_active_delete',
            'url_update_view': 'uchet_active:status_active_update',
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
    count_dataset = dataset.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(dataset, 10)  #  paginate_by 10
    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages) 

    title_text = "Единицы измерения (список записей)"
    context = {           
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,
            'user_group_admin': config("USER_GROUP_ADMIN"),  
            'user_group_staf': config("USER_GROUP_STAF"),
            'url_delete_view': 'uchet_active:name_quantity_active_delete',
            'url_update_view': 'uchet_active:name_quantity_active_update',            
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



