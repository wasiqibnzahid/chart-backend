import ast
from django import forms
from django.contrib import messages
from django.contrib import admin

from server.utils import process_data_and_create_records
from .models import DataUpload, Record,ErrorLog,Site,LocalRecord,LocalErrorLog,LocalSite
# Register your models here.

class DataUploadAdminForm(forms.ModelForm):
    class Meta:
        model = DataUpload
        fields = ['data', 'target_model', 'process_amp_values']

    def clean_data(self):
        data = self.cleaned_data['data']
        try:
            # Try to parse the data as a dictionary
            parsed_data = ast.literal_eval(data)
            if not isinstance(parsed_data, dict):
                raise ValueError
        except Exception as e:
            raise forms.ValidationError("Invalid data format. Please ensure you're entering a valid Python dictionary.")
        return parsed_data

class DataUploadAdmin(admin.ModelAdmin):
    form = DataUploadAdminForm

    def save_model(self, request, obj, form, change):
        # Get the cleaned data (parsed dictionary)
        data = form.cleaned_data['data']
        target_model = form.cleaned_data['target_model']
        process_amp_values = form.cleaned_data['process_amp_values']
        # Process the data to create records
        errors = process_data_and_create_records(data, target_model, process_amp_values)
        if errors:
            messages.error(request, f"Data processed with errors: {errors}")
        else:
            messages.success(request, "Data processed successfully.")
        # Optionally save the DataUpload instance
        super().save_model(request, obj, form, change)

admin.site.register(DataUpload, DataUploadAdmin)

admin.site.register(Site)
admin.site.register(Record)
admin.site.register(ErrorLog)


admin.site.register(LocalSite)
admin.site.register(LocalRecord)
admin.site.register(LocalErrorLog)