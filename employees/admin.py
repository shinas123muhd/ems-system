from django.contrib import admin
from .models import DynamicForm, FormField, Employee, EmployeeFieldValue


class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 0


@admin.register(DynamicForm)
class DynamicFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'fields_count', 'is_active', 'created_at')
    inlines = [FormFieldInline]


class EmployeeFieldValueInline(admin.TabularInline):
    model = EmployeeFieldValue
    extra = 0


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'email', 'form', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'employee_id')
    inlines = [EmployeeFieldValueInline]
