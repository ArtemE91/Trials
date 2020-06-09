from django.urls import path
from .views import TrialCreate, TrialListView

app_name = 'trial'
urlpatterns = [
    path('', TrialListView.as_view(), name='list'),
    path('create/', TrialCreate.as_view(), name='create'),
]
