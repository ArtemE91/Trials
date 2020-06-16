from django.urls import path

from .views import (UserLoginView, UserLogOut)

app_name = 'user'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOut.as_view(), name='logout')
]