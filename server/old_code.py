from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Data setup
data = {
    'Date': [],
    'Azteca UNO (Note)': [],
    'Azteca UNO (Video)': [],
    'Azteca 7 (Note)': [],
    'Azteca 7 (Video)': [],
    'Deportes (Note)': [],
    'Deportes (Video)': [],
    'ADN40 (Note)': [],
    'ADN40 (Video)': [],
    'A+ (Note)': [],
    'A+ (Video)': [],
    'Noticias (Note)': [],
    'Noticias (Video)': [],
    'Milenio (Note)': [],
    'Milenio (Video)': [],
    'El Heraldo (Note)': [],
    'El Heraldo (Video)': [],
    'El Universal (Note)': [],
    'El Universal (Video)': [],
    'Televisa (Note)': [],
    'Televisa (Video)': [],
    'Terra (Note)': [],
    'Terra (Video)': [],
    'AS (Note)': [],
    'AS (Video)': [],
    'Infobae (Note)': [],
    'Infobae (Video)': [],
    'NY Times (Note)': [],
    'NY Times (Video)': [],
}
df = pd.DataFrame(data)

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
