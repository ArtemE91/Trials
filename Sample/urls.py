from django.urls import path

from .views import (SampleList, SampleTableListView, SampleDetail,
                    SampleCreate, SampleMaterialList, SampleTypeList,
                    SampleMaterialCreate, SampleTypeCreate, SampleUpdateView,
                    SampleDeleteView)


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
    path('material/create/', SampleMaterialCreate.as_view(), name='material_create'),
    path('type/', SampleTypeList.as_view(), name='type'),
    path('type/create/', SampleTypeCreate.as_view(), name='type_create'),
]