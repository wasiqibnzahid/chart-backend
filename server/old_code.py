from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Data setup
data = {
    'Date': [
        '2024-06-17',
        '2024-06-25',
        '2024-07-02',
        '2024-07-08',
        '2024-07-22',
        '2024-07-29',
        '2024-08-05',
        '2024-08-12',
        '2024-08-19'
    ],
    'Azteca UNO (Note)': [78, 74, 77, 78, 69, 72, 64, 66, 66],
    'Azteca UNO (Video)': [63, 81, 79, 76, 71, 74, 71, 69, 72],
    'Azteca 7 (Note)': [63, 64, 65, 63, 67, 65, 65, 67, 66],
    'Azteca 7 (Video)': [59, 68, 64, 67, 70, 74, 66, 70, 72],
    'Deportes (Note)': [56, 61, 59, 64, 67, 65, 60, 66, 65],
    'Deportes (Video)': [64, 59, 63, 68, 67, 66, 65, 66, 66],
    'ADN40 (Note)': [53, 59, 59, 60, 53, 67, 58, 67, 65],
    'ADN40 (Video)': [64, 83, 67, 68, 69, 70, 66, 67, 65],
    'A+ (Note)': [76, 83, 80, 78, 84, 74, 73, 75, 72],
    'A+ (Video)': [74, 75, 85, 73, 80, 77, 72, 75, 77],
    'Noticias (Note)': [71, 83, 85, 83, 77, 84, 73, 70, 75],
    'Noticias (Video)': [63, 75, 64, 76, 63, 74, 55, 76, 77],
    'Milenio (Note)': [81, 83, 84, 83, 52, 33, 34, 77, 60],
    'Milenio (Video)': [84, 75, 77, 80, 49, 47, 46, 66, 66],
    'El Heraldo (Note)': [90, 83, 90, 80, 80, 83, 56, 67, 91],
    'El Heraldo (Video)': [89, 81, 87, 82, 51, 49, 52, 59, 92],
    'El Universal (Note)': [55, 81, 87, 56, 34, 34, 34, 47, 47],
    'El Universal (Video)': [45, 34, 34, 30, 30, 29, 25, 46, 46],
    'Televisa (Note)': [71, 35, 34, 35, 53, 34, 34, 47, 59],
    'Televisa (Video)': [38, 50, 51, 48, 48, 47, 47, 48, 50],
    'Terra (Note)': [38, 50, 61, 30, 19, 54, 56, 60, 58],
    'Terra (Video)': [80, 54, 49, 53, 80, 71, 82, 84, 70],
    'AS (Note)': [87, 74, 71, 25, 30, 25, 25, 77, 77],
    'AS (Video)': [89, 82, 87, 56, 37, 39, 41, 58, 90],
    'Infobae (Note)': [70, 31, 61, 58, 66, 63, 70, 59, 47],
    'Infobae (Video)': [72, 45, 49, 48, 47, 48, 49, 50, 50],
    'NY Times (Note)': [60, 33, 44, 47, 41, 54, 50, 59, 59],
    'NY Times (Video)': [36, 45, 44, 48, 47, 54, 41, 40, 40],
}

# Define the colors for each company
# Function to calculate insights for TV Azteca


def calculate_relevant_insights(df_data, companies, title):
    significant_changes = []

    for company in companies:
        initial_value = df_data[company].iloc[0]
        final_value = df_data[company].iloc[-1]
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


def calculate_competition_insights(filtered_df, companies, title):
    significant_changes = []

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
        insight = f"Competition {most_relevant[1]} {most_relevant[2]} by {
            abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = None

    return insight
