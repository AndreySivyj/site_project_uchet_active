from django.urls import path, include
from .views import *
# from uchet_active.views import *

app_name = 'auth_users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('', include('uchet_active.urls')), # главная страница, в т.ч. LOGIN_REDIRECT_URL
    # path('reestr_active_list/', reestr_active_list_view, name='reestr_active_list'),

]