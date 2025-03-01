import pandas as pd
from collections import defaultdict
from server.models import LocalRecord
from datetime import datetime
import json

is_calc = False


columns = [
    'TV Azteca Avg', 'Competition Avg',
    'TV Azteca Note Avg', 'Competition Note Avg',
    'TV Azteca Video Avg', 'Competition Video Avg', 'Date'
]

changeKeys = [
    'TV Azteca Avg Change',
    'Competition Avg Change',
    'TV Azteca Note Change',
    'Competition Note Change',
    'TV Azteca Video Change',
    'Competition Video Change',
]
azteca_columns = [
    'Azteca Veracruz (Note)', 'Azteca Veracruz (Video)', 'Azteca Quintanaroo (Note)', 'Azteca Quintanaroo (Video)',
    'Azteca BC (Note)', 'Azteca BC (Video)', 'Azteca Sinaloa (Note)', 'Azteca Sinaloa (Video)',
    'Azteca CJ (Note)', 'Azteca CJ (Video)', 'Azteca Aguascalientes (Note)', 'Azteca Aguascalientes (Video)'
]
azteca_columns_raw = [
    'Azteca Veracruz', 'Azteca Quintanaroo',
    'Azteca BC', 'Azteca Sinaloa',
    'Azteca CJ', 'Azteca Aguascalientes'
]

competition_columns = [
    'Azteca Queretaro (Note)', 'Azteca Queretaro (Video)', 'Azteca Chiapas (Note)', 'Azteca Chiapas (Video)',
    'Azteca Puebla (Note)', 'Azteca Puebla (Video)', 'Azteca Yucatan (Note)', 'Azteca Yucatan (Video)',
    'Azteca Chihuahua (Note)', 'Azteca Chihuahua (Video)', 'Azteca Morelos (Note)', 'Azteca Morelos (Video)',
    'Azteca Jalisco (Note)', 'Azteca Jalisco (Video)', 'Azteca Guerrero (Note)', 'Azteca Guerrero (Video)',
    'Azteca Bajio (Note)', 'Azteca Bajio (Video)', 'Laguna (Note)', 'Laguna (Video)'
]

