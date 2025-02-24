from django.http import JsonResponse
from django.views import View
from django.db.models import Q
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
    df['Image Pages Avg'] = df[metric_columns].replace(
        0, pd.NA).mean(axis=1).round(1)
    df['Note Avg'] = df[[col for col in metric_columns if 'Note' in col]
                        ].replace(0, pd.NA).mean(axis=1).round(1)
    df['Video Avg'] = df[[col for col in metric_columns if 'Video' in col]
                         ].replace(0, pd.NA).mean(axis=1).round(1)

    # Calculate changes
    df['Image Pages Change'] = df['Image Pages Avg'].pct_change()
    df['Note Change'] = df['Note Avg'].pct_change()
    df['Video Change'] = df['Video Avg'].pct_change()

    return df


def non_zero_avg(series):
    """Compute average ignoring zeros"""
    non_zero_values = series[series != 0]  # Exclude zeros
    non_zero_values = pd.Series(non_zero_values)  # Ensure it's a Pandas Series
    return non_zero_values.mean() if not non_zero_values.empty else 0.0



def safe_division(numerator, denominator):
    """Safe division function to prevent division by zero"""
    return (numerator / denominator - 1) if denominator else 0.0


def calculate_weekly_averages(df: pd.DataFrame):
    months = []
    df['Date'] = pd.to_datetime(df['Date'])

    # Identify Note and Video columns
    cols = [col for col in df.columns if "(Note)" in col or "(Video)" in col]

    grouped = df.groupby(['Date'])

    for (date,), month_df in grouped:
        # Aggregate across all Note/Video columns
        avg_value = month_df[cols].apply(
            lambda x: non_zero_avg(x.values.flatten()), axis=1).mean()

        image_avg = avg_value  # Use computed average

        # Calculate changes
        if months:
            prev_month = months[-1]
            image_change = safe_division(
                image_avg, prev_month['Image Pages Avg'])
        else:
            image_change = 100

        # Sync values
        res = {
            'Date': f"{date.date()}",
            'Image Pages Change': image_change,
            'Note Change': image_change,
            'Video Change': image_change,
            'Image Pages Avg': image_avg,
            'Note Avg': image_avg,
            'Video Avg': image_avg,
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
        # Remove date-related columns before calculating metrics
        metric_columns = [col for col in quarter_df.columns if col not in [
            'Date', 'Year', 'Quarter']]

        # Calculate averages
        image_avg = quarter_df[metric_columns].replace(
            0, pd.NA).mean(axis=1).mean().round(1)
        note_avg = quarter_df[[col for col in metric_columns if 'Note' in col]].replace(
            0, pd.NA).mean(axis=1).mean().round(1)
        video_avg = quarter_df[[col for col in metric_columns if 'Video' in col]].replace(
            0, pd.NA).mean(axis=1).mean().round(1)

        # Calculate changes
        if quarters:
            prev_quarter = quarters[-1]
            image_change = safe_division(
                image_avg, prev_quarter['Image Pages Avg'])
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
        # Remove date-related columns before calculating metrics
        metric_columns = [col for col in year_df.columns if col not in [
            'Date', 'Year', 'Month', 'Quarter']]

        # Calculate averages
        image_avg = year_df[metric_columns].replace(
            0, pd.NA).mean(axis=1).mean().round(1)
        note_avg = year_df[[col for col in metric_columns if 'Note' in col]].replace(
            0, pd.NA).mean(axis=1).mean().round(1)
        video_avg = year_df[[col for col in metric_columns if 'Video' in col]].replace(
            0, pd.NA).mean(axis=1).mean().round(1)

        # Calculate changes
        if years:
            prev_year = years[-1]
            image_change = safe_division(
                image_avg, prev_year['Image Pages Avg'])
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
    # Remove date-related columns before calculating metrics
    metric_columns = [col for col in df.columns if col not in [
        'Date', 'Year', 'Month', 'Quarter']]

    # Calculate all-time averages
    image_avg = df[metric_columns].replace(
        0, pd.NA).mean(axis=1).mean().round(1)
    note_avg = df[[col for col in metric_columns if 'Note' in col]].replace(
        0, pd.NA).mean(axis=1).mean().round(1)
    video_avg = df[[col for col in metric_columns if 'Video' in col]].replace(
        0, pd.NA).mean(axis=1).mean().round(1)

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
                {"name": "Image Pages Avg", "data": [
                    {"x": row["Date"], "y": row["Image Pages Avg"]} for row in data]},
                {"name": "Note Avg", "data": [
                    {"x": row["Date"], "y": row["Note Avg"]} for row in data]},
                {"name": "Video Avg", "data": [
                    {"x": row["Date"], "y": row["Video Avg"]} for row in data]},
            ],
            "changes": [
                {"name": "Image Pages Change", "data": [
                    {"x": row["Date"], "y": row["Image Pages Change"]} for row in data]},
                {"name": "Note Change", "data": [
                    {"x": row["Date"], "y": row["Note Change"]} for row in data]},
                {"name": "Video Change", "data": [
                    {"x": row["Date"], "y": row["Video Change"]} for row in data]},
            ],
        }
    }

    return response


