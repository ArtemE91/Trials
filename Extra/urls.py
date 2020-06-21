from django.urls import path
from .views import DataLoadingTemplateView

app_name = 'extra'
urlpatterns = [
    path('data/loading/', DataLoadingTemplateView.as_view(), name='data_loading'),
]
