# Generated by Django 5.1 on 2024-10-20 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_errorlog_localerrorlog_localrecord_localsite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localsite',
            name='note_sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='localsite',
            name='note_urls',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='localsite',
            name='sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='localsite',
            name='video_sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='localsite',
            name='video_urls',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='note_sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='note_urls',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='video_sitemap_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='video_urls',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
