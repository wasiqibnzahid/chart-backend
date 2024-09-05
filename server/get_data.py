import pandas as pd
import threading

from collections import defaultdict
from .models import Record
from django.utils.dateparse import parse_date
from datetime import datetime
import json
from .old_code import df as df2, data
is_calc = False
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


def fetch_records():
    # Initialize a dictionary to store the results
    data = defaultdict(list)

    # Fetch all records, you can add filtering if necessary (e.g., for specific date range)
    records = Record.objects.all().order_by('date')

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
            data[f"{name} (Note)"].append(record.note_value)
            data[f"{name} (Video)"].append(record.video_value)

    # Convert defaultdict to a normal dictionary for output
    return dict(data)


def init(inner_data=None):
    if (inner_data is None):
        inner_data = fetch_records()
    df = pd.DataFrame(inner_data)

    # Calculating averages

    df['TV Azteca Avg'] = df[tv_azteca_columns].mean(axis=1).round(1)
    df['Competition Avg'] = df[competition_columns].mean(axis=1).round(1)

    df['TV Azteca Note Avg'] = df[[
        col for col in tv_azteca_columns if 'Note' in col]].mean(axis=1).round(1)
    df['Competition Note Avg'] = df[[
        col for col in competition_columns if 'Note' in col]].mean(axis=1).round(1)

    df['TV Azteca Video Avg'] = df[[
        col for col in tv_azteca_columns if 'Video' in col]].mean(axis=1).round(1)
    df['Competition Video Avg'] = df[[
        col for col in competition_columns if 'Video' in col]].mean(axis=1).round(1)

    def pct_change(series):
        return series.pct_change().apply(lambda x: x)

    df['TV Azteca Avg Change'] = pct_change(df['TV Azteca Avg'])
    df['Competition Avg Change'] = pct_change(df['Competition Avg'])

    df['TV Azteca Note Change'] = pct_change(df['TV Azteca Note Avg'])
    df['Competition Note Change'] = pct_change(df['Competition Note Avg'])

    df['TV Azteca Video Change'] = pct_change(df['TV Azteca Video Avg'])
    df['Competition Video Change'] = pct_change(df['Competition Video Avg'])
    return df


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
        insight = f"TV Azteca {most_relevant[1]} {most_relevant[2]} by {
            abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = "No significant changes were observed across the TV Azteca companies."

    return insight


