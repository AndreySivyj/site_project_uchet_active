from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404#, HttpResponse, HttpRequest
from .models import Type_active, Name_active, Inventory_number, Owner_active, Status_active
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




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
            # 'user_login': request.user,            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:type_active_list_view',
        }
    except Type_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/type_active_detailview.html', context)


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
            # 'user_login': request.user,            
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,            
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
            # 'user_login': request.user,            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:name_active_list_view',
        }
    except Name_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/name_active_detailview.html', context)


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
            # 'user_login': request.user,            
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,            
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
            # 'user_login': request.user,            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:inventory_number_list_view',
        }
    except Inventory_number.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/inventory_number_detailview.html', context)


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
            # 'user_login': request.user,            
            'dataset': dataset,      
            'count_dataset': count_dataset,      
            'title_text':title_text,            
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
            # 'user_login': request.user,            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:owner_active_list_view',
        }
    except Owner_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/owner_active_detailview.html', context)


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
            # 'user_login': request.user,            
            'data': data,      
            'title_text':title_text,
            'url_return_to_the_list_view': 'uchet_active:status_active_list_view',           
        }
    except Status_active.DoesNotExist:
        raise Http404('Такой записи не существует') 
    return render(request, 'uchet_active/status_active_detailview.html', context)


