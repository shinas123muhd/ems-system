from django.db import models
from django.conf import settings


FIELD_TYPES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('email', 'Email'),
    ('date', 'Date'),
    ('password', 'Password'),
    ('textarea', 'Textarea'),
    ('select', 'Select/Dropdown'),
    ('checkbox', 'Checkbox'),
    ('radio', 'Radio'),
    ('tel', 'Phone'),
    ('url', 'URL'),
]


class DynamicForm(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def fields_count(self):
        return self.fields.count()


class FormField(models.Model):
    form = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES, default='text')
    placeholder = models.CharField(max_length=200, blank=True)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    options = models.TextField(blank=True, help_text='Comma-separated options for select/radio')
    default_value = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.form.name} - {self.label}"

    def get_options_list(self):
        if self.options:
            return [opt.strip() for opt in self.options.split(',') if opt.strip()]
        return []

    @property
    def field_name(self):
        return f"field_{self.id}"


class Employee(models.Model):
    form = models.ForeignKey(DynamicForm, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            from django.db.models import Max
            max_id = Employee.objects.aggregate(Max('id'))['id__max'] or 0
            self.employee_id = f"EMP{(max_id + 1):04d}"
        super().save(*args, **kwargs)


class EmployeeFieldValue(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='field_values')
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)
    value = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'form_field')

    def __str__(self):
        return f"{self.employee} - {self.form_field.label}: {self.value}"
