from django.urls import path

from .views import SampleList, SampleTableListView, SampleDetail, SampleCreate

urlpatterns = [
    path('sample/', SampleList.as_view(), name='sample'),
    path('sample/table/', SampleTableListView.as_view(), name='sample_table'),
    path('sample/<int:id>/', SampleDetail.as_view(), name='sample_detail'),
    path('sample/create/', SampleCreate.as_view(), name='sample_create'),
]