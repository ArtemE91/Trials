from django.urls import path
from .views import TrialCreate, TrialList, TrialDetail, TrialUpdate

app_name = 'trial'
urlpatterns = [
    path('<int:pk>/update/', TrialUpdate.as_view(), name='update'),
    path('<int:pk>/', TrialDetail.as_view(), name='detail'),
    path('', TrialList.as_view(), name='list'),
    path('create/', TrialCreate.as_view(), name='create'),
]
