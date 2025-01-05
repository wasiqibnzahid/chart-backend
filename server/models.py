from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

from django.db import models

from server.constants import DEFAULT_DECIMAL_PLACES, DEFAULT_MAX_DIGITS


class RecordCommonFields(models.Model):
    note_first_contentful_paint = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) from page load to the first visible content. Lower values are better."
    )

    note_total_blocking_time = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Total time (in seconds) the page was unresponsive to user input. High values indicate poor interactivity."
    )

    note_speed_index = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) for the page's content to become visually complete. Lower values are better."
    )

    note_largest_contentful_paint = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) to render the largest visible content element. Lower values indicate faster rendering."
    )

    note_cumulative_layout_shift = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Score indicating unexpected layout shifts. Lower values are better."
    )

    video_first_contentful_paint = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) from video page load to the first visible content. Lower values are better."
    )

    video_total_blocking_time = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Total time (in seconds) the video page was unresponsive to user input. High values indicate poor interactivity."
    )

    video_speed_index = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) for video page content to become visually complete. Lower values are better."
    )

    video_largest_contentful_paint = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Time (in seconds) to render the largest visible content element on the video page. Lower values improve UX."
    )

    video_cumulative_layout_shift = models.DecimalField(
        max_digits=DEFAULT_MAX_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        default=0,
        help_text="Score indicating unexpected layout shifts on the video page. Lower values are better."
    )

    class Meta:
        abstract = True


class Site(models.Model):
    name = models.CharField(max_length=255)
    sitemap_url = models.URLField(null=True, blank=True)
    video_sitemap_url = models.URLField(null=True, blank=True)
    note_sitemap_url = models.URLField(null=True, blank=True)
    video_urls = models.JSONField(null=True, blank=True)
    note_urls = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Record(RecordCommonFields):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, null=True, blank=True)
    note_value = models.FloatField(null=True, blank=True)
    video_value = models.FloatField(null=True, blank=True)
    total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.name} - {self.total_value} - {self.date}"


class ErrorLog(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"


class LocalSite(models.Model):
    name = models.CharField(max_length=255)
    sitemap_url = models.URLField(null=True, blank=True)
    video_sitemap_url = models.URLField(null=True, blank=True)
    note_sitemap_url = models.URLField(null=True, blank=True)
    video_urls = models.JSONField(null=True, blank=True)
    note_urls = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class LocalRecord(RecordCommonFields):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(
        LocalSite, on_delete=models.CASCADE, null=True, blank=True)
    note_value = models.FloatField(null=True, blank=True)
    video_value = models.FloatField(null=True, blank=True)
    total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.name} - {self.total_value} - {self.date}"


class AmpRecord(RecordCommonFields):
    name = models.CharField(max_length=255)
    note_value = models.FloatField(null=True, blank=True)
    video_value = models.FloatField(null=True, blank=True)
    total_value = models.FloatField(null=True, blank=True)
    azteca = models.BooleanField(default=False)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.name} - {self.total_value} - {self.date}"


class LocalErrorLog(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"

# models.py


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
    target_model = models.CharField(
        max_length=20, choices=TARGET_MODEL_CHOICES, default='record')
    process_amp_values = models.BooleanField(
        choices=PROCESS_AMP_CHOICES, default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data upload on {self.uploaded_at}"


class WebsiteCheck(RecordCommonFields):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('waiting', 'Waiting'),
        ('failed', 'Failed'),
        ('done', 'Done')
    ]

    url = models.URLField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True  # Create index on status field
    )
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    json_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.url} - {self.status}"


class LastJobRun(models.Model):
    last_run = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    @classmethod
    def update_last_run(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        obj.last_run = timezone.now()
        obj.save()

    @classmethod
    def should_run(cls):
        obj, _ = cls.objects.get_or_create(
            id=1,
            defaults={'last_run': timezone.now() - timedelta(days=1)}
        )

        now = timezone.now()

        # Check if it's Monday between 4-6 AM
        is_monday = now.weekday() == 0
        is_time_window = 4 <= now.hour < 6
        # add print to now time and compared time values
        print(f"is_monday: {is_monday}, is_time_window: {is_time_window}, now: {now}, last_run: {obj.last_run}")
        # Check if last run was not today
        last_run_not_today = obj.last_run.date() != now.date()

        return is_monday and is_time_window and last_run_not_today
