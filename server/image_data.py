from django.http import JsonResponse
from django.utils import timezone
import pandas as pd
from collections import defaultdict

from .models import ImageRecord
from server.utils import safe_division

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
    
    # Calculate averages excluding 0 values
    df['Image Pages Avg'] = df[metric_columns].replace(0, pd.NA).mean(axis=1).round(1)
    df['Note Avg'] = df[[col for col in metric_columns if 'Note' in col]].replace(0, pd.NA).mean(axis=1).round(1)
    df['Video Avg'] = df[[col for col in metric_columns if 'Video' in col]].replace(0, pd.NA).mean(axis=1).round(1)
    
    # Calculate changes
    df['Image Pages Change'] = df['Image Pages Avg'].pct_change() 
    df['Note Change'] = df['Note Avg'].pct_change() 
    df['Video Change'] = df['Video Avg'].pct_change() 
    
    return df

def calculate_weekly_averages(df):
    months = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')

    # Group the data by date
    grouped = df.groupby(['Date'])

    for (date,), month_df in grouped:
        metric_columns = [col for col in month_df.columns if col not in ['Date', 'Year', 'Month']]
        
        # Calculate averages
        image_avg = month_df[metric_columns].replace(0, pd.NA).mean(axis=1).mean().round(1)
        note_avg = month_df[[col for col in metric_columns if 'Note' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        video_avg = month_df[[col for col in metric_columns if 'Video' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        
        # Calculate changes
        if months:
            prev_month = months[-1]
            image_change = safe_division(image_avg, prev_month['Image Pages Avg'])
            note_change = safe_division(note_avg, prev_month['Note Avg'])
            video_change = safe_division(video_avg, prev_month['Video Avg'])
        else:
            image_change = 100
            note_change = 100
            video_change = 100
            
        res = {
            'Date': f"{date.date()}",
            'Image Pages Change': image_change,
            'Note Change': note_change,
            'Video Change': video_change,
            'Image Pages Avg': image_avg,
            'Note Avg': note_avg,
            'Video Avg': video_avg,
        }
        
        months.append(res)
        
    return pd.DataFrame(months)

def calculate_quarterly_averages(df):
    quarters = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter

    # Group the data by year and quarter
    grouped = df.groupby(['Year', 'Quarter'])

    for (year, quarter), quarter_df in grouped:
        metric_columns = [col for col in quarter_df.columns if col not in ['Date', 'Year', 'Quarter']]
        
        # Calculate averages
        image_avg = quarter_df[metric_columns].replace(0, pd.NA).mean(axis=1).mean().round(1)
        note_avg = quarter_df[[col for col in metric_columns if 'Note' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        video_avg = quarter_df[[col for col in metric_columns if 'Video' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        
        # Calculate changes
        if quarters:
            prev_quarter = quarters[-1]
            image_change = safe_division(image_avg, prev_quarter['Image Pages Avg'])
            note_change = safe_division(note_avg, prev_quarter['Note Avg'])
            video_change = safe_division(video_avg, prev_quarter['Video Avg'])
        else:
            image_change = 100
            note_change = 100
            video_change = 100
            
        res = {
            'Date': f"Q{quarter}-{year}",
            'Image Pages Change': image_change,
            'Note Change': note_change,
            'Video Change': video_change,
            'Image Pages Avg': image_avg,
            'Note Avg': note_avg,
            'Video Avg': video_avg,
        }
        
        quarters.append(res)
        
    return pd.DataFrame(quarters)

def calculate_yearly_averages(df):
    years = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year

    # Group the data by year
    grouped = df.groupby(['Year'])

    for (year,), year_df in grouped:
        metric_columns = [col for col in year_df.columns if col not in ['Date', 'Year']]
        
        # Calculate averages
        image_avg = year_df[metric_columns].replace(0, pd.NA).mean(axis=1).mean().round(1)
        note_avg = year_df[[col for col in metric_columns if 'Note' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        video_avg = year_df[[col for col in metric_columns if 'Video' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
        
        # Calculate changes
        if years:
            prev_year = years[-1]
            image_change = safe_division(image_avg, prev_year['Image Pages Avg'])
            note_change = safe_division(note_avg, prev_year['Note Avg'])
            video_change = safe_division(video_avg, prev_year['Video Avg'])
        else:
            image_change = 100
            note_change = 100
            video_change = 100
            
        res = {
            'Date': f"Q1-{year}",  # Using Q1 format to match existing pattern
            'Image Pages Change': image_change,
            'Note Change': note_change,
            'Video Change': video_change,
            'Image Pages Avg': image_avg,
            'Note Avg': note_avg,
            'Video Avg': video_avg,
        }
        
        years.append(res)
        
    return pd.DataFrame(years)

def calculate_all_time_averages(df):
    metric_columns = [col for col in df.columns if col not in ['Date', 'Year', 'Month', 'Quarter']]
    
    # Calculate all-time averages
    image_avg = df[metric_columns].replace(0, pd.NA).mean(axis=1).mean().round(1)
    note_avg = df[[col for col in metric_columns if 'Note' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
    video_avg = df[[col for col in metric_columns if 'Video' in col]].replace(0, pd.NA).mean(axis=1).mean().round(1)
    
    return {
        'Date': timezone.now().date().isoformat(),
        'Image Pages Change': 100,
        'Note Change': 100,
        'Video Change': 100,
        'Image Pages Avg': image_avg,
        'Note Avg': note_avg,
        'Video Avg': video_avg,
    }

def get_image_data():
    inner_data = fetch_image_records()
    df = init_image_data(inner_data)
    
    # Fill NaN values with 0 for the weekly data
    df['Image Pages Change'] = df['Image Pages Change'].fillna(0)
    df['Note Change'] = df['Note Change'].fillna(0)
    df['Video Change'] = df['Video Change'].fillna(0)
    
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

def get_image_averages():
    df = init_image_data()
    quarter_data = calculate_quarterly_averages(df).to_dict('records')
    week_data = calculate_weekly_averages(df).to_dict('records')
    
    
    return {
        "quarter": quarter_data,
        "week": week_data,
    } 