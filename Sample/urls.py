from django.urls import path

from .views import (SampleList, SampleTableListView, SampleDetail,
                    SampleCreate, SampleMaterialList, SampleTypeList,
                    SampleMaterialCreate, SampleTypeCreate)


app_name = 'sample'
urlpatterns = [
    path('', SampleList.as_view(), name=''),
    path('table/', SampleTableListView.as_view(), name='table'),
    path('detail/<int:id>/', SampleDetail.as_view(), name='detail'),
    path('create/', SampleCreate.as_view(), name='create'),
    path('material/', SampleMaterialList.as_view(), name='material'),
    path('material/create/', SampleMaterialCreate.as_view(), name='material_create'),
    path('type/', SampleTypeList.as_view(), name='type'),
    path('type/create/', SampleTypeCreate.as_view(), name='type_create'),
]
