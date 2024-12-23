import json
import pandas as pd

from server.models import Record
from django.db.models import Avg, F
from django.db.models.functions import TruncYear, TruncMonth

tv_azteca_columns = [
    'Azteca UNO (Note)', 'Azteca UNO (Video)', 'Azteca 7 (Note)', 'Azteca 7 (Video)',
    'Deportes (Note)', 'Deportes (Video)', 'ADN40 (Note)', 'ADN40 (Video)',
    'A+ (Note)', 'A+ (Video)', 'Noticias (Note)', 'Noticias (Video)'
]

azteca_columns_raw = [
    'Azteca UNO', 'Azteca 7',
    'Deportes', 'ADN40',
    'A+', 'Noticias'
]

competition_columns_raw = [
    'Milenio', 'El Heraldo',
    'El Universal', 'Televisa',
    'Terra', 'AS',
    'Infobae',  'NY Times',
]
competition_columns = [
    'Milenio (Note)', 'Milenio (Video)', 'El Heraldo (Note)', 'El Heraldo (Video)',
    'El Universal (Note)', 'El Universal (Video)', 'Televisa (Note)', 'Televisa (Video)',
    'Terra (Note)', 'Terra (Video)', 'AS (Note)', 'AS (Video)',
    'Infobae (Note)', 'Infobae (Video)', 'NY Times (Note)', 'NY Times (Video)'
]

from django.db.models import Avg, F
from django.db.models.functions import TruncMonth, TruncYear

def get_quarter_from_date(date):
    """Helper function to determine the quarter based on the month of the date"""
    month = date.month
    return f"Q{month}-{date.year}"

def calculate_changes(current_value, previous_value):
    """Helper function to calculate change between current and previous period"""
    return (current_value - previous_value) if previous_value else 0

def calculate_avg_for_columns(record, columns):
    """Helper function to calculate the average for the given columns"""
    values = [getattr(record, column, None) for column in columns]
    values = [value for value in values if value is not None]
    return sum(values) / len(values) if values else 0

def custom_function():
    # Calculate all-time averages
    all_time_averages = Record.objects.aggregate(
        avg_note_value=Avg('note_value'),
        avg_video_value=Avg('video_value'),
        avg_total_value=Avg('total_value')
    )

    # Initialize data for quarterly results
    quarters_data = []
    prev_quarter_averages = {}

    # Grouping by month and calculating the averages
    comp_records = Record.objects.filter(
        name__in=competition_columns_raw,
        note_value__gt=0,
        video_value__gt=0,
        total_value__gt=0
    ).annotate(
        month=TruncMonth('date'),
        year=TruncYear('date')
    ).values('year', 'month').annotate(
        avg_note_value=Avg('note_value'),
        avg_video_value=Avg('video_value'),
        avg_total_value=Avg('total_value')
    )

    azteca_records = Record.objects.filter(
        name__in=azteca_columns_raw,
        note_value__gt=0,
        video_value__gt=0,
        total_value__gt=0
    ).annotate(
        month=TruncMonth('date'),
        year=TruncYear('date')
    ).values('year', 'month').annotate(
        avg_note_value=Avg('note_value'),
        avg_video_value=Avg('video_value'),
        avg_total_value=Avg('total_value')
    )
    prev_comp_record = {}
    prev_azteca_record = {}
    # Iterate over records and combine Azteca and Competition data
    for comp_record, azteca_record in zip(comp_records, azteca_records):
        quarter = get_quarter_from_date(comp_record['month'])

        # If it's the first period, initialize previous data as 0
        if quarter not in prev_quarter_averages:
            prev_quarter_averages[quarter] = {
                'TV Azteca Change': 0,
                'Competition Change': 0,
                'TV Azteca Video Change': 0,
                'Competition Video Change': 0,
                'TV Azteca Note Change': 0,
                'Competition Note Change': 0
            }

        # Get previous period data for comparison
        prev_avg = prev_quarter_averages[quarter]

        # Calculate the changes for this quarter compared to the previous period
        tv_azteca_change = calculate_changes(getattr(azteca_record, 'total_value', 0), prev_azteca_record.get('total_value', 0))
        competition_change = calculate_changes(getattr(comp_record, 'total_value', 0), prev_comp_record.get('total_value', 0))
        tv_azteca_change_note = calculate_changes(getattr(azteca_record, 'note_value', 0), prev_azteca_record.get('note_value', 0))
        competition_change_note = calculate_changes(getattr(comp_record, 'note_value', 0), prev_comp_record.get('note_value', 0))
        tv_azteca_change_video = calculate_changes(getattr(azteca_record, 'video_value', 0), prev_azteca_record.get('video_value', 0))
        competition_change_video = calculate_changes(getattr(comp_record, 'video_value', 0), prev_comp_record.get('video_value', 0))

        # Store the data for this quarter
        quarter_data = {
            "Date": quarter,
            "TV Azteca Change": tv_azteca_change,
            "Competition Change": competition_change,
            "TV Azteca Video Change": tv_azteca_change_video,
            "Competition Video Change": competition_change_video,
            "TV Azteca Note Change": tv_azteca_change_note,
            "Competition Note Change": competition_change_note,
            "TV Azteca Avg": getattr(azteca_record, 'total_value', 0),
            "Competition Avg": getattr(comp_record, 'total_value', 0),
            "TV Azteca Video Avg": getattr(azteca_record, 'video_value', 0),
            "Competition Video Avg": getattr(comp_record, 'video_value', 0),
            "TV Azteca Note Avg": getattr(azteca_record, 'note_value', 0),
            "Competition Note Avg": getattr(comp_record, 'note_value', 0),
            "competition": [],
            "azteca": []
        }

        # Add company data for this quarter (Azteca & Competition)
        azteca_data = get_company_data(azteca_record, tv_azteca_columns, 'azteca')
        competition_data = get_company_data(comp_record, competition_columns, 'competition')

        # Add company data to quarter data
        quarter_data["azteca"].extend(azteca_data)
        quarter_data["competition"].extend(competition_data)

        # Append this quarter's data to the results list
        quarters_data.append(quarter_data)

        # Update previous period (quarter) averages for future comparisons
        prev_quarter_averages[quarter] = {
            'TV Azteca Change': azteca_record['avg_note_value'],
            'Competition Change': comp_record['avg_video_value'],
            'TV Azteca Video Change': azteca_record['avg_video_value'],
            'Competition Video Change': comp_record['avg_total_value'],
            'TV Azteca Note Change': azteca_record['avg_note_value'],
            'Competition Note Change': comp_record['avg_video_value']
        }

        prev_azteca_record = azteca_record
        prev_comp_record = comp_record

    return {
        'quarters_data': quarters_data,
        'all_time_averages': all_time_averages
    }

def get_company_data(record, columns, category):
    """
    Helper function to gather company data for Azteca or Competition
    """

    return {
        "name": record['name'],
        "total": record['note_value'],
        "video": record['video_value'],
        "note": record['total_value'],
        "total_change": 0,  # You may calculate the change based on previous periods
        "video_change": 0,
        "note_change": 0
    }

