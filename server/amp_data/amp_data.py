import pandas as pd
from collections import defaultdict
from server.models import AmpRecord
from datetime import datetime
import json
from django.utils import timezone
from server.constants import AmpSites 
from typing import Optional
from server.utils import safe_division, validate_dataframe_input
from itertools import chain
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for detailed logs
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define global variables
is_calc = False

# Updated columns to include AMP
columns = [
    'AMP Avg', 
    'AMP Note Avg',
    'AMP Video Avg',
    'Date'
]

# Updated changeKeys to include AMP changes
changeKeys = [
    'AMP Avg Change',
    'AMP Note Change',
    'AMP Video Change',
]

amp_columns = [
    'Azteca UNO (Note)', 'Azteca UNO (Video)', 'Azteca 7 (Note)', 'Azteca 7 (Video)', 
    'Deportes (Note)', 'Deportes (Video)', 'ADN40 (Note)', 'ADN40 (Video)', 
    'Noticias (Note)', 'Noticias (Video)', 
    'Azteca Veracruz (Note)', 'Azteca Veracruz (Video)', 'Azteca Quintanaroo (Note)', 'Azteca Quintanaroo (Video)',
    'Azteca Sinaloa (Note)', 'Azteca Sinaloa (Video)', 'Azteca BC (Note)', 'Azteca BC (Video)',
    'Azteca CJ (Note)', 'Azteca CJ (Video)', 'Azteca Aguascalientes (Note)', 'Azteca Aguascalientes (Video)',
    'Azteca Queretaro (Note)', 'Azteca Queretaro (Video)', 'Azteca Chiapas (Note)', 'Azteca Chiapas (Video)',
    'Azteca Puebla (Note)', 'Azteca Puebla (Video)', 'Azteca Yucatan (Note)', 'Azteca Yucatan (Video)',
    'Azteca Chihuahua (Note)', 'Azteca Chihuahua (Video)', 'Azteca Morelos (Note)', 'Azteca Morelos (Video)',
    'Azteca Jalisco (Note)', 'Azteca Jalisco (Video)', 'Azteca Guerrero (Note)', 'Azteca Guerrero (Video)',
    'Azteca Bajio (Note)', 'Azteca Bajio (Video)', 'Laguna (Note)', 'Laguna (Video)',
]

amp_columns_raw = [
    'Azteca UNO', 'Azteca 7',
    'Deportes', 'ADN40',
    'Noticias',
    'Azteca Veracruz', 'Azteca Quintanaroo',
    'Azteca Sinaloa', 'Azteca BC',
    'Azteca CJ', 'Azteca Aguascalientes',
    'Azteca Queretaro', 'Azteca Chiapas',
    'Azteca Puebla', 'Azteca Yucatan',
    'Azteca Chihuahua', 'Azteca Morelos',
    'Azteca Jalisco', 'Azteca Guerrero',
    'Azteca Bajio', 'Laguna'
]

