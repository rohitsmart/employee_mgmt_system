
from django.contrib import admin
from django.urls import path
from users.views import user_signup
from users.views import user_login, user_logout
from project.views import create_module,delete_module, update_module, get_module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/signup/', user_signup, name='user_signup'),
    path('api/project/createModule/',create_module, name='create_module'),
    path('api/user/login/', user_login, name='user_login'),
    path('api/project/deleteModule/', delete_module, name='delete_module'),
    path('api/project/updateModule/', update_module, name='update_module'),
    path('api/project/getModule/', get_module ,name='get_module'),
    path('api/user/logout/', user_logout, name='user_logout'),
    
]
