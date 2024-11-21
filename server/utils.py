from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, List, Optional, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class AppConfig:
    DEFAULT_START_DATE: str = "01-2024"
    DEFAULT_END_DATE: str = "12-2024"
    MAX_ERROR_LOGS: int = 5
    ROUND_DECIMALS: int = 1

config = AppConfig()

def dummy_reverse(apps, schema_editor):
    pass

def safe_division(
    numerator: Optional[float], denominator: Optional[float], default: float = 0.0
) -> float:
    try:
        if denominator in [0, None] or pd.isna(denominator) or pd.isna(numerator):
            return default
        result = (numerator - denominator) * 100.0 / denominator
        return result if not pd.isna(result) else default
    except Exception as e:
        return default


def safe_mean(df_subset):
    """Safely calculate mean handling NaN values"""
    try:
        return df_subset.mean(axis=1).round(1)
    except Exception:
        return pd.Series([0] * len(df_subset))

def validate_date_filter(date_filter):
    """Validate and standardize date filter input"""
    try:
        start = datetime.strptime(date_filter.get('start', '01-2024'), '%m-%Y')
        end = datetime.strptime(date_filter.get('end', '12-2024'), '%m-%Y')
        if start > end:
            start, end = end, start
        return {'start': start, 'end': end}
    except ValueError:
        return None

class ErrorResponse(TypedDict):
    error: str
    details: Optional[str]

class InsightResponse(TypedDict):
    videos: dict
    notes: dict
    total: dict

class WeeklyResponse(TypedDict):
    data: List[dict]
    changes: List[dict]
    comparison: dict

def validate_dataframe_input(data: Dict[str, List[Any]]) -> Optional[Dict[str, List[Any]]]:
    """Validate input data for DataFrame creation"""
    if not data or 'Date' not in data:
        return None
        
    # Get the expected length from Date column
    expected_length = len(data['Date'])
    
    # Validate all arrays have the same length
    for key, value in data.items():
        if len(value) != expected_length:
            return None
            
    return data

def ensure_columns_exist(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
    """Ensure all required columns exist in DataFrame"""
    for column in required_columns:
        if column not in df.columns:
            df[column] = 0.0
    return df

def process_data_and_create_records(data, target_model_name, process_amp_values):
    from .models import Record, LocalRecord, Site, LocalSite
    from datetime import datetime
    errors = []

    try:
        # Extract dates from data
        dates = data.get('Date')
        if not dates:
            errors.append("No 'Date' field found in the data.")
            return errors

        # Remove 'Date' from keys to get site keys
        keys = list(data.keys())
        keys.remove('Date')

        # Extract site names from keys in data
        names_in_data = set()
        for key in keys:
            name = key.rsplit(' (', 1)[0]
            names_in_data.add(name)
        names_in_data = list(names_in_data)

        if process_amp_values:
            # Retrieve all site objects from both Site and LocalSite models
            site_objects = Site.objects.filter(name__in=names_in_data)
            localsite_objects = LocalSite.objects.filter(name__in=names_in_data)

            # Create mappings from site name to Site and LocalSite objects
            site_name_to_site = {site.name: site for site in site_objects}
            site_name_to_localsite = {site.name: site for site in localsite_objects}

            # Get all unique site names from both models
            all_site_names = site_name_to_site | site_name_to_localsite

            # Iterate through each date
            for i, date_str in enumerate(dates):
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    errors.append(f"Invalid date format: {date_str}")
                    continue

                # Iterate through all sites from both models
                for name, site_obj in all_site_names.items():
                    # Initialize keys for note and video
                    note_key = f'{name} (Note)'
                    video_key = f'{name} (Video)'

                    # Get note and video values from data if present, else set to zero
                    if name in names_in_data:
                        note_values = data.get(note_key)
                        video_values = data.get(video_key)
                        note_value = note_values[i] if note_values and i < len(note_values) else 0
                        video_value = video_values[i] if video_values and i < len(video_values) else 0
                    else:
                        note_value = 0
                        video_value = 0

                    # Calculate total_value
                    total_value = note_value + video_value

                    # Determine if 'azteca' should be True or False
                    azteca = 'Azteca' in name

                    # Prepare record data for AMP values
                    record_data_amp = {
                        'amp_note_value': note_value,
                        'amp_video_value': video_value,
                        'amp_total_value': total_value,
                        'azteca': azteca,
                        'date': date,
                    }

                    # Process for Site model
                    site_obj = site_name_to_site.get(name)
                    if site_obj:
                        # Create or update Record
                        Record.objects.update_or_create(
                            name=name,
                            date=date,
                            defaults=record_data_amp
                        )

                    # Process for LocalSite model
                    localsite_obj = site_name_to_localsite.get(name)
                    if localsite_obj:
                        # Create or update LocalRecord
                        LocalRecord.objects.update_or_create(
                            name=name,
                            date=date,
                            defaults=record_data_amp
                        )

        else:
            # Not processing AMP values; use target_model_name to determine models
            if target_model_name == 'record':
                TargetRecordModel = Record
                TargetSiteModel = Site
            elif target_model_name == 'localrecord':
                TargetRecordModel = LocalRecord
                TargetSiteModel = LocalSite
            else:
                errors.append(f"Invalid target model: {target_model_name}")
                return errors

            # Retrieve site objects from the target model
            site_objects = TargetSiteModel.objects.filter(name__in=names_in_data)
            site_name_to_obj = {site.name: site for site in site_objects}

            # Iterate through each date
            for i, date_str in enumerate(dates):
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    errors.append(f"Invalid date format: {date_str}")
                    continue

                # Iterate through all sites in the target model
                for name, site_obj in site_name_to_obj.items():
                    # Initialize keys for note and video
                    note_key = f'{name} (Note)'
                    video_key = f'{name} (Video)'

                    # Get note and video values from data if present, else set to zero
                    if name in names_in_data:
                        note_values = data.get(note_key)
                        video_values = data.get(video_key)
                        note_value = note_values[i] if note_values and i < len(note_values) else 0
                        video_value = video_values[i] if video_values and i < len(video_values) else 0
                    else:
                        note_value = 0
                        video_value = 0

                    # Calculate total_value
                    total_value = note_value + video_value

                    # Determine if 'azteca' should be True or False
                    azteca = 'Azteca' in name

                    # Prepare record data for non-AMP values
                    record_data_non_amp = {
                        'note_value': note_value,
                        'video_value': video_value,
                        'total_value': total_value,
                        'amp_note_value': None,
                        'amp_video_value': None,
                        'amp_total_value': None,
                        'azteca': azteca,
                        'date': date,
                        'site': site_obj,
                    }

                    # Create or update Record or LocalRecord
                    TargetRecordModel.objects.update_or_create(
                        name=name,
                        date=date,
                        defaults=record_data_non_amp
                    )

    except Exception as e:
        errors.append(str(e))

    return errors