# Label mapping remains unchanged
label_mapping = {
    'Azteca UNO (Note)': 'UNO',
    'Azteca UNO (Video)': 'UNO',
    'Azteca 7 (Note)': '7',
    'Azteca 7 (Video)': '7',
    'Deportes (Note)': 'Deportes',
    'Deportes (Video)': 'Deportes',
    'ADN40 (Note)': 'ADN40',
    'ADN40 (Video)': 'ADN40',
    'Noticias (Note)': 'Noticias',
    'Noticias (Video)': 'Noticias',
    'Azteca Veracruz (Note)': 'Veracruz',
    'Azteca Veracruz (Video)': 'Veracruz',
    'Azteca Quintanaroo (Note)': 'Quintanaroo',
    'Azteca Quintanaroo (Video)': 'Quintanaroo',
    'Azteca Sinaloa (Note)': 'Sinaloa',
    'Azteca Sinaloa (Video)': 'Sinaloa',
    "Azteca BC (Note)": "BC",
    "Azteca BC (Video)": "BC",
    "Azteca CJ (Note)": "CJ",
    "Azteca CJ (Video)": "CJ",
    "Azteca Aguascalientes (Note)": "Aguascalientes",
    "Azteca Aguascalientes (Video)": "Aguascalientes",
    "Azteca Queretaro (Note)": "Queretaro",
    "Azteca Queretaro (Video)": "Queretaro",
    "Azteca Chiapas (Note)": "Chiapas",
    "Azteca Chiapas (Video)": "Chiapas",
    "Azteca Puebla (Note)": "Puebla",
    "Azteca Puebla (Video)": "Puebla",
    "Azteca Yucatan (Note)": "Yucatan",
    "Azteca Yucatan (Video)": "Yucatan",
    "Azteca Chihuahua (Note)": "Chihuahua",
    "Azteca Chihuahua (Video)": "Chihuahua",
    "Azteca Morelos (Note)": "Morelos",
    "Azteca Morelos (Video)": "Morelos",
    "Azteca Jalisco (Note)": "Jalisco",
    "Azteca Jalisco (Video)": "Jalisco",
    "Azteca Guerrero (Note)": "Guerrero",
    "Azteca Guerrero (Video)": "Guerrero",
    "Azteca Bajio (Note)": "Bajio",
    "Azteca Bajio (Video)": "Bajio",
    "Laguna (Note)": "Laguna",
    "Laguna (Video)": "Laguna"
}

def fetch_records():
    # Dictionary to store grouped and structured data
    data = defaultdict(list)

    all_records = AmpRecord.objects.all().order_by("date")

    # Group records by date
    grouped_records = defaultdict(list)
    for record in all_records:
        grouped_records[record.date].append(record)

    # Get all unique names (e.g., "Azteca UNO") to ensure consistent keys
    all_names = set(record.name for record in all_records)

    # Iterate over the grouped records and populate the dictionary
    for date, records_on_date in grouped_records.items():
        # Convert date to string format 'YYYY-MM-DD'
        data["Date"].append(str(date))

        # Create a temporary dictionary for the current date
        temp_data = {f"{name} (Note)": 0 for name in all_names}
        temp_data.update({f"{name} (Video)": 0 for name in all_names})

        # Update temporary data with the actual values from records
        for record in records_on_date:
            temp_data[f"{record.name} (Note)"] += int(record.note_value or 0)
            temp_data[f"{record.name} (Video)"] += int(record.video_value or 0)

        # Append the values from temp_data to the main data dictionary
        for key in temp_data:
            data[key].append(temp_data[key])

    # Ensure all keys have values for all dates
    for key in data.keys():
        if key != "Date":  # Skip the "Date" key
            while len(data[key]) < len(data["Date"]):
                data[key].append(0)

    # Convert defaultdict to a normal dictionary for output
    return dict(data)

def init(inner_data=None):
    if inner_data is None:
        inner_data = fetch_records()
    # print('This is Amp Inner data',inner_data)
    df = pd.DataFrame(inner_data)
    
    # Calculate averages excluding zeros
    df['AMP Avg'] = df[amp_columns][df[amp_columns] != 0].mean(axis=1).round(1)

    df['AMP Note Avg'] = df[[col for col in amp_columns if 'Note' in col]][
        df[[col for col in amp_columns if 'Note' in col]] != 0].mean(axis=1).round(1)

    df['AMP Video Avg'] = df[[col for col in amp_columns if 'Video' in col]][
        df[[col for col in amp_columns if 'Video' in col]] != 0].mean(axis=1).round(1)

    def pct_change(series):
        return series.pct_change().apply(lambda x: x)

    df['AMP Avg Change'] = pct_change(df['AMP Avg'])
    df['AMP Note Change'] = pct_change(df['AMP Note Avg'])
    df['AMP Video Change'] = pct_change(df['AMP Video Avg'])
    
    return df

def formatToJson(df):
    json_str = df.to_json(orient='records')
    return json.loads(json_str)

