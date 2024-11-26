import ast
from django import forms
from django.contrib import messages
from django.contrib import admin

from server.utils import process_data_and_create_records
from .models import AmpRecord, DataUpload, Record,ErrorLog,Site,LocalRecord,LocalErrorLog,LocalSite
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
    search_fields = ('data', 'target_model')
    list_filter = ('target_model', 'process_amp_values', 'uploaded_at')
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

# Site Admin
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'sitemap_url', 'video_sitemap_url', 'note_sitemap_url')
    search_fields = ('name',)
    list_filter = ('name',)  # Filter by name or other fields you want

admin.site.register(Site, SiteAdmin)

# Record Admin
class RecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'note_value', 'video_value', 'total_value', 'date', 'azteca')
    search_fields = ('name', 'site__name')  # Allow search by site name
    list_filter = ('azteca', 'date', 'site')  # Add filter for azteca, date, and site

admin.site.register(Record, RecordAdmin)

# ErrorLog Admin
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)  # Filter by the creation date of the log

admin.site.register(ErrorLog, ErrorLogAdmin)

# LocalSite Admin
class LocalSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'sitemap_url', 'video_sitemap_url', 'note_sitemap_url')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(LocalSite, LocalSiteAdmin)

# LocalRecord Admin
class LocalRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'note_value', 'video_value', 'total_value', 'azteca', 'date')
    search_fields = ('name', 'site__name')  # Allow search by site name
    list_filter = ('azteca', 'date', 'site')  # Filter by azteca, date, and site

admin.site.register(LocalRecord, LocalRecordAdmin)

# AmpRecord Admin
class AmpRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'amp_note_value', 'amp_video_value', 'amp_total_value', 'azteca', 'date')
    search_fields = ('name',)
    list_filter = ('azteca', 'date')  # Filter by azteca and date

admin.site.register(AmpRecord, AmpRecordAdmin)

# LocalErrorLog Admin
class LocalErrorLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)

admin.site.register(LocalErrorLog, LocalErrorLogAdmin)

