# Generated by Django 5.1 on 2024-09-05 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_record_azteca'),
    ]

    operations = [
        migrations.RunSQL('''
BEGIN;

-- Inserting records for 'Azteca UNO'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Azteca UNO', 78, 63, (78 + 63) / 2, true, '2024-06-17'),
    ('Azteca UNO', 74, 81, (74 + 81) / 2, true, '2024-06-25'),
    ('Azteca UNO', 77, 79, (77 + 79) / 2, true, '2024-07-02'),
    ('Azteca UNO', 78, 76, (78 + 76) / 2, true, '2024-07-08'),
    ('Azteca UNO', 69, 71, (69 + 71) / 2, true, '2024-07-22'),
    ('Azteca UNO', 72, 74, (72 + 74) / 2, true, '2024-07-29'),
    ('Azteca UNO', 64, 71, (64 + 71) / 2, true, '2024-08-05'),
    ('Azteca UNO', 66, 69, (66 + 69) / 2, true, '2024-08-12'),
    ('Azteca UNO', 66, 72, (66 + 72) / 2, true, '2024-08-19');

-- Inserting records for 'Azteca 7'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Azteca 7', 63, 59, (63 + 59) / 2, true, '2024-06-17'),
    ('Azteca 7', 64, 68, (64 + 68) / 2, true, '2024-06-25'),
    ('Azteca 7', 65, 64, (65 + 64) / 2, true, '2024-07-02'),
    ('Azteca 7', 63, 67, (63 + 67) / 2, true, '2024-07-08'),
    ('Azteca 7', 67, 70, (67 + 70) / 2, true, '2024-07-22'),
    ('Azteca 7', 65, 74, (65 + 74) / 2, true, '2024-07-29'),
    ('Azteca 7', 65, 66, (65 + 66) / 2, true, '2024-08-05'),
    ('Azteca 7', 67, 70, (67 + 70) / 2, true, '2024-08-12'),
    ('Azteca 7', 66, 72, (66 + 72) / 2, true, '2024-08-19');

-- Inserting records for 'Deportes'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Deportes', 56, 64, (56 + 64) / 2, true, '2024-06-17'),
    ('Deportes', 61, 59, (61 + 59) / 2, true, '2024-06-25'),
    ('Deportes', 59, 63, (59 + 63) / 2, true, '2024-07-02'),
    ('Deportes', 64, 68, (64 + 68) / 2, true, '2024-07-08'),
    ('Deportes', 67, 67, (67 + 67) / 2, true, '2024-07-22'),
    ('Deportes', 65, 66, (65 + 66) / 2, true, '2024-07-29'),
    ('Deportes', 60, 65, (60 + 65) / 2, true, '2024-08-05'),
    ('Deportes', 66, 66, (66 + 66) / 2, true, '2024-08-12'),
    ('Deportes', 65, 66, (65 + 66) / 2, true, '2024-08-19');

-- Inserting records for 'ADN40'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('ADN40', 53, 64, (53 + 64) / 2, true, '2024-06-17'),
    ('ADN40', 59, 83, (59 + 83) / 2, true, '2024-06-25'),
    ('ADN40', 59, 67, (59 + 67) / 2, true, '2024-07-02'),
    ('ADN40', 60, 68, (60 + 68) / 2, true, '2024-07-08'),
    ('ADN40', 53, 69, (53 + 69) / 2, true, '2024-07-22'),
    ('ADN40', 67, 70, (67 + 70) / 2, true, '2024-07-29'),
    ('ADN40', 58, 66, (58 + 66) / 2, true, '2024-08-05'),
    ('ADN40', 67, 67, (67 + 67) / 2, true, '2024-08-12'),
    ('ADN40', 65, 65, (65 + 65) / 2, true, '2024-08-19');

-- Inserting records for 'A+'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('A+', 76, 74, (76 + 74) / 2, true, '2024-06-17'),
    ('A+', 83, 75, (83 + 75) / 2, true, '2024-06-25'),
    ('A+', 80, 85, (80 + 85) / 2, true, '2024-07-02'),
    ('A+', 78, 73, (78 + 73) / 2, true, '2024-07-08'),
    ('A+', 84, 80, (84 + 80) / 2, true, '2024-07-22'),
    ('A+', 74, 77, (74 + 77) / 2, true, '2024-07-29'),
    ('A+', 73, 72, (73 + 72) / 2, true, '2024-08-05'),
    ('A+', 75, 75, (75 + 75) / 2, true, '2024-08-12'),
    ('A+', 72, 77, (72 + 77) / 2, true, '2024-08-19');

-- Inserting records for 'Noticias'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Noticias', 71, 63, (71 + 63) / 2, true, '2024-06-17'),
    ('Noticias', 83, 75, (83 + 75) / 2, true, '2024-06-25'),
    ('Noticias', 85, 64, (85 + 64) / 2, true, '2024-07-02'),
    ('Noticias', 83, 76, (83 + 76) / 2, true, '2024-07-08'),
    ('Noticias', 77, 63, (77 + 63) / 2, true, '2024-07-22'),
    ('Noticias', 84, 74, (84 + 74) / 2, true, '2024-07-29'),
    ('Noticias', 73, 55, (73 + 55) / 2, true, '2024-08-05'),
    ('Noticias', 70, 76, (70 + 76) / 2, true, '2024-08-12'),
    ('Noticias', 75, 77, (75 + 77) / 2, true, '2024-08-19');

-- Inserting records for 'Milenio'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Milenio', 81, 84, (81 + 84) / 2, false, '2024-06-17'),
    ('Milenio', 83, 75, (83 + 75) / 2, false, '2024-06-25'),
    ('Milenio', 84, 77, (84 + 77) / 2, false, '2024-07-02'),
    ('Milenio', 83, 80, (83 + 80) / 2, false, '2024-07-08'),
    ('Milenio', 52, 49, (52 + 49) / 2, false, '2024-07-22'),
    ('Milenio', 33, 47, (33 + 47) / 2, false, '2024-07-29'),
    ('Milenio', 34, 46, (34 + 46) / 2, false, '2024-08-05'),
    ('Milenio', 77, 66, (77 + 66) / 2, false, '2024-08-12'),
    ('Milenio', 60, 66, (60 + 66) / 2, false, '2024-08-19');

INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('El Heraldo', 90, 89, (90 + 89) / 2, false, '2024-06-17'),
    ('El Heraldo', 83, 81, (83 + 81) / 2, false, '2024-06-25'),
    ('El Heraldo', 90, 87, (90 + 87) / 2, false, '2024-07-02'),
    ('El Heraldo', 80, 82, (80 + 82) / 2, false, '2024-07-08'),
    ('El Heraldo', 80, 51, (80 + 51) / 2, false, '2024-07-22'),
    ('El Heraldo', 83, 49, (83 + 49) / 2, false, '2024-07-29'),
    ('El Heraldo', 56, 52, (56 + 52) / 2, false, '2024-08-05'),
    ('El Heraldo', 67, 59, (67 + 59) / 2, false, '2024-08-12'),
    ('El Heraldo', 91, 92, (91 + 92) / 2, false, '2024-08-19');

-- Inserting records for 'El Universal'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('El Universal', 55, 45, (55 + 45) / 2, false, '2024-06-17'),
    ('El Universal', 81, 34, (81 + 34) / 2, false, '2024-06-25'),
    ('El Universal', 87, 34, (87 + 34) / 2, false, '2024-07-02'),
    ('El Universal', 56, 30, (56 + 30) / 2, false, '2024-07-08'),
    ('El Universal', 34, 30, (34 + 30) / 2, false, '2024-07-22'),
    ('El Universal', 34, 29, (34 + 29) / 2, false, '2024-07-29'),
    ('El Universal', 34, 25, (34 + 25) / 2, false, '2024-08-05'),
    ('El Universal', 47, 46, (47 + 46) / 2, false, '2024-08-12'),
    ('El Universal', 47, 46, (47 + 46) / 2, false, '2024-08-19');

-- Inserting records for 'Televisa'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Televisa', 71, 38, (71 + 38) / 2, false, '2024-06-17'),
    ('Televisa', 35, 50, (35 + 50) / 2, false, '2024-06-25'),
    ('Televisa', 34, 51, (34 + 51) / 2, false, '2024-07-02'),
    ('Televisa', 35, 48, (35 + 48) / 2, false, '2024-07-08'),
    ('Televisa', 53, 48, (53 + 48) / 2, false, '2024-07-22'),
    ('Televisa', 34, 47, (34 + 47) / 2, false, '2024-07-29'),
    ('Televisa', 34, 47, (34 + 47) / 2, false, '2024-08-05'),
    ('Televisa', 47, 48, (47 + 48) / 2, false, '2024-08-12'),
    ('Televisa', 59, 50, (59 + 50) / 2, false, '2024-08-19');

-- Inserting records for 'Terra'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Terra', 38, 80, (38 + 80) / 2, false, '2024-06-17'),
    ('Terra', 50, 54, (50 + 54) / 2, false, '2024-06-25'),
    ('Terra', 61, 49, (61 + 49) / 2, false, '2024-07-02'),
    ('Terra', 30, 53, (30 + 53) / 2, false, '2024-07-08'),
    ('Terra', 19, 80, (19 + 80) / 2, false, '2024-07-22'),
    ('Terra', 54, 71, (54 + 71) / 2, false, '2024-07-29'),
    ('Terra', 56, 82, (56 + 82) / 2, false, '2024-08-05'),
    ('Terra', 60, 84, (60 + 84) / 2, false, '2024-08-12'),
    ('Terra', 58, 70, (58 + 70) / 2, false, '2024-08-19');

-- Inserting records for 'AS'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('AS', 87, 89, (87 + 89) / 2, false, '2024-06-17'),
    ('AS', 74, 82, (74 + 82) / 2, false, '2024-06-25'),
    ('AS', 71, 87, (71 + 87) / 2, false, '2024-07-02'),
    ('AS', 25, 56, (25 + 56) / 2, false, '2024-07-08'),
    ('AS', 30, 37, (30 + 37) / 2, false, '2024-07-22'),
    ('AS', 25, 39, (25 + 39) / 2, false, '2024-07-29'),
    ('AS', 25, 41, (25 + 41) / 2, false, '2024-08-05'),
    ('AS', 77, 58, (77 + 58) / 2, false, '2024-08-12'),
    ('AS', 77, 90, (77 + 90) / 2, false, '2024-08-19');

-- Inserting records for 'Infobae'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('Infobae', 70, 72, (70 + 72) / 2, false, '2024-06-17'),
    ('Infobae', 31, 45, (31 + 45) / 2, false, '2024-06-25'),
    ('Infobae', 61, 49, (61 + 49) / 2, false, '2024-07-02'),
    ('Infobae', 58, 48, (58 + 48) / 2, false, '2024-07-08'),
    ('Infobae', 66, 47, (66 + 47) / 2, false, '2024-07-22'),
    ('Infobae', 63, 48, (63 + 48) / 2, false, '2024-07-29'),
    ('Infobae', 70, 49, (70 + 49) / 2, false, '2024-08-05'),
    ('Infobae', 59, 50, (59 + 50) / 2, false, '2024-08-12'),
    ('Infobae', 47, 50, (47 + 50) / 2, false, '2024-08-19');

-- Inserting records for 'NY Times'
INSERT INTO server_record (name, note_value, video_value, total_value, azteca, date) VALUES
    ('NY Times', 60, 36, (60 + 36) / 2, false, '2024-06-17'),
    ('NY Times', 33, 45, (33 + 45) / 2, false, '2024-06-25'),
    ('NY Times', 44, 44, (44 + 44) / 2, false, '2024-07-02'),
    ('NY Times', 47, 48, (47 + 48) / 2, false, '2024-07-08'),
    ('NY Times', 41, 47, (41 + 47) / 2, false, '2024-07-22'),
    ('NY Times', 54, 54, (54 + 54) / 2, false, '2024-07-29'),
    ('NY Times', 50, 41, (50 + 41) / 2, false, '2024-08-05'),
    ('NY Times', 59, 40, (59 + 40) / 2, false, '2024-08-12'),
    ('NY Times', 59, 40, (59 + 40) / 2, false, '2024-08-19');

COMMIT;
                          ''')
    ]