def transform_data(data, include_columns=[], start_date=None, end_date=None):
    # Convert start_date and end_date to datetime.date objects for comparison
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Initialize the series dictionary
    series = {}

    # Process each item in the data
    for entry in data:
        date = datetime.strptime(entry["Date"], "%Y-%m-%d").date()

        # Filter based on the date range if provided
        if (start_date and date < start_date) or (end_date and date > end_date):
            continue

        for key, value in entry.items():
            if key != "Date" and (key in include_columns or len(include_columns) == 0):
                if key not in series:
                    series[key] = []
                series[key].append({"x": date.strftime("%Y-%m-%d"), "y": value})

    # Convert series to a list of dictionaries
    result = [{"name": key, "data": value} for key, value in series.items()]

    return result

def calculate_relevant_insights(filtered_df, companies, title, date_filter=None):
    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to a datetime object representing the start and end of the month.
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format if it's not already
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%Y-%m-%d')

        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    significant_changes = []

    # Check if the filtered DataFrame is not empty before proceeding
    if not filtered_df.empty:
        for company in companies:
            initial_value = filtered_df[company].iloc[0]
            final_value = filtered_df[company].iloc[-1]
            if initial_value == 0:
                percentage_change = 0
            else:
                percentage_change = ((final_value - initial_value) / initial_value) * 100

            if abs(percentage_change) >= 5:
                if abs(percentage_change) < 10:
                    change_description = "mildly"
                elif abs(percentage_change) < 20:
                    change_description = "moderately"
                else:
                    change_description = "significantly"

                change_type = "decreased" if percentage_change < 0 else "increased"
                significant_changes.append(
                    (company, change_type, change_description, percentage_change))

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"{title} {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = f"No significant changes were observed across the {title} companies."

    return insight

def calculate_weekly_averages(df):
    months = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')

    # Group the data by year and month
    grouped = df.groupby(['Date'])

    for (date, ), month_df in grouped:
        amp_avg = round(month_df[amp_columns][month_df[amp_columns] != 0].mean(axis=1).mean(), 1)

        amp_avg_video = round(month_df[[col for col in amp_columns if 'Video' in col]][
            month_df[[col for col in amp_columns if 'Video' in col]] != 0].mean(axis=1).mean(), 1)

        amp_avg_note = round(month_df[[col for col in amp_columns if 'Note' in col]][
            month_df[[col for col in amp_columns if 'Note' in col]] != 0].mean(axis=1).mean(), 1)

        amp_map = {}

        if months:
            prev_month = months[-1]
            prev_amp_avg = prev_month['AMP Avg']

            prev_amp_avg_video = prev_month['AMP Video Avg']

            prev_amp_avg_note = prev_month['AMP Note Avg']

            amp_change = safe_division(amp_avg , prev_amp_avg)

            amp_change_video = safe_division(amp_avg_video , prev_amp_avg_video)

            amp_change_note = safe_division(amp_avg_note , prev_amp_avg_note)
        else:
            amp_change = 100
            amp_change_video = 100
            amp_change_note = 100

        res = {
            'Date': f"{date.date()}",
            'AMP Change': amp_change,
            'AMP Video Change': amp_change_video,
            'AMP Note Change': amp_change_note,
            'AMP Avg': amp_avg,
            'AMP Video Avg': amp_avg_video,
            'AMP Note Avg': amp_avg_note,
            "amp": [] 
        }
        
        for (index, company) in enumerate(amp_columns_raw):
            company_avg = round(month_df[[col for col in amp_columns if company in col]][month_df[[col for col in amp_columns if company in col]] != 0].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in amp_columns if 'Video' in col and company in col]][month_df[[col for col in amp_columns if 'Video' in col and company in col]] != 0].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in amp_columns if 'Note' in col and company in col]][month_df[[col for col in amp_columns if 'Note' in col and company in col]] != 0].mean(axis=1).mean(), 1)
        # Process AMP data
            if len(months) > 0:
                prev_month = months[-1]
                prev_amp_avg = prev_month['AMP Avg']
                prev_amp_video_avg = prev_month['AMP Video Avg']
                prev_amp_note_avg = prev_month['AMP Note Avg']

                amp_change = safe_division(company_avg, prev_amp_avg)
                amp_video_change = safe_division(company_avg_video, prev_amp_video_avg)
                amp_note_change = safe_division(company_avg_note, prev_amp_note_avg)
            else:
                amp_change = 100
                amp_video_change = 100
                amp_note_change = 100

            res["amp"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(amp_change) else (amp_change or 0),
                "video_change": 0 if pd.isna(amp_video_change) else (amp_video_change or 0),
                "note_change": 0 if pd.isna(amp_note_change) else (amp_note_change or 0)
            })

        months.append(res)

    return pd.DataFrame(months)

