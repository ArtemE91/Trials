from django.urls import path
from .views import DataLoadingTemplateView, InfoFIllTemplateView, DownloadDataTemplateView

app_name = 'extra'
urlpatterns = [
    path('data/loading/', DataLoadingTemplateView.as_view(), name='data_loading'),
    path('info/', InfoFIllTemplateView.as_view(), name='info_fill_config'),
    path('download/', DownloadDataTemplateView.as_view(), name='download_excel'),
]
