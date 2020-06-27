from django.urls import path
from .views import (TrialCreate, TrialList, TrialDetail,
                    TrialUpdate, TrialDelete, ExperimentCreate,
                    TrialDetailTr,TrialModalDetail, ExperimentList,
                    ExperimentDelete, ExperimentUpdate, TrialGraph,
                    TrialTableListView)

app_name = 'trial'
urlpatterns = [
    path('table/', TrialTableListView.as_view(), name='table'),
    path('experiment/<int:pk>/delete/', ExperimentDelete.as_view(), name='delete_experiment'),
    path('experiment/<int:pk>/update/', ExperimentUpdate.as_view(), name='update_experiment'),
    path('<int:pk>/create_experiment/', ExperimentCreate.as_view(), name='create_experiment'),
    path('<int:pk>/experement_list/', ExperimentList.as_view(), name='list_experiment'),
    path('<int:pk>/delete/', TrialDelete.as_view(), name='delete'),
    path('<int:pk>/get_graph/', TrialGraph.as_view(), name='get_graph'),
    path('<int:pk>/update/', TrialUpdate.as_view(), name='update'),
    path('<int:pk>/', TrialDetail.as_view(), name='detail'),
    path('detail/tr/<int:pk>/', TrialDetailTr.as_view(), name='detail_tr'),
    path('detail/<int:pk>/', TrialModalDetail.as_view(), name='detail_modal'),
    path('', TrialList.as_view(), name='list'),
    path('create/', TrialCreate.as_view(), name='create'),
]