def calculate_quarterly_averages(df):
    months = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')

    # Group the data by year and month
    grouped = df.groupby(['Year', 'Month'])

    for (year, month), month_df in grouped:
        amp_avg = month_df[amp_columns].mean(axis=1).mean().round(1)

        amp_avg_video = month_df[[col for col in amp_columns if 'Video' in col]].mean(axis=1).mean().round(1)

        amp_avg_note = month_df[[col for col in amp_columns if 'Note' in col]].mean(axis=1).mean().round(1)

        amp_map = {}

        if months:
            prev_month = months[-1]
            prev_amp_avg = prev_month['AMP Avg']

            prev_amp_avg_video = prev_month['AMP Video Avg']

            prev_amp_avg_note = prev_month['AMP Note Avg']

            amp_change = safe_division(amp_avg , prev_amp_avg)

            amp_change_video = safe_division(amp_avg_video , prev_amp_avg_video)

            amp_change_note = safe_division(amp_avg_note , prev_amp_avg_note)
        else:
            amp_change = 100
            amp_change_video = 100
            amp_change_note = 100

        res = {
            'Date': f"Q{int(month.strftime('%m'))}-{year}",
            'AMP Change': amp_change,
            'AMP Video Change': amp_change_video,
            'AMP Note Change': amp_change_note,
            'AMP Avg': amp_avg,
            'AMP Video Avg': amp_avg_video,
            'AMP Note Avg': amp_avg_note,
            "amp": [] 
        }
        
        for (index, company) in enumerate(amp_columns_raw):
            company_avg = round(month_df[[col for col in amp_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in amp_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in amp_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)
        # Process AMP data
            if len(months) > 0:
                prev_month = months[-1]
                prev_amp_avg = prev_month['AMP Avg']
                prev_amp_video_avg = prev_month['AMP Video Avg']
                prev_amp_note_avg = prev_month['AMP Note Avg']

                amp_change = safe_division(company_avg, prev_amp_avg)
                amp_video_change = safe_division(company_avg_video, prev_amp_video_avg)
                amp_note_change = safe_division(company_avg_note, prev_amp_note_avg)
            else:
                amp_change = 100
                amp_video_change = 100
                amp_note_change = 100

            res["amp"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(amp_change) else (amp_change or 0),
                "video_change": 0 if pd.isna(amp_video_change) else (amp_video_change or 0),
                "note_change": 0 if pd.isna(amp_note_change) else (amp_note_change or 0)
            })

        months.append(res)

    return pd.DataFrame(months)

def calculate_yearly_averages(df):
    months = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')

    # Group the data by year and month
    grouped = df.groupby(['Year'])

    for (year,), month_df in grouped:
        amp_avg = month_df[amp_columns].mean(axis=1).mean().round(1)

        amp_avg_video = month_df[[col for col in amp_columns if 'Video' in col]].mean(axis=1).mean().round(1)

        amp_avg_note = month_df[[col for col in amp_columns if 'Note' in col]].mean(axis=1).mean().round(1)

        amp_map = {}

        if months:
            prev_month = months[-1]
            prev_amp_avg = prev_month['AMP Avg']

            prev_amp_avg_video = prev_month['AMP Video Avg']

            prev_amp_avg_note = prev_month['AMP Note Avg']

            amp_change = safe_division(amp_avg , prev_amp_avg)

            amp_change_video = safe_division(amp_avg_video , prev_amp_avg_video)

            amp_change_note = safe_division(amp_avg_note , prev_amp_avg_note)
        else:
            amp_change = 100
            amp_change_video = 100
            amp_change_note = 100

        res = {
            'Date': f"Q{int(1)}-{year}",
            'AMP Change': amp_change,
            'AMP Video Change': amp_change_video,
            'AMP Note Change': amp_change_note,
            'AMP Avg': amp_avg,
            'AMP Video Avg': amp_avg_video,
            'AMP Note Avg': amp_avg_note,
            "amp": [] 
        }
        
        for (index, company) in enumerate(amp_columns_raw):
            company_avg = round(month_df[[col for col in amp_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in amp_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in amp_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)
        # Process AMP data
            if len(months) > 0:
                prev_month = months[-1]
                prev_amp_avg = prev_month['AMP Avg']
                prev_amp_video_avg = prev_month['AMP Video Avg']
                prev_amp_note_avg = prev_month['AMP Note Avg']

                amp_change = safe_division(company_avg, prev_amp_avg)
                amp_video_change = safe_division(company_avg_video, prev_amp_video_avg)
                amp_note_change = safe_division(company_avg_note, prev_amp_note_avg)
            else:
                amp_change = 100
                amp_video_change = 100
                amp_note_change = 100

            res["amp"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(amp_change) else (amp_change or 0),
                "video_change": 0 if pd.isna(amp_video_change) else (amp_video_change or 0),
                "note_change": 0 if pd.isna(amp_note_change) else (amp_note_change or 0)
            })

        months.append(res)

    return pd.DataFrame(months)

def calculate_all_time_averages(df):
    date = timezone.now()

    amp_avg = df[amp_columns].mean(axis=1).mean().round(1)

    amp_avg_video = df[[col for col in amp_columns if 'Video' in col]].mean(axis=1).mean().round(1)

    amp_avg_note = df[[col for col in amp_columns if 'Note' in col]].mean(axis=1).mean().round(1)

    res = {
        'Date': f"{date.date()}",
        'AMP Change': 100,
        'AMP Video Change': 100,
        'AMP Note Change': 100,
        'AMP Avg': amp_avg,
        'AMP Video Avg': amp_avg_video,
        'AMP Note Avg': amp_avg_note,
        "amp": [] 
    }
        
    for (index, company) in enumerate(amp_columns_raw):
        company_avg = round(df[[col for col in amp_columns if company in col]].mean(axis=1).mean(), 1)
        company_avg_video = round(df[[col for col in amp_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
        company_avg_note = round(df[[col for col in amp_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)
    
        res["amp"].append({
            "name": company,
            "total": company_avg,
            "video": company_avg_video,
            "note": company_avg_note,
            "total_change": 100,
            "video_change": 100,
            "note_change": 100
        })


    return res

def calculate_changes(df):
    # Make a copy of the input DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Convert 'Date' to datetime and sort by 'Date'
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy = df_copy.sort_values(by='Date')

    # Get the latest and second-to-last dates
    latest_date = df_copy['Date'].max()
    second_last_date = df_copy[df_copy['Date'] < latest_date]['Date'].max()

    # Filter the data for the latest and second-to-last quarters
    latest_df = df_copy[df_copy['Date'] == latest_date]
    second_last_df = df_copy[df_copy['Date'] == second_last_date]

    # Compute averages for the latest date
    amp_avg_latest = latest_df[amp_columns].mean(axis=1).mean().round(1)

    amp_avg_video_latest = latest_df[[col for col in amp_columns if 'Video' in col]].mean(axis=1).mean().round(1)
    
    amp_avg_note_latest = latest_df[[col for col in amp_columns if 'Note' in col]].mean(axis=1).mean().round(1)
    
    amp_avg_second_last = second_last_df[amp_columns].mean(axis=1).mean().round(1)

    amp_avg_video_second_last = second_last_df[[col for col in amp_columns if 'Video' in col]].mean(axis=1).mean().round(1)

    amp_avg_note_second_last = second_last_df[[col for col in amp_columns if 'Note' in col]].mean(axis=1).mean().round(1)

    # Calculate the changes
    amp_change = safe_division(amp_avg_latest , amp_avg_second_last)

    amp_change_video = safe_division(amp_avg_video_latest , amp_avg_video_second_last)

    amp_change_note = safe_division(amp_avg_note_latest, amp_avg_note_second_last)

    # Prepare the result dictionary
    res = {
        'Date': latest_date.strftime('%Y-%m-%d'),
        'AMP Change': amp_change,
        
        'AMP Video Change': amp_change_video,
        
        'AMP Note Change': amp_change_note,
        
        'AMP Avg': amp_avg_latest,
        
        'AMP Video Avg': amp_avg_video_latest,
        
        'AMP Note Avg': amp_avg_note_latest,
        "amp": []  # Added AMP section
    }
    for (index, company) in enumerate(amp_columns_raw):
        company_avg_latest = round(latest_df[
            [col for col in amp_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_latest = round(latest_df[
            [col for col in amp_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_latest = round(latest_df[
            [col for col in amp_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_second_last = round(second_last_df[
            [col for col in amp_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_second_last = round(second_last_df[
            [col for col in amp_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_second_last = round(second_last_df[
            [col for col in amp_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)

        # Add AMP-level data comparison
        amp_change = safe_division(company_avg_latest, company_avg_second_last)
        amp_video_change = safe_division(company_avg_video_latest, company_avg_video_second_last)
        amp_note_change = safe_division(company_avg_note_latest, company_avg_note_second_last)

        res["amp"].append({
            "name": company,
            "total": company_avg_latest,
            "video": company_avg_video_latest,
            "note": company_avg_note_latest,
            "total_change": 0 if pd.isna(amp_change) else (amp_change or 0),
            "video_change": 0 if pd.isna(amp_video_change) else (amp_video_change or 0),
            "note_change": 0 if pd.isna(amp_note_change) else (amp_note_change or 0)
        })

    return res

def calculate_competition_insights(filtered_df, companies, is_competition, date_filter=None):
    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to a datetime object representing the start and end of the month.
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format if it's not already
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%Y-%m-%d')

        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    significant_changes = []
    for company in companies:
        try:
            initial_value = filtered_df[company].iloc[0]
            final_value = filtered_df[company].iloc[-1]

            if initial_value == 0:
                percentage_change = 0
            else:
                percentage_change = ((final_value - initial_value) / initial_value) * 100

            if abs(percentage_change) >= 5:
                if abs(percentage_change) < 10:
                    change_description = "mildly"
                elif abs(percentage_change) < 20:
                    change_description = "moderately"
                else:
                    change_description = "significantly"

                change_type = "decreased" if percentage_change < 0 else "increased"
                significant_changes.append(
                    (company, change_type, change_description, percentage_change))
        except Exception as e:
            logger.exception(f"Exception processing company {company}: {e}")
            continue

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"Competition {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = None

    return insight

def calculate_relevant_insights(filtered_df, companies, title, date_filter=None):
    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to a datetime object representing the start and end of the month.
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format if it's not already
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%Y-%m-%d')

        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    significant_changes = []

    # Check if the filtered DataFrame is not empty before proceeding
    if not filtered_df.empty:
        for company in companies:
            initial_value = filtered_df[company].iloc[0]
            final_value = filtered_df[company].iloc[-1]
            if initial_value == 0:
                percentage_change = 0
            else:
                percentage_change = ((final_value - initial_value) / initial_value) * 100

            if abs(percentage_change) >= 5:
                if abs(percentage_change) < 10:
                    change_description = "mildly"
                elif abs(percentage_change) < 20:
                    change_description = "moderately"
                else:
                    change_description = "significantly"

                change_type = "decreased" if percentage_change < 0 else "increased"
                significant_changes.append(
                    (company, change_type, change_description, percentage_change))

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"{title} {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = f"No significant changes were observed across the {title} companies."

    return insight

def formatLolData(df, inner_data):
    data_as_json = formatToJson(df)
    note = []
    video = []
    
    video_self = calculate_relevant_insights(
        df, [col for col in list(label_mapping.keys()) if 'Video' in col], '')
    note_self = calculate_relevant_insights(
        df, [col for col in list(label_mapping.keys()) if 'Note' in col], '')
    total_self = calculate_relevant_insights(
        df, list(label_mapping.keys()), '')

    # Dictionaries to store the combined data and totals
    for index, item in enumerate(data_as_json):
        item["Date"] = inner_data["Date"][index]
    transformed_data = transform_data(data_as_json)

    for item in transformed_data:
        if "Video" in item["name"]:
            if item['name'] in label_mapping:
                item['name'] = label_mapping[item["name"]]
            else:
                item['name'] = item['name'].replace(" (Video)", "")
            video.append(item)
        elif "Note" in item["name"]:
            if item['name'] in label_mapping:
                item['name'] = label_mapping[item["name"]]
            else:
                item['name'] = item['name'].replace(" (Note)", "")
            note.append(item)
        else:
            # Handle AMP or other non-Note/Video data if necessary
            if item['name'] in label_mapping:
                item['name'] = label_mapping[item["name"]]
            combined_name = item['name']
            video.append(item)
            note.append(item)

    combined_data = {}
    # Combine video and note data
    for item in video + note:
        name = item['name']
        for entry in item['data']:
            date = entry['x']
            value = entry['y']

            # Initialize combined_data entry if it doesn't exist
            if name not in combined_data:
                combined_data[name] = {}
            if date not in combined_data[name]:
                combined_data[name][date] = {'sum': 0, 'count': 0}

            # Add value to sum and increment count
            combined_data[name][date]['sum'] += 0 if value is None else value
            combined_data[name][date]['count'] += 1

    # Format the averages output
    totals = []
    for name, dates in combined_data.items():
        # Calculate averages for each date
        data = [{'x': date, 'y': values['sum'] / values['count']}
                for date, values in sorted(dates.items())]
        totals.append({'name': name, 'data': data})
    return {
        "videos": video,
        "notes": note,
        "total": totals,
        "insights": {
            "videos": {
                "self": video_self,
            },
            "notes": {
                "self": note_self,
            },
            "total": {
                "self": total_self,
            }
        }
    }

def get_data():
    inner_data = fetch_records()
    df = init(inner_data)
    data = formatToJson(df)
    average_data = transform_data(data, columns)
    percentages = transform_data(data, changeKeys)
    other = formatLolData(df, inner_data)

    return {
        "weekly": {
            "data": average_data,
            "changes": percentages,
        },
        "comparison": other
    }

def get_averages():
    df = init()
    quarter_data = formatToJson(
        calculate_quarterly_averages(df))
    week_data = formatToJson(
        calculate_weekly_averages(df))
    year_data = formatToJson(
        calculate_yearly_averages(df))
    all_time_data = (
        calculate_all_time_averages(df))

    return {
        "quarter": quarter_data,
        "week": week_data,
        "year": year_data,
        "all_time": all_time_data,
    }

def get_insights(date_filter=None):
    df = init()
    video_self = calculate_relevant_insights(
        df, [col for col in amp_columns if 'Video' in col], '', date_filter)
    note_self = calculate_relevant_insights(
        df, [col for col in amp_columns if 'Note' in col], '', date_filter)
    total_self = calculate_relevant_insights(
        df, amp_columns, '', date_filter)
    

    return {
        "videos": {
            "self": video_self,
        },
        "notes": {
            "self": note_self,
        },
        "total": {
            "self": total_self,
        },
    }
