import os
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tv_charts.settings')

# Setup Django
django.setup()

# Now you can import models and access Django settings
from server.models import LocalRecord


data = {
    'Date': [
        '2024-09-07',
        '2024-09-16',
        '2024-09-23',
        '2024-09-30',
        '2024-10-07'

    ],
    'Azteca Veracruz (Note)': [58, 60, 62, 60, 63],
    'Azteca Veracruz (Video)': [60, 61, 63, 60, 67],

    'Azteca Quintanaroo (Note)': [63, 61, 59, 63, 63],
    'Azteca Quintanaroo (Video)': [59, 62, 62, 64, 64],

    'Azteca BC (Note)': [60, 62, 59, 60, 60],
    'Azteca BC (Video)': [71, 66, 66, 68, 63],

    'Azteca Sinaloa (Note)': [60, 63, 61, 60, 60],
    'Azteca Sinaloa (Video)': [58, 63, 61, 62, 63],

    'Azteca CJ (Note)': [63, 62, 61, 65, 62],
    'Azteca CJ (Video)': [74, 72, 71, 72, 64],

    'Azteca Aguascalientes (Note)': [64, 64, 61, 61, 61],
    'Azteca Aguascalientes (Video)': [61, 63, 65, 66, 66],

    'Azteca Queretaro (Note)': [66, 55, 67, 61, 62],
    'Azteca Queretaro (Video)': [61, 66, 66, 63, 67],

    'Azteca Chiapas (Note)': [55, 57, 63, 65, 64],
    'Azteca Chiapas (Video)': [64, 65, 65, 66, 61],

    'Azteca Puebla (Note)': [65, 67, 63, 61, 61],
    'Azteca Puebla (Video)': [66, 67, 65, 64, 64],

    'Azteca Yucatan (Note)': [59, 59, 60, 64, 63],
    'Azteca Yucatan (Video)': [68, 63, 64, 66, 67],

    'Azteca Chihuahua (Note)': [53, 52, 59, 59, 60],
    'Azteca Chihuahua (Video)': [56, 61, 61, 60, 61],

    'Azteca Morelos (Note)': [52, 52, 58, 58, 65],
    'Azteca Morelos (Video)': [62, 62, 63, 60, 65],

    'Azteca Jalisco (Note)': [58, 59, 58, 59, 61],
    'Azteca Jalisco (Video)': [64, 60, 58, 60, 63],

    'Azteca Guerrero (Note)': [62, 60, 60, 59, 60],
    'Azteca Guerrero (Video)': [61, 61, 61, 61, 62],

    'Azteca Bajio (Note)': [60, 60, 63, 61, 61],
    'Azteca Bajio (Video)': [62, 58, 61, 63, 64]
}


names = [
    "Azteca Veracruz (Note)",
    "Azteca Veracruz (Video)",
    "Azteca Quintanaroo (Note)",
    "Azteca Quintanaroo (Video)",
    "Azteca BC (Note)",
    "Azteca BC (Video)",
    "Azteca Sinaloa (Note)",
    "Azteca Sinaloa (Video)",
    "Azteca CJ (Note)",
    "Azteca CJ (Video)",
    "Azteca Aguascalientes (Note)",
    "Azteca Aguascalientes (Video)",
    "Azteca Queretaro (Note)",
    "Azteca Queretaro (Video)",
    "Azteca Chiapas (Note)",
    "Azteca Chiapas (Video)",
    "Azteca Puebla (Note)",
    "Azteca Puebla (Video)",
    "Azteca Yucatan (Note)",
    "Azteca Yucatan (Video)",
    "Azteca Chihuahua (Note)",
    "Azteca Chihuahua (Video)",
    "Azteca Morelos (Note)",
    "Azteca Morelos (Video)",
    "Azteca Jalisco (Note)",
    "Azteca Jalisco (Video)",
    "Azteca Guerrero (Note)",
    "Azteca Guerrero (Video)",
    "Azteca Bajio (Note)",
    "Azteca Bajio (Video)"
]  # Define names that indicate azteca is true

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

        record = {
            "name": name.split("(")[0].strip(),
            "note_value": float(note_value),
            "video_value": float(video_value),
            "total_value": float(total_value),
            "azteca": True if name.startswith("Azteca") else False,
            "date": date
        }

        LocalRecord.objects.create(**record)
