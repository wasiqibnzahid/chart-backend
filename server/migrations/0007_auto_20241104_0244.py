# Generated by Django 5.1 on 2024-11-03 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_auto_20241104_0230'),
    ]

    operations = [
        # remove sql syntax errors
        migrations.RunSQL('''
                          delete from server_localrecord where date = '2024-10-14';
                          INSERT INTO server_localrecord (name, note_value, video_value, total_value, azteca, date) VALUES
                          -- Week of October 14, 2024
                          ('Azteca Veracruz', 64, 67, 65.5, true, '2024-10-14'),
('Azteca Quintanaroo', 67, 67, 67.0, true, '2024-10-14'),
('Azteca BajaCalifornia', 60, 67, 63.5, true, '2024-10-14'),
('Azteca Sinaloa', 60, 65, 62.5, true, '2024-10-14'),
('Azteca Ciudad Juarez', 68, 66, 67.0, true, '2024-10-14'),
('Azteca Aguascalientes', 62, 64, 63.0, true, '2024-10-14'),
('Azteca Queretaro', 64, 62, 63.0, true, '2024-10-14'),
('Azteca Chiapas', 63, 65, 64.0, true, '2024-10-14'),
('Azteca Puebla', 62, 64, 63.0, true, '2024-10-14'),
('Azteca Yucatan', 65, 65, 65.0, true, '2024-10-14'),
('Azteca Chihuahua', 61, 64, 62.5, true, '2024-10-14'),
('Azteca Morelos', 66, 64, 65.0, true, '2024-10-14'),
('Azteca Jalisco', 66, 65, 65.5, true, '2024-10-14'),
('Azteca Guerrero', 64, 66, 65.0, true, '2024-10-14'),
('Azteca Bajio', 66, 64, 65.0, true, '2024-10-14');

INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
-- Week of October 21, 2024
('Azteca UNO', 65, 64, 64.5, true, '2024-10-21'),
('Azteca 7', 66, 65, 65.5, true, '2024-10-21'),
('Deportes', 63, 66, 64.5, true, '2024-10-21'),
('ADN40', 63, 68, 65.5, true, '2024-10-21'),
('A+', 66, 65, 65.5, true, '2024-10-21'),
('Noticias', 68, 69, 68.5, true, '2024-10-21'),
('Milenio', 14, 38, 26.0, false, '2024-10-21'),
('El Heraldo', 88, 88, 88.0, false, '2024-10-21'),
('El Universal', 48, 51, 49.5, false, '2024-10-21'),
('Televisa', 82, 53, 67.5, false, '2024-10-21'),
('Terra', 80, 64, 72.0, false, '2024-10-21'),
('AS', 78, 78, 78.0, false, '2024-10-21'),
('Infobae', 91, 69, 80.0, false, '2024-10-21'),
('NY Times', 47, 33, 40.0, false, '2024-10-21'),

-- Week of October 28, 2024
('Azteca UNO', 67, 66, 66.5, true, '2024-10-28'),
('Azteca 7', 67, 68, 67.5, true, '2024-10-28'),
('Deportes', 65, 64, 64.5, true, '2024-10-28'),
('ADN40', 65, 67, 66.0, true, '2024-10-28'),
('A+', 62, 64, 63.0, true, '2024-10-28'),
('Noticias', 69, 67, 68.0, true, '2024-10-28'),
('Milenio', 48, 48, 48.0, false, '2024-10-28'),
('El Heraldo', 100, 90, 95.0, false, '2024-10-28'),
('El Universal', 44, 54, 49.0, false, '2024-10-28'),
('Televisa', 41, 46, 43.5, false, '2024-10-28'),
('Terra', 60, 62, 61.0, false, '2024-10-28'),
('AS', 64, 65, 64.5, false, '2024-10-28'),
('Infobae', 68, 59, 63.5, false, '2024-10-28'),
('NY Times', 31, 32, 31.5, false, '2024-10-28'); 
        ''')
    ]
