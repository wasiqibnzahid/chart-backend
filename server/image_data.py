from django.http import JsonResponse
from django.utils import timezone
import pandas as pd
from collections import defaultdict

from .models import ImageRecord

def fetch_image_records():
    data = defaultdict(list)
    records = ImageRecord.objects.all().order_by('date')
    
    # Group records by date
    grouped_records = defaultdict(list)
    for record in records:
        grouped_records[record.date].append(record)
        
    # Process grouped records
    for date, records_on_date in grouped_records.items():
        data['Date'].append(str(date))
        for record in records_on_date:
            # For image records, we use the same metrics for both note and video
            data[f"{record.name} (Note)"].append(int(record.note_value or 0))
            data[f"{record.name} (Video)"].append(int(record.video_value or 0))
            
    return dict(data)

def init_image_data(inner_data=None):
    if inner_data is None:
        inner_data = fetch_image_records()
    df = pd.DataFrame(inner_data)
    
    # Get all column names except 'Date'
    metric_columns = [col for col in df.columns if col != 'Date']
    
    # Calculate averages
    df['Image Pages Avg'] = df[metric_columns].mean(axis=1).round(1)
    df['Note Avg'] = df[[col for col in metric_columns if 'Note' in col]].mean(axis=1).round(1)
    df['Video Avg'] = df[[col for col in metric_columns if 'Video' in col]].mean(axis=1).round(1)
    
    # Calculate changes
    df['Image Pages Change'] = df['Image Pages Avg'].pct_change()
    df['Note Change'] = df['Note Avg'].pct_change()
    df['Video Change'] = df['Video Avg'].pct_change()
    
    return df

def get_image_data():
    inner_data = fetch_image_records()
    df = init_image_data(inner_data)
    
    # Convert DataFrame to JSON format
    data = df.to_dict('records')
    
    # Prepare the response structure
    response = {
        "weekly": {
            "data": [
                {"name": "Image Pages Avg", "data": [{"x": row["Date"], "y": row["Image Pages Avg"]} for row in data]},
                {"name": "Note Avg", "data": [{"x": row["Date"], "y": row["Note Avg"]} for row in data]},
                {"name": "Video Avg", "data": [{"x": row["Date"], "y": row["Video Avg"]} for row in data]},
            ],
            "changes": [
                {"name": "Image Pages Change", "data": [{"x": row["Date"], "y": row["Image Pages Change"]} for row in data]},
                {"name": "Note Change", "data": [{"x": row["Date"], "y": row["Note Change"]} for row in data]},
                {"name": "Video Change", "data": [{"x": row["Date"], "y": row["Video Change"]} for row in data]},
            ],
        }
    }
    
    return response 