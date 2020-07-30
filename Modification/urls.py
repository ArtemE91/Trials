from django.urls import path

from .views import (ModificationListView, ModificationDetailView, ModificationUpdateView,
                    ModificationCreateView, ModificationDeleteView, )

app_name = 'modification'
urlpatterns = [
    path('', ModificationListView.as_view(), name='list'),
    path('dropdown/', ModificationListView.as_view(
        template_name='modification/includes/modification_dropdown.html'),
         name='dropdown_list'),
    path('<int:pk>/', ModificationDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', ModificationUpdateView.as_view(), name='update'),
    path('create/', ModificationCreateView.as_view(), name='create'),
    path('create/modal/', ModificationCreateView.as_view(
            template_name='modification/modification_create_modal.html'),
         name='create_modal'),
    path('<int:pk>/delete/', ModificationDeleteView.as_view(), name='delete'),
]

