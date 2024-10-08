from .local_data import init, formatToJson, azteca_columns, competition_columns, azteca_columns_raw,competition_columns_raw
import pandas as pd
def get_averages():
    df = init()
    quarter_data = formatToJson(
        calculate_quarterly_averages(df))
    week_data = calculate_changes(df)

    return {
        "quarter": quarter_data,
        "week": week_data
    }

def calculate_quarterly_averages(df):

    quarters = []
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q')

    # Group the data by year and quarter
    grouped = df.groupby(['Year', 'Quarter'])

    for (year, quarter), quarter_df in grouped:
        azteca_avg = quarter_df[azteca_columns].mean(
            axis=1).mean().round(1)
        competition_avg = quarter_df[competition_columns].mean(
            axis=1).mean().round(1)
        azteca_avg_video = quarter_df[[
            col for col in azteca_columns if 'Video' in col]].mean(
            axis=1).mean().round(1)
        competition_avg_video = quarter_df[[
            col for col in competition_columns if 'Video' in col]].mean(
            axis=1).mean().round(1)
        azteca_avg_note = quarter_df[[
            col for col in azteca_columns if 'Note' in col]].mean(
            axis=1).mean().round(1)
        competition_avg_note = quarter_df[[
            col for col in competition_columns if 'Note' in col]].mean(
            axis=1).mean().round(1)
        azteca_map = {}
        competition_map = {}

        if quarters:
            prev_quarter = quarters[-1]
            prev_azteca_avg = prev_quarter['TV Azteca Avg']
            prev_competition_avg = prev_quarter['Competition Avg']
            prev_azteca_avg_video = prev_quarter['TV Azteca Video Avg']
            prev_competition_avg_video = prev_quarter['Competition Video Avg']
            prev_azteca_avg_note = prev_quarter['TV Azteca Note Avg']
            prev_competition_avg_note = prev_quarter['Competition Note Avg']

            azteca_change = (
                azteca_avg - prev_azteca_avg) * 100 / prev_azteca_avg
            competition_change = (
                competition_avg - prev_competition_avg) * 100 / prev_competition_avg
            azteca_change_video = (
                azteca_avg_video - prev_azteca_avg_video) * 100 / prev_azteca_avg_video
            competition_change_video = (
                competition_avg_video - prev_competition_avg_video) * 100 / prev_competition_avg_video
            azteca_change_note = (
                azteca_avg_note - prev_azteca_avg_note) * 100 / prev_azteca_avg_note
            competition_change_note = (
                competition_avg_note - prev_competition_avg_note) * 100 / prev_competition_avg_note
        else:
            azteca_change = ""
            competition_change = ""
            azteca_change_note = ""
            competition_change_note = ""
            azteca_change_video = ""
            competition_change_video = ""
        res = {
            'Date': f"Q3-{year}",
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

            company_avg = quarter_df[[
                col for col in azteca_columns if company in col]].mean(
                axis=1).mean().round(1)
            company_avg_video = quarter_df[[
                col for col in azteca_columns if 'Video' in col and company in col]].mean(
                axis=1).mean().round(1)
            company_avg_note = quarter_df[[
                col for col in azteca_columns if 'Note' in col and company in col]].mean(
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

        quarters.append(res)

    return pd.DataFrame(quarters)

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
    azteca_avg_latest = latest_df[azteca_columns].mean(
        axis=1).mean().round(1)
    competition_avg_latest = latest_df[competition_columns].mean(
        axis=1).mean().round(1)
    azteca_avg_video_latest = latest_df[[
        col for col in azteca_columns if 'Video' in col]].mean(axis=1).mean().round(1)
    competition_avg_video_latest = latest_df[[
        col for col in competition_columns if 'Video' in col]].mean(axis=1).mean().round(1)
    azteca_avg_note_latest = latest_df[[
        col for col in azteca_columns if 'Note' in col]].mean(axis=1).mean().round(1)
    competition_avg_note_latest = latest_df[[
        col for col in competition_columns if 'Note' in col]].mean(axis=1).mean().round(1)

    # Compute averages for the second-to-last date
    azteca_avg_second_last = second_last_df[azteca_columns].mean(
        axis=1).mean().round(1)
    competition_avg_second_last = second_last_df[competition_columns].mean(
        axis=1).mean().round(1)
    azteca_avg_video_second_last = second_last_df[[
        col for col in azteca_columns if 'Video' in col]].mean(axis=1).mean().round(1)
    competition_avg_video_second_last = second_last_df[[
        col for col in competition_columns if 'Video' in col]].mean(axis=1).mean().round(1)
    azteca_avg_note_second_last = second_last_df[[
        col for col in azteca_columns if 'Note' in col]].mean(axis=1).mean().round(1)
    competition_avg_note_second_last = second_last_df[[
        col for col in competition_columns if 'Note' in col]].mean(axis=1).mean().round(1)

    # Calculate the changes
    azteca_change = (azteca_avg_latest -
                        azteca_avg_second_last) * 100 / azteca_avg_second_last
    competition_change = (competition_avg_latest -
                          competition_avg_second_last) * 100 / competition_avg_second_last
    azteca_change_video = (azteca_avg_video_latest -
                              azteca_avg_video_second_last) * 100 / azteca_avg_video_second_last
    competition_change_video = (competition_avg_video_latest -
                                competition_avg_video_second_last) * 100 / competition_avg_video_second_last
    azteca_change_note = (azteca_avg_note_latest -
                             azteca_avg_note_second_last) * 100 / azteca_avg_note_second_last
    competition_change_note = (competition_avg_note_latest -
                               competition_avg_note_second_last) * 100 / competition_avg_note_second_last

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
        company_avg_latest = latest_df[[
            col for col in azteca_columns if company in col]].mean(axis=1).mean().round(1)
        company_avg_video_latest = latest_df[[
            col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean().round(1)
        company_avg_note_latest = latest_df[[
            col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean().round(1)

        company_avg_second_last = second_last_df[[
            col for col in azteca_columns if company in col]].mean(axis=1).mean().round(1)
        company_avg_video_second_last = second_last_df[[
            col for col in azteca_columns if 'Video' in col and company in col]].mean(axis=1).mean().round(1)
        company_avg_note_second_last = second_last_df[[
            col for col in azteca_columns if 'Note' in col and company in col]].mean(axis=1).mean().round(1)

        company_change = (
            company_avg_latest - company_avg_second_last) * 100 / company_avg_second_last
        company_change_video = (
            company_avg_video_latest - company_avg_video_second_last) * 100 / company_avg_video_second_last
        company_change_note = (
            company_avg_note_latest - company_avg_note_second_last) * 100 / company_avg_note_second_last

        res["azteca"].append({
            "name": company,
            "total": company_avg_latest,
            "video": company_avg_video_latest,
            "note": company_avg_note_latest,
            "total_change": company_change,
            "video_change": company_change_video,
            "note_change": company_change_note
        })

    # Add company-level data comparison (Competition)
    for (index, company) in enumerate(competition_columns_raw):
        company_avg_latest = latest_df[[
            col for col in competition_columns if company in col]].mean(axis=1).mean().round(1)
        company_avg_video_latest = latest_df[[
            col for col in competition_columns if 'Video' in col and company in col]].mean(axis=1).mean().round(1)
        company_avg_note_latest = latest_df[[
            col for col in competition_columns if 'Note' in col and company in col]].mean(axis=1).mean().round(1)

        company_avg_second_last = second_last_df[[
            col for col in competition_columns if company in col]].mean(axis=1).mean().round(1)
        company_avg_video_second_last = second_last_df[[
            col for col in competition_columns if 'Video' in col and company in col]].mean(axis=1).mean().round(1)
        company_avg_note_second_last = second_last_df[[
            col for col in competition_columns if 'Note' in col and company in col]].mean(axis=1).mean().round(1)

        company_change = (
            company_avg_latest - company_avg_second_last) * 100 / company_avg_second_last
        company_change_video = (
            company_avg_video_latest - company_avg_video_second_last) * 100 / company_avg_video_second_last
        company_change_note = (
            company_avg_note_latest - company_avg_note_second_last) * 100 / company_avg_note_second_last

        res["competition"].append({
            "name": company,
            "total": company_avg_latest,
            "video": company_avg_video_latest,
            "note": company_avg_note_latest,
            "total_change": company_change,
            "video_change": company_change_video,
            "note_change": company_change_note
        })

    return res