def calculate_quarterly_averages(df):

    quarters = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q')

    # Group the data by year and quarter
    grouped = df.groupby(['Year', 'Quarter'])

    for (year, quarter), quarter_df in grouped:
        tv_azteca_avg = quarter_df[tv_azteca_columns].mean(
            axis=1).mean().round(1)
        competition_avg = quarter_df[competition_columns].mean(
            axis=1).mean().round(1)
        tv_azteca_avg_video = quarter_df[[
            col for col in tv_azteca_columns if 'Video' in col]].mean(
            axis=1).mean().round(1)
        competition_avg_video = quarter_df[[
            col for col in competition_columns if 'Video' in col]].mean(
            axis=1).mean().round(1)
        tv_azteca_avg_note = quarter_df[[
            col for col in tv_azteca_columns if 'Note' in col]].mean(
            axis=1).mean().round(1)
        competition_avg_note = quarter_df[[
            col for col in competition_columns if 'Note' in col]].mean(
            axis=1).mean().round(1)
        azteca_map = {}
        competition_map = {}

        if quarters:
            prev_quarter = quarters[-1]
            prev_tv_azteca_avg = prev_quarter['TV Azteca Avg']
            prev_competition_avg = prev_quarter['Competition Avg']
            prev_tv_azteca_avg_video = prev_quarter['TV Azteca Video Avg']
            prev_competition_avg_video = prev_quarter['Competition Video Avg']
            prev_tv_azteca_avg_note = prev_quarter['TV Azteca Note Avg']
            prev_competition_avg_note = prev_quarter['Competition Note Avg']

            tv_azteca_change = (
                tv_azteca_avg - prev_tv_azteca_avg) * 100 / prev_tv_azteca_avg
            competition_change = (
                competition_avg - prev_competition_avg) * 100 / prev_competition_avg
            tv_azteca_change_video = (
                tv_azteca_avg_video - prev_tv_azteca_avg_video) * 100 / prev_tv_azteca_avg_video
            competition_change_video = (
                competition_avg_video - prev_competition_avg_video) * 100 / prev_competition_avg_video
            tv_azteca_change_note = (
                tv_azteca_avg_note - prev_tv_azteca_avg_note) * 100 / prev_tv_azteca_avg_note
            competition_change_note = (
                competition_avg_note - prev_competition_avg_note) * 100 / prev_competition_avg_note
        else:
            tv_azteca_change = ""
            competition_change = ""
            tv_azteca_change_note = ""
            competition_change_note = ""
            tv_azteca_change_video = ""
            competition_change_video = ""
        res = {
            'Date': f"Q{quarter.quarter}-{year}",
            'TV Azteca Change': tv_azteca_change,
            'Competition Change': competition_change,
            'TV Azteca Video Change': tv_azteca_change_video,
            'Competition Video Change': competition_change_video,
            'TV Azteca Note Change': tv_azteca_change_note,
            'Competition Note Change': competition_change_note,
            'TV Azteca Avg': tv_azteca_avg,
            'Competition Avg': competition_avg,
            'TV Azteca Video Avg': tv_azteca_avg_video,
            'Competition Video Avg': competition_avg_video,
            'TV Azteca Note Avg': tv_azteca_avg_note,
            'Competition Note Avg': competition_avg_note,
            "competition": [],
            "azteca": []


        }
        for (index, company) in enumerate(azteca_columns_raw):

            company_avg = quarter_df[[
                col for col in tv_azteca_columns if company in col]].mean(
                axis=1).mean().round(1)
            company_avg_video = quarter_df[[
                col for col in tv_azteca_columns if 'Video' in col and company in col]].mean(
                axis=1).mean().round(1)
            company_avg_note = quarter_df[[
                col for col in tv_azteca_columns if 'Note' in col and company in col]].mean(
                axis=1).mean().round(1)
            if (len(quarters) > 0):
                item = prev_quarter.get("azteca")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = (
                    company_avg - prev_company_avg) * 100 / prev_company_avg
                company_change_video = (
                    company_avg_video - prev_company_avg_video) * 100 / prev_company_avg_video
                company_change_note = (
                    company_avg_note - prev_company_avg_note) * 100 / prev_company_avg_note
                prev_quarter = quarters[-1]
            else:
                company_change = ''
                company_change_video = ''
                company_change_note = ''
            res["azteca"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": company_change,
                "video_change": company_change_video,
                "note_change": company_change_note
            })

        for (index, company) in enumerate(competition_columns_raw):

            company_avg = quarter_df[[
                col for col in competition_columns if company in col]].mean(
                axis=1).mean().round(1)
            company_avg_video = quarter_df[[
                col for col in competition_columns if "Video" in col and company in col]].mean(
                axis=1).mean().round(1)
            company_avg_note = quarter_df[[
                col for col in competition_columns if "Note" in col and company in col]].mean(
                axis=1).mean().round(1)
            if (len(quarters) > 0):
                item = prev_quarter.get("competition")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = (
                    company_avg - prev_company_avg) * 100 / prev_company_avg
                company_change_video = (
                    company_avg_video - prev_company_avg_video) * 100 / prev_company_avg_video
                company_change_note = (
                    company_avg_note - prev_company_avg_note) * 100 / prev_company_avg_note
                prev_quarter = quarters[-1]
            else:
                company_change = ''
                company_change_video = ''
                company_change_note = ''
            res["competition"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": company_change,
                "video_change": company_change_video,
                "note_change": company_change_note
            })

        # for company in tv_azteca_columns:
        #     # Calculate average
        #     company_avg = quarter_df[company].mean().round(1)

        #     # Store the average in the results dictionary
        #     res['azteca'][f'{company} Avg'] = company_avg

        #     # Calculate change from the previous quarter if it exists
        #     if quarters:
        #         prev_company_avg = quarters[-1].get('azteca')[f'{company} Avg']
        #         if prev_company_avg is not None and prev_company_avg != 0:
        #             company_change = (
        #                 (company_avg - prev_company_avg) / prev_company_avg) * 100
        #             res['azteca'][f'{company} Change'] = company_change.round(1)
        #         else:
        #             res['azteca'][f'{company} Change'] = None
        #     else:
        #         res['azteca'][f'{company} Change'] = None
        # for company in competition_columns:
        #     # Calculate average
        #     company_avg = quarter_df[company].mean().round(1)

        #     # Store the average in the results dictionary
        #     res['competition'][f'{company} Avg'] = company_avg

        #     # Calculate change from the previous quarter if it exists
        #     if quarters:
        #         prev_company_avg = quarters[-1].get('competition')[f'{company} Avg']
        #         if prev_company_avg is not None and prev_company_avg != 0:
        #             company_change = (
        #                 (company_avg - prev_company_avg) / prev_company_avg) * 100
        #             res['competition'][f'{company} Change'] = company_change.round(1)
        #         else:
        #             res['competition'][f'{company} Change'] = None
        #     else:
        #         res['competition'][f'{company} Change'] = None

        # Append results for the quarter
        quarters.append(res)

    return pd.DataFrame(quarters)


label_mapping = {
    'Azteca UNO (Note)': 'UNO',
    'Azteca UNO (Video)': 'UNO',
    'Azteca 7 (Note)': '7',
    'Azteca 7 (Video)': '7',
    'El Heraldo (Note)': 'Heraldo',
    'El Heraldo (Video)': 'Heraldo',
    'El Universal (Note)': 'Universal',
    'El Universal (Video)': 'Universal'
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
        insight = f"Competition {most_relevant[1]} {most_relevant[2]} by {
            abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = None

    return insight


def formatLolData(df, inner_data):
    data_as_json = formatToJson(df2)
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
            combined_data[name][date]['sum'] += value
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
    return quarter_data


def get_insights(date_filter=None):
    df = init()
    video_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Video' in col], '', date_filter)
    video_self = calculate_relevant_insights(
        df, [col for col in list(
            label_mapping.keys()) if 'Video' in col], '', date_filter)
    note_other = calculate_competition_insights(
        df, [
            col for col in competition_columns if 'Note' in col], '', date_filter)
    note_self = calculate_relevant_insights(
        df, [col for col in list(
            label_mapping.keys()) if 'Note' in col], '', date_filter)
    total_self = calculate_relevant_insights(
        df, list(label_mapping.keys()), '', date_filter)
    total_competition = calculate_competition_insights(df, [
        col for col in competition_columns if col not in list(label_mapping.keys())], '', date_filter)
    return {
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
