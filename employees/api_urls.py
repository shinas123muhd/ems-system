from django.urls import path
from . import api_views

urlpatterns = [
    # Dynamic Forms API
    path('forms/', api_views.FormListCreateView.as_view(), name='api_form_list'),
    path('forms/<int:pk>/', api_views.FormDetailView.as_view(), name='api_form_detail'),
    path('forms/<int:pk>/fields/', api_views.FormFieldsView.as_view(), name='api_form_fields'),
    # Employees API
    path('employees/', api_views.EmployeeListCreateView.as_view(), name='api_employee_list'),
    path('employees/<int:pk>/', api_views.EmployeeDetailView.as_view(), name='api_employee_detail'),
]
