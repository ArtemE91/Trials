from django.urls import path
from .views import (TrialCreate, TrialList, TrialDetail,
                    TrialUpdate, TrialDelete, ExperimentCreate, TrialDetailTr,
                    TrialModalDetail)

app_name = 'trial'
urlpatterns = [
    path('create_experiment/', ExperimentCreate.as_view(), name='create_experiment'),
    path('<int:pk>/delete/', TrialDelete.as_view(), name='delete'),
    path('<int:pk>/update/', TrialUpdate.as_view(), name='update'),
    path('<int:pk>/', TrialDetail.as_view(), name='detail'),
    path('detail/tr/<int:pk>/', TrialDetailTr.as_view(), name='detail_tr'),
    path('detail/<int:pk>/', TrialModalDetail.as_view(), name='detail_modal'),
    path('', TrialList.as_view(), name='list'),
    path('create/', TrialCreate.as_view(), name='create'),
]
