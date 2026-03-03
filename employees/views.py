from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .models import DynamicForm, FormField, Employee, EmployeeFieldValue


@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_forms = DynamicForm.objects.filter(is_active=True).count()
    recent_employees = Employee.objects.select_related('form')[:5]
    return render(request, 'employees/dashboard.html', {
        'total_employees': total_employees,
        'total_forms': total_forms,
        'recent_employees': recent_employees,
    })


# ─── FORM BUILDER VIEWS ───────────────────────────────────────────────────────

def form_list(request):
    return render(request, 'employees/form_list.html')



def form_builder(request, pk=None):
    return render(request, 'employees/form_builder.html')


# @login_required
# @require_http_methods(["POST"])
# def save_form(request):
#     try:
#         data = json.loads(request.body)
#         form_id = data.get('id')
#         name = data.get('name', '').strip()
#         description = data.get('description', '')
#         fields = data.get('fields', [])

#         if not name:
#             return JsonResponse({'success': False, 'error': 'Form name is required.'}, status=400)

#         if form_id:
#             form_obj = get_object_or_404(DynamicForm, pk=form_id, created_by=request.user)
#             form_obj.name = name
#             form_obj.description = description
#             form_obj.save()
#             form_obj.fields.all().delete()
#         else:
#             form_obj = DynamicForm.objects.create(
#                 name=name, description=description, created_by=request.user
#             )

#         for i, f in enumerate(fields):
#             FormField.objects.create(
#                 form=form_obj,
#                 label=f.get('label', ''),
#                 field_type=f.get('field_type', 'text'),
#                 placeholder=f.get('placeholder', ''),
#                 is_required=f.get('is_required', False),
#                 options=f.get('options', ''),
#                 default_value=f.get('default_value', ''),
#                 order=i,
#             )

#         return JsonResponse({'success': True, 'id': form_obj.id, 'message': 'Form saved successfully.'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)}, status=500)


# @login_required
# def get_form_data(request, pk):
#     form_obj = get_object_or_404(DynamicForm, pk=pk, created_by=request.user)
#     data = {
#         'id': form_obj.id,
#         'name': form_obj.name,
#         'description': form_obj.description,
#         'fields': [
#             {
#                 'id': f.id,
#                 'label': f.label,
#                 'field_type': f.field_type,
#                 'placeholder': f.placeholder,
#                 'is_required': f.is_required,
#                 'options': f.options,
#                 'default_value': f.default_value,
#                 'order': f.order,
#             }
#             for f in form_obj.fields.all()
#         ]
#     }
#     return JsonResponse(data)


@login_required
@require_http_methods(["DELETE"])
def delete_form(request, pk):
    form_obj = get_object_or_404(DynamicForm, pk=pk, created_by=request.user)
    form_obj.delete()
    return JsonResponse({'success': True, 'message': 'Form deleted.'})


# ─── EMPLOYEE VIEWS ───────────────────────────────────────────────────────────


def employee_list(request):
    return render(request, 'employees/employee_list.html')



def employee_create(request):
    return render(request, 'employees/employee_form.html')



def employee_edit(request, pk):
    return render(request, 'employees/employee_form.html')



def save_employee(request):
    pass



@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
@require_http_methods(["DELETE"])
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return JsonResponse({'success': True, 'message': 'Employee deleted.'})


@login_required
def get_form_fields(request, pk):
    """Return form fields as JSON for dynamic form rendering."""
    form_obj = get_object_or_404(DynamicForm, pk=pk)
    fields = [
        {
            'id': f.id,
            'label': f.label,
            'field_type': f.field_type,
            'placeholder': f.placeholder,
            'is_required': f.is_required,
            'options': f.get_options_list(),
            'default_value': f.default_value,
            'field_name': f.field_name,
        }
        for f in form_obj.fields.all()
    ]
    return JsonResponse({'fields': fields})
