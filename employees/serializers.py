from rest_framework import serializers
from .models import DynamicForm, FormField, Employee, EmployeeFieldValue


class FormFieldSerializer(serializers.ModelSerializer):
    options_list = serializers.SerializerMethodField()

    class Meta:
        model = FormField
        fields = ('id', 'label', 'field_type', 'placeholder', 'is_required',
                  'order', 'options', 'options_list', 'default_value', 'field_name')
        read_only_fields = ('id', 'field_name', 'options_list')

    def get_options_list(self, obj):
        return obj.get_options_list()


class DynamicFormListSerializer(serializers.ModelSerializer):
    fields_count = serializers.ReadOnlyField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = DynamicForm
        fields = ('id', 'name', 'description', 'fields_count', 'is_active', 'created_by_name', 'created_at')

    def get_created_by_name(self, obj):
        return obj.created_by.full_name


class DynamicFormDetailSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, read_only=True)
    fields_count = serializers.ReadOnlyField()

    class Meta:
        model = DynamicForm
        fields = ('id', 'name', 'description', 'fields', 'fields_count', 'is_active', 'created_at', 'updated_at')


class DynamicFormWriteSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True, required=False)

    class Meta:
        model = DynamicForm
        fields = ('id', 'name', 'description', 'is_active', 'fields')

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        form = DynamicForm.objects.create(**validated_data)
        for i, f in enumerate(fields_data):
            f['order'] = f.get('order', i)
            FormField.objects.create(form=form, **f)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if fields_data is not None:
            instance.fields.all().delete()
            for i, f in enumerate(fields_data):
                f['order'] = f.get('order', i)
                FormField.objects.create(form=instance, **f)
        return instance


class EmployeeFieldValueSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    field_type = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeFieldValue
        fields = ('id', 'form_field', 'label', 'field_type', 'value')

    def get_label(self, obj):
        return obj.form_field.label

    def get_field_type(self, obj):
        return obj.form_field.field_type


class EmployeeListSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'employee_id', 'first_name', 'last_name', 'full_name', 'email', 'form', 'form_name', 'created_at')
        read_only_fields = ('id', 'employee_id', 'full_name')

    def get_form_name(self, obj):
        return obj.form.name if obj.form else None


class EmployeeDetailSerializer(serializers.ModelSerializer):
    field_values = EmployeeFieldValueSerializer(many=True, read_only=True)
    form_name = serializers.SerializerMethodField()
    form_fields = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'employee_id', 'first_name', 'last_name', 'full_name',
                  'email', 'form', 'form_name', 'form_fields', 'field_values', 'created_at', 'updated_at')
        read_only_fields = ('id', 'employee_id', 'full_name')

    def get_form_name(self, obj):
        return obj.form.name if obj.form else None

    def get_form_fields(self, obj):
        if obj.form:
            return FormFieldSerializer(obj.form.fields.all(), many=True).data
        return []


class EmployeeWriteSerializer(serializers.ModelSerializer):
    dynamic_fields = serializers.DictField(child=serializers.CharField(allow_blank=True), required=False, write_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'form', 'dynamic_fields')

    def create(self, validated_data):
        dynamic_fields = validated_data.pop('dynamic_fields', {})
        employee = Employee.objects.create(**validated_data)
        self._save_fields(employee, dynamic_fields)
        return employee

    def update(self, instance, validated_data):
        dynamic_fields = validated_data.pop('dynamic_fields', {})
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        self._save_fields(instance, dynamic_fields)
        return instance

    def _save_fields(self, employee, dynamic_fields):
        for key, value in dynamic_fields.items():
            if key.startswith('field_'):
                try:
                    fid = int(key.split('_')[1])
                    ff = FormField.objects.get(id=fid)
                    EmployeeFieldValue.objects.update_or_create(
                        employee=employee, form_field=ff, defaults={'value': value}
                    )
                except (FormField.DoesNotExist, ValueError):
                    pass
