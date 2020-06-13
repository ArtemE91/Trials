from django.urls import path

from .views import (SampleList, SampleTableListView, SampleDetail,
                    SampleCreate, SampleMaterialList, SampleTypeList,
                    SampleMaterialCreate, SampleTypeCreate, SampleUpdateView,
                    SampleDeleteView, SampleMaterialDetail, SampleMaterialUpdateView,
                    SampleMaterialDeleteView, SampleTypeUpdateView, SampleTypeDeleteView,
                    SampleTypeDetail, )

app_name = 'sample'
urlpatterns = [
    path('', SampleList.as_view(), name=''),
    path('table/', SampleTableListView.as_view(), name='table'),
    path('<int:pk>/', SampleDetail.as_view(), name='detail'),
    path('detail/<int:pk>/', SampleDetail.as_view(
        template_name='sample/sample_modal_detail.html'),
         name='detail_modal'),
    path('detail/tr/<int:pk>/', SampleDetail.as_view(
        template_name='sample/sample_detail_tr.html'),
         name='detail_tr'),
    path('<int:pk>/update/', SampleUpdateView.as_view(), name='update'),
    path('create/', SampleCreate.as_view(), name='create'),
    path('<int:pk>/delete/', SampleDeleteView.as_view(), name='delete'),
    path('material/', SampleMaterialList.as_view(), name='material'),
    path('material/table/', SampleMaterialList.as_view(
        template_name='sample/material/material.html'),
         name='material_table'),
    path('material/<int:pk>/update/', SampleMaterialUpdateView.as_view(), name='material_update'),
    path('material/<int:pk>/delete/', SampleMaterialDeleteView.as_view(), name='material_delete'),
    path('material/detail/<int:pk>/', SampleMaterialDetail.as_view(), name='material_detail'),
    path('material/create/', SampleMaterialCreate.as_view(), name='material_create'),
    path('material/create/form/', SampleMaterialCreate.as_view(
        template_name='sample/material/material_create.html'),
         name='material_create_form'),
    path('type/', SampleTypeList.as_view(), name='type'),
    path('type/table/', SampleTypeList.as_view(
        template_name='sample/type/type.html'),
         name='type_table'),
    path('type/<int:pk>/update/', SampleTypeUpdateView.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', SampleTypeDeleteView.as_view(), name='type_delete'),
    path('type/detail/<int:pk>/', SampleTypeDetail.as_view(), name='type_detail'),
    path('type/create/form/', SampleTypeCreate.as_view(
        template_name='sample/type/type_create.html'
    ), name='type_create_form'),
    path('type/create/', SampleTypeCreate.as_view(), name='type_create'),
]