competition_columns_raw = [
    'Azteca Queretaro', 'Azteca Chiapas',
    'Azteca Puebla', 'Azteca Yucatan',
    'Azteca Chihuahua', 'Azteca Morelos',
    'Azteca Jalisco',  'Azteca Guerrero',
    'Azteca Bajio', 'Laguna'
]
label_mapping = {
    'Azteca Veracruz (Note)': 'Veracruz',
    'Azteca Veracruz (Video)': 'Veracruz',
    'Azteca Quintanaroo (Note)': 'Quintanaroo',
    'Azteca Quintanaroo (Video)': 'Quintanaroo',
    'Azteca BC (Note)': 'BC',
    'Azteca BC (Video)': 'BC',
    'Azteca Sinaloa (Note)': 'Sinaloa',
    'Azteca Sinaloa (Video)': 'Sinaloa',
    "Azteca CJ (Note)": "CJ",
    "Azteca CJ (Video)": "CJ",
    "Azteca Aguascalientes (Note)": "Aguascalientes",
    "Azteca Aguascalientes (Video)": "Aguascalientes",
    "Azteca Queretaro (Note)": "Queretaro",
    "Azteca Queretaro (Video)": "Queretaro",
    "Laguna (Note)": "Laguna",
    "Laguna (Video)": "Laguna",
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
    "Azteca Bajio (Video)": "Bajio"
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


def formatToJson(df):
    json_str = df.to_json(orient='records')
    return json.loads(json_str)


def fetch_records():
    # Initialize a dictionary to store the results

    data = defaultdict(list)

    # Fetch all records, you can add filtering if necessary (e.g., for specific date range)
    records = LocalRecord.objects.all().order_by('date')

    # Group records by date
    grouped_records = defaultdict(list)

    for record in records:
        grouped_records[record.date].append(record)

    # Iterate over the grouped records and populate the dictionary
    for date, records_on_date in grouped_records.items():
        # Convert date to string format 'YYYY-MM-DD'
        data['Date'].append(str(date))

        for record in records_on_date:
            # Example: Azteca UNO (Note), Azteca UNO (Video)
            name = record.name
            data[f"{name} (Note)"].append(record.note_value or 0)
            data[f"{name} (Video)"].append(record.video_value or 0)

    # Convert defaultdict to a normal dictionary for output
    final_data = dict(data)
    return final_data


def init(inner_data=None):
    if (inner_data is None):
        inner_data = fetch_records()
    df = pd.DataFrame(inner_data)

    # Calculate averages excluding zeros
    df['TV Azteca Avg'] = df[azteca_columns][df[azteca_columns] != 0].mean(axis=1).round(1) or 0
    df['TV Azteca Avg'] = 0 if pd.isna(df['TV Azteca Avg']) else df['TV Azteca Avg']

    df['Competition Avg'] = df[competition_columns][df[competition_columns] != 0].mean(axis=1).round(1) or 0
    df['Competition Avg'] = 0 if pd.isna(df['Competition Avg']) else df['Competition Avg']

    df['TV Azteca Note Avg'] = df[[col for col in azteca_columns if 'Note' in col]][
        df[[col for col in azteca_columns if 'Note' in col]] != 0].mean(axis=1).round(1) or 0
    df['Competition Note Avg'] = df[[col for col in competition_columns if 'Note' in col]][
        df[[col for col in competition_columns if 'Note' in col]] != 0].mean(axis=1).round(1) or 0

    df['TV Azteca Video Avg'] = df[[col for col in azteca_columns if 'Video' in col]][
        df[[col for col in azteca_columns if 'Video' in col]] != 0].mean(axis=1).round(1) or 0
    df['Competition Video Avg'] = df[[col for col in competition_columns if 'Video' in col]][
        df[[col for col in competition_columns if 'Video' in col]] != 0].mean(axis=1).round(1) or 0

    def pct_change(series):
        return series.pct_change().apply(lambda x: x)

    df['TV Azteca Avg Change'] = pct_change(df['TV Azteca Avg'])
    df['Competition Avg Change'] = pct_change(df['Competition Avg'])

    df['TV Azteca Note Change'] = pct_change(df['TV Azteca Note Avg'])
    df['Competition Note Change'] = pct_change(df['Competition Note Avg'])

    df['TV Azteca Video Change'] = pct_change(df['TV Azteca Video Avg'])
    df['Competition Video Change'] = pct_change(df['Competition Video Avg'])

    return df


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
        date = entry["Date"]

        # Filter based on the date range if provided
        if (start_date and date < start_date) or (end_date and date > end_date):
            continue

        for key, value in entry.items():
            if key != "Date" and (key in include_columns or len(include_columns) == 0):
                if key not in series:
                    series[key] = []
                series[key].append({"x": date, "y": value})

    # Convert series to a list of dictionaries
    result = [{"name": key, "data": value} for key, value in series.items()]

    return result


def formatLolData(df, inner_data):
    data_as_json = formatToJson(df[[col for col in df.columns if not col.startswith(
        'TV') and not col.startswith("Competition")]])
    note = []
    video = []
    video_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Video' in col], '')
    video_self = calculate_relevant_insights(
        df, [col for col in list(
            label_mapping.keys()) if 'Video' in col], '')
    note_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Note' in col], '')
    note_self = calculate_relevant_insights(
        df, [col for col in list(
            label_mapping.keys()) if 'Note' in col], '')
    total_self = calculate_relevant_insights(
        df, list(label_mapping.keys()), '')
    total_competition = calculate_competition_insights(
        df, competition_columns, '')

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
        else:
            if item['name'] in label_mapping:
                item['name'] = label_mapping[item["name"]]
            else:
                item['name'] = item['name'].replace(" (Note)", "")
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
            combined_data[name][date]['sum'] += value or 0
            combined_data[name][date]['count'] += 1

    # Format the averages output
    totals = []
    for name, dates in combined_data.items():
        # Calculate averages for each date
        data = []
        for date, values in sorted(dates.items()):
            avg = (values['sum'] / values['count']) or 0
            avg = 0 if pd.isna(avg) else avg
            data.append({'x': date, 'y': avg})
        totals.append({'name': name, 'data': data})
    return {
        "videos": video,
        "notes": note,
        "total": totals,
        "insights": {
            "videos": {
                "self": video_self,
                "competition": video_other
            },
            "notes": {
                "self": note_self,
                "competition": note_other
            },
            "total": {
                "self": total_self,
                "competition": total_competition
            }
        }
    }


def calculate_competition_insights(filtered_df, companies, is_competition, date_filter=None):
    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to a datetime object representing the start and end of the month.
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(
            date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format if it's not already
        filtered_df['Date'] = pd.to_datetime(
            filtered_df['Date'], format='%Y-%m-%d')

        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (
            filtered_df['Date'] <= end_date)]
    significant_changes = []
    for company in companies:
        try:
            initial_value = filtered_df[company].iloc[0]
            final_value = filtered_df[company].iloc[-1]

            percentage_change = (
                (final_value - initial_value) / initial_value) * 100

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
            print(f"Exception: {e}")
            continue

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"TV Competition {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = None

    return insight


def calculate_relevant_insights(filtered_df, companies, title, date_filter=None):
    if date_filter:
        # Convert start and end dates from 'MM-YYYY' format to a datetime object representing the start and end of the month.
        start_date = pd.to_datetime(date_filter['start'], format='%m-%Y')
        end_date = pd.to_datetime(
            date_filter['end'], format='%m-%Y') + pd.offsets.MonthEnd(1)

        # Convert the 'Date' column to datetime format if it's not already
        filtered_df['Date'] = pd.to_datetime(
            filtered_df['Date'], format='%Y-%m-%d')

        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (
            filtered_df['Date'] <= end_date)]

    significant_changes = []

    # Check if the filtered DataFrame is not empty before proceeding
    if not filtered_df.empty:
        for company in companies:
            initial_value = filtered_df[company].iloc[0]
            final_value = filtered_df[company].iloc[-1]
            percentage_change = (
                (final_value - initial_value) / initial_value) * 100

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
        insight = f"TV Azteca {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = "No significant changes were observed across the Azteca companies."

    return insight
