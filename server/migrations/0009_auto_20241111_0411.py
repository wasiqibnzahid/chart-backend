# Generated by Django 5.1 on 2024-11-10 23:11

from django.db import migrations


def add_laguna_site(apps, schema_editor):
    LocalSite = apps.get_model('server', 'LocalSite')
    LocalRecord = apps.get_model('server', 'LocalRecord')

    # Create Laguna site
    LocalSite.objects.create(
        name='Laguna',
        sitemap_url=None,
        video_sitemap_url='https://www.aztecalaguna.com/sitemap-video.xml',
        note_sitemap_url='https://www.aztecalaguna.com/sitemap-content.xml'
    )

    existing_dates = LocalRecord.objects.values_list(
        'date', flat=True).distinct()

    for date in existing_dates:
        if date:
            LocalRecord.objects.create(
                name='Laguna',
                note_value=0,
                video_value=0,
                total_value=0,
                azteca=True,
                date=date
            )


def update_sitemap_urls(apps, schema_editor):
    LocalSite = apps.get_model('server', 'LocalSite')
    
    sitemap_data = {
        'Azteca Quintanaroo': {
            'note': 'https://www.aztecaquintanaroo.com/sitemap-content.xml',
            'video': 'https://www.aztecaquintanaroo.com/sitemap-video.xml'
        },
        'Azteca Bajio': {
            'note': 'https://www.aztecabajio.com/sitemap-content.xml',
            'video': 'https://www.aztecabajio.com/sitemap-video.xml'
        },
        'Azteca CJ': {
            'note': 'https://www.aztecaciudadjuarez.com/sitemap-content.xml',
            'video': 'https://www.aztecaciudadjuarez.com/sitemap-video.xml'
        },
        'Azteca Yucatan': {
            'note': 'https://www.aztecayucatan.com/sitemap-content.xml',
            'video': 'https://www.aztecayucatan.com/sitemap-video.xml'
        },
        'Azteca Jalisco': {
            'note': 'https://www.aztecajalisco.com/sitemap-content.xml',
            'video': 'https://www.aztecajalisco.com/sitemap-video.xml'
        },
        'Azteca Puebla': {
            'note': 'https://www.aztecapuebla.com/sitemap-content.xml',
            'video': 'https://www.aztecapuebla.com/sitemap-video.xml'
        },
        'Azteca Veracruz': {
            'note': 'https://www.aztecaveracruz.com/sitemap-content.xml',
            'video': 'https://www.aztecaveracruz.com/sitemap-video.xml'
        },
        'Azteca BC': {
            'note': 'https://www.tvaztecabajacalifornia.com/sitemap-content.xml',
            'video': 'https://www.tvaztecabajacalifornia.com/sitemap-video.xml'
        },
        'Azteca Morelos': {
            'note': 'https://www.aztecamorelos.com/sitemap-content.xml',
            'video': 'https://www.aztecamorelos.com/sitemap-video.xml'
        },
        'Azteca Guerrero': {
            'note': 'https://www.aztecaguerrero.com/sitemap-content.xml',
            'video': 'https://www.aztecaguerrero.com/sitemap-video.xml'
        },
        'Azteca Chiapas': {
            'note': 'https://www.aztecachiapas.com/sitemap-content.xml',
            'video': 'https://www.aztecachiapas.com/sitemap-video.xml'
        },
        'Azteca Sinaloa': {
            'note': 'https://www.aztecasinaloa.com/sitemap-content.xml',
            'video': 'https://www.aztecasinaloa.com/sitemap-video.xml'
        },
        'Azteca Aguascalientes': {
            'note': 'https://www.aztecaaguascalientes.com/sitemap-content.xml',
            'video': 'https://www.aztecaaguascalientes.com/sitemap-video.xml'
        },
        'Azteca Queretaro': {
            'note': 'https://www.aztecaqueretaro.com/sitemap-content.xml',
            'video': 'https://www.aztecaqueretaro.com/sitemap-video.xml'
        },
        'Azteca Chihuahua': {
            'note': 'https://www.aztecachihuahua.com/sitemap-content.xml',
            'video': 'https://www.aztecachihuahua.com/sitemap-video.xml'
        }
    }

    for site_name, urls in sitemap_data.items():
        LocalSite.objects.filter(name=site_name).update(
            note_sitemap_url=urls['note'],
            video_sitemap_url=urls['video']
        )


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_auto_20241104_0258'),
    ]
    operations = [
        migrations.RunPython(add_laguna_site),
        migrations.RunPython(update_sitemap_urls),
    ]
