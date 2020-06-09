from django.urls import path
from .views import TrialCreate, TrialListView, TrialDetailView

app_name = 'trial'
urlpatterns = [
    path('<int:pk>/', TrialDetailView.as_view(), name='detail'),
    path('', TrialListView.as_view(), name='list'),
    path('create/', TrialCreate.as_view(), name='create'),
]
