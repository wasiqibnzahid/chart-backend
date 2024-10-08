# Generated by Django 5.1 on 2024-09-03 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note_value', models.FloatField(blank=True, null=True)),
                ('video_value', models.FloatField(blank=True, null=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sitemap_url', models.URLField()),
                ('video_sitemap_url', models.URLField()),
                ('note_sitemap_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='websites', to='server.site')),
            ],
        ),
    ]
