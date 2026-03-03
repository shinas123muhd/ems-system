from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import DynamicForm, FormField, Employee
from .serializers import (
    DynamicFormListSerializer, DynamicFormDetailSerializer, DynamicFormWriteSerializer,
    FormFieldSerializer, EmployeeListSerializer, EmployeeDetailSerializer, EmployeeWriteSerializer
)


#  FORMS

class FormListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forms = DynamicForm.objects.filter(created_by=request.user)
        serializer = DynamicFormListSerializer(forms, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = DynamicFormWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return DynamicForm.objects.get(pk=pk, created_by=user)
        except DynamicForm.DoesNotExist:
            return None

    def get(self, request, pk):
        form = self.get_object(pk, request.user)
        if not form:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DynamicFormDetailSerializer(form)
        return Response(serializer.data)

    def put(self, request, pk):
        form = self.get_object(pk, request.user)
        if not form:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DynamicFormWriteSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        form = self.get_object(pk, request.user)
        if not form:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DynamicFormWriteSerializer(form, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = self.get_object(pk, request.user)
        if not form:
            return Response({'error': 'Form not found.'}, status=status.HTTP_404_NOT_FOUND)
        form.delete()
        return Response({'message': 'Form deleted.'})


class FormFieldsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        fields = FormField.objects.filter(
            form_id=pk,
            form__created_by=request.user  
        )
        serializer = FormFieldSerializer(fields, many=True)
        return Response(serializer.data)


# EMPLOYEES
class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Employee.objects.select_related('form').all()

        search      = request.query_params.get('search', '')
        form_id     = request.query_params.get('form_id', '')
        field_label = request.query_params.get('field_label', '')
        field_value = request.query_params.get('field_value', '')

        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)  |
                Q(email__icontains=search)       |
                Q(employee_id__icontains=search)
            )

        if form_id:
            qs = qs.filter(form_id=form_id)

        if field_label and field_value:
            qs = qs.filter(
                field_values__form_field__label__icontains=field_label,
                field_values__value__icontains=field_value
            )

       
        serializer = EmployeeListSerializer(qs.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # helper — fetch employee by id, return None if not found
    def get_object(self, pk):
        try:
            return Employee.objects.select_related('form').prefetch_related(
                'field_values__form_field'
            ).get(pk=pk)
        except Employee.DoesNotExist:
            return None

    # return a single employee with all dynamic field values
    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeDetailSerializer(employee)
        return Response(serializer.data)

    #fully update an employee
    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeWriteSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /api/employees/1/ — partially update an employee
    def patch(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeWriteSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/employees/1/ — delete an employee
    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        employee.delete()
        return Response({'message': 'Employee deleted.'})




