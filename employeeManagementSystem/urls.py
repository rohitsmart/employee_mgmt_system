
from django.contrib import admin
from django.urls import path
from users.views import user_signup
from users.views import user_login
from project.views import create_module
from project.views import delete_module


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/signup/', user_signup, name='user_signup'),
    path('api/project/createModule/',create_module, name='create_module'),
    path('api/user/login/', user_login, name='user_login'),
    path('api/project/deleteModule/', delete_module, name='delete_module'),
]
