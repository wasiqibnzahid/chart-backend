from django.db import models
from datetime import datetime, timedelta


class Site(models.Model):
    name = models.CharField(max_length=255)
    sitemap_url = models.URLField(null=True,blank=True)
    video_sitemap_url = models.URLField(null=True,blank=True)
    note_sitemap_url = models.URLField(null=True,blank=True)
    video_urls = models.JSONField(null=True,blank=True)
    note_urls = models.JSONField(null=True,blank=True)

    def __str__(self):
        return self.name



class Record(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)
    note_value = models.FloatField(null=True, blank=True)
    video_value = models.FloatField(null=True, blank=True)
    total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)

    # def save(self, *args, **kwargs):
    #     # Set date to the Monday of the current week
    #     today = datetime.today()
    #     monday_of_current_week = today - timedelta(days=today.weekday())
    #     self.date = monday_of_current_week.date()

    #     # Calculate the total_value as the average of note_value and video_value
    #     if self.note_value is not None and self.video_value is not None:
    #         self.total_value = (self.note_value + self.video_value) / 2
    #     else:
    #         self.total_value = None

    #     super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.total_value} - {self.date}"


class ErrorLog(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"



class LocalSite(models.Model):
    name = models.CharField(max_length=255)
    sitemap_url = models.URLField(null=True,blank=True)
    video_sitemap_url = models.URLField(null=True,blank=True)
    note_sitemap_url = models.URLField(null=True,blank=True)
    video_urls = models.JSONField(null=True,blank=True)
    note_urls = models.JSONField(null=True,blank=True)

    def __str__(self):
        return self.name



class LocalRecord(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(LocalSite, on_delete=models.CASCADE, null=True, blank=True)
    note_value = models.FloatField(null=True, blank=True)
    video_value = models.FloatField(null=True, blank=True)
    total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)
    
class AmpRecord(models.Model):
    name = models.CharField(max_length=255)
    amp_note_value = models.FloatField(null=True, blank=True)
    amp_video_value = models.FloatField(null=True, blank=True)
    amp_total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)

    # def save(self, *args, **kwargs):
    #     # Set date to the Monday of the current week
    #     today = datetime.today()
    #     monday_of_current_week = today - timedelta(days=today.weekday())
    #     self.date = monday_of_current_week.date()

    #     # Calculate the total_value as the average of note_value and video_value
    #     if self.note_value is not None and self.video_value is not None:
    #         self.total_value = (self.note_value + self.video_value) / 2
    #     else:
    #         self.total_value = None

    #     super(Record, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.amp_total_value} - {self.date}"


class LocalErrorLog(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"
    
# models.py

from django.db import models

class DataUpload(models.Model):
    TARGET_MODEL_CHOICES = [
        ('record', 'Record'),
        ('localrecord', 'LocalRecord'),
    ]
    PROCESS_AMP_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    data = models.TextField(help_text="Paste your data here.")
    target_model = models.CharField(max_length=20, choices=TARGET_MODEL_CHOICES, default='record')
    process_amp_values = models.BooleanField(choices=PROCESS_AMP_CHOICES, default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data upload on {self.uploaded_at}"

