from django.urls import path
from .views import TrialCreate

app_name = 'trial'
urlpatterns = [
    path('create/', TrialCreate.as_view(), name='create'),
]
