import json
from server.utils import safe_division
from django.utils import timezone
from .local_data import init, formatToJson, azteca_columns, competition_columns, azteca_columns_raw,competition_columns_raw
import pandas as pd
def get_averages():
    df = init()
    quarter_data = formatToJson(
        calculate_quarterly_averages(df))
    week_data = formatToJson(
        calculate_weekly_averages(df))
    year_data = formatToJson(
        calculate_yearly_averages(df))
    all_time_data = calculate_all_time_averages(df)

    return {
        "quarter": quarter_data,
        "week": week_data,
        "year": year_data,
        "all_time": all_time_data,
    }
def calculate_weekly_averages(df):

    months = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')

    # Group the data by year and month
    grouped = df.groupby(['Date'])

    for (date,), month_df in grouped:
        azteca_avg = round(month_df[azteca_columns][month_df[azteca_columns] != 0].mean(axis=1).mean(), 1)
        competition_avg = round(month_df[competition_columns][month_df[competition_columns] != 0].mean(axis=1).mean(), 1)
        azteca_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col]][month_df[[col for col in azteca_columns if 'Video' in col]] != 0].mean(axis=1).mean(), 1)
        competition_avg_video = round(month_df[[col for col in competition_columns if 'Video' in col]][month_df[[col for col in competition_columns if 'Video' in col]] != 0].mean(axis=1).mean(), 1)
        azteca_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col]][month_df[[col for col in azteca_columns if 'Note' in col]] != 0].mean(axis=1).mean(), 1)
        competition_avg_note = round(month_df[[col for col in competition_columns if 'Note' in col]][month_df[[col for col in competition_columns if 'Note' in col]] != 0].mean(axis=1).mean(), 1)

        azteca_map = {}
        competition_map = {}

        if months:
            prev_month = months[-1]
            prev_azteca_avg = prev_month['TV Azteca Avg']
            prev_competition_avg = prev_month['Competition Avg']
            prev_azteca_avg_video = prev_month['TV Azteca Video Avg']
            prev_competition_avg_video = prev_month['Competition Video Avg']
            prev_azteca_avg_note = prev_month['TV Azteca Note Avg']
            prev_competition_avg_note = prev_month['Competition Note Avg']

            azteca_change = safe_division(azteca_avg, prev_azteca_avg)
            competition_change = safe_division(competition_avg, prev_competition_avg)
            azteca_change_video = safe_division(azteca_avg_video, prev_azteca_avg_video)
            competition_change_video = safe_division(competition_avg_video, prev_competition_avg_video)
            azteca_change_note = safe_division(azteca_avg_note, prev_azteca_avg_note)
            competition_change_note = safe_division(competition_avg_note, prev_competition_avg_note)

        else:
            azteca_change = 100
            competition_change = 100
            azteca_change_note = 100
            competition_change_note = 100
            azteca_change_video = 100
            competition_change_video = 100
        res = {
            'Date': f"{date.date()}",
            'TV Azteca Change': azteca_change,
            'Competition Change': competition_change,
            'TV Azteca Video Change': azteca_change_video,
            'Competition Video Change': competition_change_video,
            'TV Azteca Note Change': azteca_change_note,
            'Competition Note Change': competition_change_note,
            'TV Azteca Avg': azteca_avg,
            'Competition Avg': competition_avg,
            'TV Azteca Video Avg': azteca_avg_video,
            'Competition Video Avg': competition_avg_video,
            'TV Azteca Note Avg': azteca_avg_note,
            'Competition Note Avg': competition_avg_note,
            "competition": [],
            "azteca": []
        }

        for (index, company) in enumerate(azteca_columns_raw):
            company_avg = round(month_df[[col for col in azteca_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("azteca")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["azteca"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
            })

        for (index, company) in enumerate(competition_columns_raw):
            company_avg = round(month_df[[col for col in competition_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in competition_columns if "Video" in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in competition_columns if "Note" in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("competition")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["competition"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
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
        azteca_avg = round(month_df[azteca_columns].mean(axis=1).mean(), 1)
        competition_avg = round(month_df[competition_columns].mean(axis=1).mean(), 1)
        azteca_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col]].mean(axis=1).mean(), 1)
        competition_avg_video = round(month_df[[col for col in competition_columns if 'Video' in col]].mean(axis=1).mean(), 1)
        azteca_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col]].mean(axis=1).mean(), 1)
        competition_avg_note = round(month_df[[col for col in competition_columns if 'Note' in col]].mean(axis=1).mean(), 1)

        azteca_map = {}
        competition_map = {}

        if months:
            prev_month = months[-1]
            prev_azteca_avg = prev_month['TV Azteca Avg']
            prev_competition_avg = prev_month['Competition Avg']
            prev_azteca_avg_video = prev_month['TV Azteca Video Avg']
            prev_competition_avg_video = prev_month['Competition Video Avg']
            prev_azteca_avg_note = prev_month['TV Azteca Note Avg']
            prev_competition_avg_note = prev_month['Competition Note Avg']

            azteca_change = safe_division(azteca_avg, prev_azteca_avg)
            competition_change = safe_division(competition_avg, prev_competition_avg)
            azteca_change_video = safe_division(azteca_avg_video, prev_azteca_avg_video)
            competition_change_video = safe_division(competition_avg_video, prev_competition_avg_video)
            azteca_change_note = safe_division(azteca_avg_note, prev_azteca_avg_note)
            competition_change_note = safe_division(competition_avg_note, prev_competition_avg_note)

        else:
            azteca_change = 100
            competition_change = 100
            azteca_change_note = 100
            competition_change_note = 100
            azteca_change_video = 100
            competition_change_video = 100
        res = {
            'Date': f"Q{int(month.strftime('%m'))}-{year}",
            'TV Azteca Change': azteca_change,
            'Competition Change': competition_change,
            'TV Azteca Video Change': azteca_change_video,
            'Competition Video Change': competition_change_video,
            'TV Azteca Note Change': azteca_change_note,
            'Competition Note Change': competition_change_note,
            'TV Azteca Avg': azteca_avg,
            'Competition Avg': competition_avg,
            'TV Azteca Video Avg': azteca_avg_video,
            'Competition Video Avg': competition_avg_video,
            'TV Azteca Note Avg': azteca_avg_note,
            'Competition Note Avg': competition_avg_note,
            "competition": [],
            "azteca": []
        }

        for (index, company) in enumerate(azteca_columns_raw):
            company_avg = round(month_df[[col for col in azteca_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("azteca")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["azteca"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
            })

        for (index, company) in enumerate(competition_columns_raw):
            company_avg = round(month_df[[col for col in competition_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in competition_columns if "Video" in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in competition_columns if "Note" in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("competition")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["competition"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
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
        azteca_avg = round(month_df[azteca_columns].mean(axis=1).mean(), 1)
        competition_avg = round(month_df[competition_columns].mean(axis=1).mean(), 1)
        azteca_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col]].mean(axis=1).mean(), 1)
        competition_avg_video = round(month_df[[col for col in competition_columns if 'Video' in col]].mean(axis=1).mean(), 1)
        azteca_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col]].mean(axis=1).mean(), 1)
        competition_avg_note = round(month_df[[col for col in competition_columns if 'Note' in col]].mean(axis=1).mean(), 1)

        azteca_map = {}
        competition_map = {}

        if months:
            prev_month = months[-1]
            prev_azteca_avg = prev_month['TV Azteca Avg']
            prev_competition_avg = prev_month['Competition Avg']
            prev_azteca_avg_video = prev_month['TV Azteca Video Avg']
            prev_competition_avg_video = prev_month['Competition Video Avg']
            prev_azteca_avg_note = prev_month['TV Azteca Note Avg']
            prev_competition_avg_note = prev_month['Competition Note Avg']

            azteca_change = safe_division(azteca_avg, prev_azteca_avg)
            competition_change = safe_division(competition_avg, prev_competition_avg)
            azteca_change_video = safe_division(azteca_avg_video, prev_azteca_avg_video)
            competition_change_video = safe_division(competition_avg_video, prev_competition_avg_video)
            azteca_change_note = safe_division(azteca_avg_note, prev_azteca_avg_note)
            competition_change_note = safe_division(competition_avg_note, prev_competition_avg_note)

        else:
            azteca_change = 100
            competition_change = 100
            azteca_change_note = 100
            competition_change_note = 100
            azteca_change_video = 100
            competition_change_video = 100
        res = {
            'Date': f"Q{int(1)}-{year}",
            'TV Azteca Change': azteca_change,
            'Competition Change': competition_change,
            'TV Azteca Video Change': azteca_change_video,
            'Competition Video Change': competition_change_video,
            'TV Azteca Note Change': azteca_change_note,
            'Competition Note Change': competition_change_note,
            'TV Azteca Avg': azteca_avg,
            'Competition Avg': competition_avg,
            'TV Azteca Video Avg': azteca_avg_video,
            'Competition Video Avg': competition_avg_video,
            'TV Azteca Note Avg': azteca_avg_note,
            'Competition Note Avg': competition_avg_note,
            "competition": [],
            "azteca": []
        }

        for (index, company) in enumerate(azteca_columns_raw):
            company_avg = round(month_df[[col for col in azteca_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("azteca")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["azteca"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
            })

        for (index, company) in enumerate(competition_columns_raw):
            company_avg = round(month_df[[col for col in competition_columns if company in col]].mean(axis=1).mean(), 1)
            company_avg_video = round(month_df[[col for col in competition_columns if "Video" in col and company in col]].mean(axis=1).mean(), 1)
            company_avg_note = round(month_df[[col for col in competition_columns if "Note" in col and company in col]].mean(axis=1).mean(), 1)

            if (len(months) > 0):
                item = prev_month.get("competition")[index]
                prev_company_avg_video = item["video"]
                prev_company_avg_note = item["note"]
                prev_company_avg = item["total"]
                company_change = safe_division(company_avg, prev_company_avg)
                if(prev_company_avg == 0):
                    company_change = 0
                company_change_video = safe_division(company_avg_video, prev_company_avg_video)
                if(prev_company_avg_video == 0):
                    company_change_video = 0
                company_change_note = safe_division(company_avg_note, prev_company_avg_note)
                if(prev_company_avg_note == 0):
                    company_change_note = 0
                prev_month = months[-1]
            else:
                company_change = 100
                company_change_video = 100
                company_change_note = 100
            res["competition"].append({
                "name": company,
                "total": company_avg,
                "video": company_avg_video,
                "note": company_avg_note,
                "total_change": 0 if pd.isna(company_change) else (company_change or 0),
                "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
                "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
            })

        months.append(res)

    return pd.DataFrame(months)

def calculate_all_time_averages(df):
    date = timezone.now()
    azteca_avg = round(df[azteca_columns].mean(axis=1).mean(), 1)
    competition_avg = round(df[competition_columns].mean(axis=1).mean(), 1)
    azteca_avg_video = round(df[[col for col in azteca_columns if 'Video' in col]].mean(axis=1).mean(), 1)
    competition_avg_video = round(df[[col for col in competition_columns if 'Video' in col]].mean(axis=1).mean(), 1)
    azteca_avg_note = round(df[[col for col in azteca_columns if 'Note' in col]].mean(axis=1).mean(), 1)
    competition_avg_note = round(df[[col for col in competition_columns if 'Note' in col]].mean(axis=1).mean(), 1)

    res = {
        'Date': f"{date.date()}",
        'TV Azteca Change': 100,
        'Competition Change': 100,
        'TV Azteca Video Change': 100,
        'Competition Video Change': 100,
        'TV Azteca Note Change': 100,
        'Competition Note Change': 100,
        'TV Azteca Avg': azteca_avg,
        'Competition Avg': competition_avg,
        'TV Azteca Video Avg': azteca_avg_video,
        'Competition Video Avg': competition_avg_video,
        'TV Azteca Note Avg': azteca_avg_note,
        'Competition Note Avg': competition_avg_note,
        "competition": [],
        "azteca": []
    }

    for (index, company) in enumerate(azteca_columns_raw):
        company_avg = round(df[[col for col in azteca_columns if company in col]].mean(axis=1).mean(), 1)
        company_avg_video = round(df[[col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean(), 1)
        company_avg_note = round(df[[col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean(), 1)

        res["azteca"].append({
            "name": company,
            "total": company_avg,
            "video": company_avg_video,
            "note": company_avg_note,
            "total_change": 100,
            "video_change": 100,
            "note_change": 100
        })

    for (index, company) in enumerate(competition_columns_raw):
        company_avg = round(df[[col for col in competition_columns if company in col]].mean(axis=1).mean(), 1)
        company_avg_video = round(df[[col for col in competition_columns if "Video" in col and company in col]].mean(axis=1).mean(), 1)
        company_avg_note = round(df[[col for col in competition_columns if "Note" in col and company in col]].mean(axis=1).mean(), 1)

        res["competition"].append({
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
    azteca_avg_latest = round(latest_df[azteca_columns].mean(axis=1).mean(), 1)
    competition_avg_latest = round(latest_df[competition_columns].mean(axis=1).mean(), 1)
    azteca_avg_video_latest = round(latest_df[
        [col for col in azteca_columns if 'Video' in col]
    ].mean(axis=1).mean(), 1)
    competition_avg_video_latest = round(latest_df[
        [col for col in competition_columns if 'Video' in col]
    ].mean(axis=1).mean(), 1)
    azteca_avg_note_latest = round(latest_df[
        [col for col in azteca_columns if 'Note' in col]
    ].mean(axis=1).mean(), 1)
    competition_avg_note_latest = round(latest_df[
        [col for col in competition_columns if 'Note' in col]
    ].mean(axis=1).mean(), 1)


    # Compute averages for the second-to-last date
    azteca_avg_second_last = round(second_last_df[azteca_columns].mean(axis=1).mean(), 1)
    competition_avg_second_last = round(second_last_df[competition_columns].mean(axis=1).mean(), 1)
    azteca_avg_video_second_last = round(second_last_df[
        [col for col in azteca_columns if 'Video' in col]
    ].mean(axis=1).mean(), 1)
    competition_avg_video_second_last = round(second_last_df[
        [col for col in competition_columns if 'Video' in col]
    ].mean(axis=1).mean(), 1)
    azteca_avg_note_second_last = round(second_last_df[
        [col for col in azteca_columns if 'Note' in col]
    ].mean(axis=1).mean(), 1)
    competition_avg_note_second_last = round(second_last_df[
        [col for col in competition_columns if 'Note' in col]
    ].mean(axis=1).mean(), 1)


    # Calculate the changes
    azteca_change = safe_division(azteca_avg_latest, azteca_avg_second_last)
    competition_change = safe_division(competition_avg_latest, competition_avg_second_last)
    azteca_change_video = safe_division(azteca_avg_video_latest, azteca_avg_video_second_last)
    competition_change_video = safe_division(competition_avg_video_latest, competition_avg_video_second_last)
    azteca_change_note = safe_division(azteca_avg_note_latest, azteca_avg_note_second_last)
    competition_change_note = safe_division(competition_avg_note_latest, competition_avg_note_second_last)


    # Prepare the result dictionary
    res = {
        'Date': latest_date.strftime('%Y-%m-%d'),
        'TV Azteca Change': azteca_change,
        'Competition Change': competition_change,
        'TV Azteca Video Change': azteca_change_video,
        'Competition Video Change': competition_change_video,
        'TV Azteca Note Change': azteca_change_note,
        'Competition Note Change': competition_change_note,
        'TV Azteca Avg': azteca_avg_latest,
        'Competition Avg': competition_avg_latest,
        'TV Azteca Video Avg': azteca_avg_video_latest,
        'Competition Video Avg': competition_avg_video_latest,
        'TV Azteca Note Avg': azteca_avg_note_latest,
        'Competition Note Avg': competition_avg_note_latest,
        "competition": [],
        "azteca": []
    }

    # Add company-level data comparison (Azteca)
    for (index, company) in enumerate(azteca_columns_raw):
        company_avg_latest = round(latest_df[
            [col for col in azteca_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_latest = round(latest_df[
            [col for col in azteca_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_latest = round(latest_df[
            [col for col in azteca_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_second_last = round(second_last_df[
            [col for col in azteca_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_second_last = round(second_last_df[
            [col for col in azteca_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_second_last = round(second_last_df[
            [col for col in azteca_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)


        company_change = safe_division(company_avg_latest, company_avg_second_last)
        if(company_avg_second_last == 0):
            company_change = 0
        company_change_video = safe_division(company_avg_video_latest, company_avg_video_second_last)
        if(company_avg_video_second_last == 0):
            company_change_video = 0
        company_change_note = safe_division(company_avg_note_latest,company_avg_note_second_last)
        if(company_avg_note_second_last == 0):
            company_change_note = 0

        res["azteca"].append({
            "name": company,
            "total": company_avg_latest,
            "video": company_avg_video_latest,
            "note": company_avg_note_latest,
            "total_change": 0 if pd.isna(company_change) else (company_change or 0),
            "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
            "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
        })

    # Add company-level data comparison (Competition)
    for (index, company) in enumerate(competition_columns_raw):
        company_avg_latest = round(latest_df[
            [col for col in competition_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_latest = round(latest_df[
            [col for col in competition_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_latest = round(latest_df[
            [col for col in competition_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_second_last = round(second_last_df[
            [col for col in competition_columns if company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_video_second_last = round(second_last_df[
            [col for col in competition_columns if 'Video' in col and company in col]
        ].mean(axis=1).mean(), 1)

        company_avg_note_second_last = round(second_last_df[
            [col for col in competition_columns if 'Note' in col and company in col]
        ].mean(axis=1).mean(), 1)


        company_change = safe_division(company_avg_latest, company_avg_second_last)
        if(company_avg_second_last == 0):
            company_change = 0
        company_change_video = safe_division(company_avg_video_latest, company_avg_video_second_last)
        if(company_avg_video_second_last == 0):
            company_change_video = 0
        company_change_note = safe_division(company_avg_note_latest , company_avg_note_second_last)
        if(company_avg_note_second_last == 0):
            company_change_note = 0


        res["competition"].append({
            "name": company,
            "total": company_avg_latest,
            "video": company_avg_video_latest,
            "note": company_avg_note_latest,
            "total_change": 0 if pd.isna(company_change) else (company_change or 0),
            "video_change": 0 if pd.isna(company_change_video) else (company_change_video or 0),
            "note_change": 0 if pd.isna(company_change_note) else (company_change_note or 0)
        })

    return res
