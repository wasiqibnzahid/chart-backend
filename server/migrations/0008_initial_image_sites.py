from django.db import migrations

def create_initial_sites(apps, schema_editor):
    ImageSite = apps.get_model('server', 'ImageSite')
    sites_data = [
        ('Azteca Uno', 'https://www.tvazteca.com/aztecauno/sitemap-image.xml'),
        ('Azteca 7', 'https://www.tvazteca.com/azteca7/sitemap-image.xml'),
        ('Azteca Deportes', 'https://www.tvazteca.com/aztecadeportes/sitemap-image.xml'),
        ('ADN 40', 'https://www.adn40.mx/sitemap-image.xml'),
        ('Azteca Noticias', 'https://www.tvazteca.com/aztecanoticias/sitemap-image.xml'),
        ('Amas TV', 'https://www.tvazteca.com/amastv/sitemap-image.xml'),
    ]
    
    for name, url in sites_data:
        ImageSite.objects.get_or_create(name=name, sitemap_url=url)

def remove_initial_sites(apps, schema_editor):
    ImageSite = apps.get_model('server', 'ImageSite')
    ImageSite.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_imagesite_lastjobrun_websitecheck_imagerecord'),
    ]

    operations = [
        migrations.RunPython(create_initial_sites, remove_initial_sites),
    ] 