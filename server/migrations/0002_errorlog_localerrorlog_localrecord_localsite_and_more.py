# Generated by Django 5.1 on 2024-10-13 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocalErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note_value', models.FloatField(blank=True, null=True)),
                ('video_value', models.FloatField(blank=True, null=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
                ('azteca', models.BooleanField(default=False)),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocalSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sitemap_url', models.URLField(null=True)),
                ('video_sitemap_url', models.URLField(null=True)),
                ('note_sitemap_url', models.URLField(null=True)),
                ('video_urls', models.JSONField(null=True)),
                ('note_urls', models.JSONField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='azteca',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='site',
            name='note_urls',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='video_urls',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='note_sitemap_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='sitemap_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='video_sitemap_url',
            field=models.URLField(null=True),
        ),
        migrations.DeleteModel(
            name='Website',
        ),
    ]
