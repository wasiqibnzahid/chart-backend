import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tv_charts.settings')

# Setup Django
django.setup()

# Now you can import models and access Django settings

from server.models import Record


data = {
    'Date': [
        '2024-06-17', 
        '2024-06-25', 
        '2024-07-02', 
        '2024-07-08', 
        '2024-07-22', 
        '2024-07-29', 
        '2024-08-05', 
        '2024-08-12', 
        '2024-08-19',
        '2024-08-26',
        '2024-09-02',
        '2024-09-07',
        '2024-09-16',
        '2024-09-23',
        '2024-09-30',
        '2024-10-07',
        '2024-10-14'

        
],

    'Azteca UNO (Note)': [78, 74, 77, 78, 69, 72, 64, 66, 66, 66, 68, 69, 64, 61, 63, 62, 64],
    'Azteca UNO (Video)': [63, 81, 79, 76, 67, 71, 71, 69, 72, 71, 72, 71, 69, 67, 65, 62, 64],
    'Azteca 7 (Note)': [63, 64, 64, 63, 67, 65, 64, 67, 66, 69, 66, 63, 60, 62, 62, 63, 64],
    'Azteca 7 (Video)': [59, 80, 65, 65, 72, 74, 73, 70, 72, 68, 65, 62, 67, 66, 66, 64, 69],
    'Deportes (Note)': [56, 63, 64, 65, 64, 65, 64, 68, 65, 66, 65, 65, 64, 63, 61, 63, 63],
    'Deportes (Video)': [64, 61, 63, 64, 66, 65, 58, 60, 66, 63, 66, 63, 64, 63, 62, 65, 66],
    'ADN40 (Note)': [53, 59, 59, 60, 58, 67, 66, 65, 65, 60, 66, 62, 63, 63, 63, 61, 62],
    'ADN40 (Video)': [64, 83, 67, 68, 66, 70, 73, 72, 65, 65, 69, 66, 66, 67, 65, 66, 67],
    'A+ (Note)': [76, 75, 80, 78, 72, 74, 72, 72, 72, 68, 66, 65, 63, 64, 64, 64, 66],
    'A+ (Video)': [71, 83, 85, 84, 75, 71, 70, 75, 75, 66, 62, 64, 62, 63, 62, 64, 66],
    'Noticias (Note)': [63, 63, 64, 64, 63, 67, 55, 77, 76, 71, 72, 71, 71, 70, 71, 71, 69],
    'Noticias (Video)': [81, 75, 77, 78, 83, 75, 81, 80, 77, 70, 75, 74, 66, 65, 67, 67, 68],
    'Milenio (Note)': [84, 59, 30, 30, 52, 33, 34, 67, 60, 67, 57, 69, 68, 60, 50, 59, 24],
    'Milenio (Video)': [65, 54, 46, 46, 49, 47, 55, 65, 66, 60, 63, 61, 60, 58, 59, 54, 49],
    'El Heraldo (Note)': [90, 83, 90, 80, 80, 80, 80, 99, 91, 98, 93, 98, 95, 94, 100, 100, 100],
    'El Heraldo (Video)': [89, 81, 87, 81, 81, 81, 81, 94, 92, 99, 86, 99, 94, 93, 95, 93, 100],
    'El Universal (Note)': [55, 34, 34, 56, 34, 34, 25, 47, 47, 68, 44, 42, 56, 44, 35, 40, 43],
    'El Universal (Video)': [45, 35, 34, 30, 30, 34, 56, 45, 46, 87, 27, 48, 50, 51, 52, 37, 34],
    'Televisa (Note)': [71, 50, 34, 46, 53, 34, 55, 66, 59, 63, 57, 64, 53, 52, 36, 51, 38],
    'Televisa (Video)': [38, 54, 29, 23, 19, 29, 25, 50, 18, 16, 41, 18, 17, 15, 14, 15, 29],
    'Terra (Note)': [80, 76, 80, 80, 80, 80, 73, 77, 84, 89, 94, 88, 87, 89, 92, 91, 87],
    'Terra (Video)': [87, 84, 82, 82, 82, 82, 91, 87, 70, 90, 94, 89, 79, 83, 91, 81, 94],
    'AS (Note)': [89, 74, 71, 58, 25, 25, 34, 58, 90, 89, 88, 87, 89, 89, 91, 92, 85],
    'AS (Video)': [70, 82, 61, 35, 45, 45, 52, 61, 77, 96, 92, 89, 87, 90, 88, 86, 74],
    'Infobae (Note)': [72, 31, 49, 26, 47, 29, 30, 59, 47, 69, 62, 60, 58, 56, 59, 61, 58],
    'Infobae (Video)': [60, 45, 51, 35, 55, 35, 35, 58, 50, 67, 55, 66, 55, 56, 52, 42, 64],
    'NY Times (Note)': [45, 33, 44, 53, 25, 37, 45, 60, 59, 36, 51, 36, 44, 33, 37, 33, 32],
    'NY Times (Video)': [36, 45, 30, 37, 25, 39, 54, 41, 40, 42, 39, 37, 38, 31, 34, 34, 49],
}

names = [
    "Azteca UNO (Note)",
    "Azteca UNO (Video)",
    "Azteca 7 (Note)",
    "Azteca 7 (Video)", 
    "Deportes (Note)", 
    "Deportes (Video)", 
    "ADN40 (Note)", 
    "ADN40 (Video)",
    "A+ (Note)", 
    "A+ (Video)", 
    "Noticias (Note)",
    "Noticias (Video)",
    "Milenio (Note)",
    "Milenio (Video)",
    "El Heraldo (Note)",
    "El Heraldo (Video)",
    "El Universal (Note)",
    "El Universal (Video)",
    "Televisa (Note)",
    "Televisa (Video)",
    "Terra (Note)",
    "Terra (Video)",
    "AS (Note)",
    "AS (Video)",
    "Infobae (Note)",
    "Infobae (Video)",
    "NY Times (Note)",
    "NY Times (Video)"
          ] 


for i in range(len(data['Date'])):
    date = data['Date'][i]
    
    for name in names:
        video_value = 0
        note_value = 0
        if name.endswith("(Note)"):
            note_value = data[name][i]
            video_value = data[name.replace("(Note)", "(Video)")][i]
        elif name.endswith("(Video)"):
            continue 
        total_value = (note_value + video_value) / 2  
        
        record =  {
                "name": name.split("(")[0].strip(),
                "note_value": float(note_value),
                "video_value": float(video_value),
                "total_value": float(total_value),
                "azteca": True if name.startswith("Azteca") else False,
                "date": date
            }
        
        Record.objects.create(**record)

