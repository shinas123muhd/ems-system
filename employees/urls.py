from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Form builder
    path('forms/', views.form_list, name='form_list'),
    path('forms/builder/', views.form_builder, name='form_builder'),
    path('forms/builder/<int:pk>/', views.form_builder, name='form_builder_edit'),
    # path('forms/save/', views.save_form, name='save_form'),
    # path('forms/<int:pk>/data/', views.get_form_data, name='get_form_data'),
    # path('forms/<int:pk>/fields/', views.get_form_fields, name='get_form_fields'),
    path('forms/<int:pk>/delete/', views.delete_form, name='delete_form'),
    # Employees
    path('create/', views.employee_create, name='employee_create'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('save/', views.save_employee, name='save_employee'),
    path('<int:pk>/delete/', views.delete_employee, name='delete_employee'),
]