def get_image_averages():
    df = init_image_data()
    quarter_data = calculate_quarterly_averages(df).to_dict('records')
    week_data = calculate_weekly_averages(df)
    # .to_dict('records')
    yearly_data = calculate_yearly_averages(df).to_dict('records')
    all_time_data = calculate_all_time_averages(df)

    return {
        "quarter": quarter_data,
        "yearly": yearly_data,
        "week": week_data,
        "all_time": all_time_data
    }


def get_image_insights(date_filter=None):
    df = init_image_data()

    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to datetime
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(
            date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

        # Filter the dataframe
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Calculate insights
    if not df.empty:
        initial_image = df['Image Pages Avg'].iloc[0]
        final_image = df['Image Pages Avg'].iloc[-1]
        initial_note = df['Note Avg'].iloc[0]
        final_note = df['Note Avg'].iloc[-1]
        initial_video = df['Video Avg'].iloc[0]
        final_video = df['Video Avg'].iloc[-1]

        # Calculate percentage changes
        image_change = ((final_image - initial_image) /
                        initial_image) * 100 if initial_image != 0 else 0
        note_change = ((final_note - initial_note) /
                       initial_note) * 100 if initial_note != 0 else 0
        video_change = ((final_video - initial_video) /
                        initial_video) * 100 if initial_video != 0 else 0

        def get_change_description(change):
            if abs(change) < 5:
                return None
            if abs(change) < 10:
                return "mildly"
            if abs(change) < 20:
                return "moderately"
            return "significantly"

        def format_insight(metric_name, change):
            if abs(change) < 5:
                return None
            change_type = "decreased" if change < 0 else "increased"
            change_desc = get_change_description(change)
            return f"{metric_name} performance {change_type} {change_desc} by {abs(change):.1f}%"

        insights = {
            "image": format_insight("Image pages", image_change),
            "note": format_insight("Note pages", note_change),
            "video": format_insight("Video pages", video_change)
        }
    else:
        insights = {
            "image": None,
            "note": None,
            "video": None
        }

    return insights


class GetImageRecordsView(View):
    def get(self, request):
        records = ImageRecord.objects.all().exclude(
            Q(note_first_contentful_paint=0) &
            Q(note_total_blocking_time=0) &
            Q(note_speed_index=0) &
            Q(note_largest_contentful_paint=0) &
            Q(note_cumulative_layout_shift=0) &
            Q(video_first_contentful_paint=0) &
            Q(video_total_blocking_time=0) &
            Q(video_speed_index=0) &
            Q(video_largest_contentful_paint=0) &
            Q(video_cumulative_layout_shift=0)
        ).values(
            'id', 'name', 'note_first_contentful_paint', 'note_total_blocking_time',
            'note_speed_index', 'note_largest_contentful_paint', 'note_cumulative_layout_shift',
            'video_first_contentful_paint', 'video_total_blocking_time', 'video_speed_index',
            'video_largest_contentful_paint', 'video_cumulative_layout_shift',
            'date'
        )

        return JsonResponse(list(records), safe=False)
