from django.urls import path

from .views import SampleList, SampleTableListView, SampleDetail, SampleCreate


app_name = 'sample'
urlpatterns = [
    path('', SampleList.as_view(), name=''),
    path('table/', SampleTableListView.as_view(), name='table'),
    path('<int:id>/', SampleDetail.as_view(), name='detail'),
    path('create/', SampleCreate.as_view(), name='create'),
]
