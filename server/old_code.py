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
df = pd.DataFrame(data)

# Define the colors for each company
company_colors = {
    'Azteca UNO (Note)': '#8DA1E3',
    'Azteca UNO (Video)': '#8DA1E3',
    'Azteca 7 (Note)': '#A8D5BA',
    'Azteca 7 (Video)': '#A8D5BA',
    'Deportes (Note)': '#CDA1D1',
    'Deportes (Video)': '#CDA1D1',
    'ADN40 (Note)': '#C2A476',
    'ADN40 (Video)': '#C2A476',
    'A+ (Note)': '#ACE6E6',
    'A+ (Video)': '#ACE6E6',
    'Noticias (Note)': '#D0E1C3',
    'Noticias (Video)': '#D0E1C3',
    'Milenio (Note)': '#BCC1AE',
    'Milenio (Video)': '#BCC1AE',
    'El Heraldo (Note)': '#D3D3D3',
    'El Heraldo (Video)': '#D3D3D3',
    'El Universal (Note)': '#D0E1C3',
    'El Universal (Video)': '#D0E1C3',
    'Televisa (Note)': '#FFB266',
    'Televisa (Video)': '#FFB266',
    'Terra (Note)': '#ACE6E6',
    'Terra (Video)': '#ACE6E6',
    'AS (Note)': '#FFFACD',
    'AS (Video)': '#FFFACD',
    'Infobae (Note)': '#A7D8DE',
    'Infobae (Video)': '#A7D8DE',
    'NY Times (Note)': '#FF9999',
    'NY Times (Video)': '#FF9999'
}

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


def create_insights_section(filtered_df, azteca_companies, competition_companies, title):
    azteca_insights = calculate_relevant_insights(
        filtered_df, azteca_companies, title)
    competition_insights = calculate_competition_insights(
        filtered_df, competition_companies, title) if competition_companies else None

    insights = [
        html.H4(f"Summary and Insights: {title}"),
        html.P(f"TV Azteca: {azteca_insights}")
    ]

    if competition_insights:
        insights.append(html.P(f"Competition: {competition_insights}"))

    return html.Div(insights)


# Create grouped bar chart
def create_grouped_bar_chart(df, companies, yaxis_range=[0, 100], title="", num_weeks=None):
    fig = go.Figure()

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

    x_positions = []
    bar_width = 0.8  # Adjust based on the width of each bar

    for i, company in enumerate(companies):
        display_name = label_mapping.get(company, company.split()[0])
        combined_labels = [f"{display_name} ({date})" for date in df['Date']]

        changes = df[company].diff().fillna(0)
        arrows = [
            f'<span style="color:green;">▲</span>' if change > 0 else
            f'<span style="color:red;">▼</span>' if change < 0 else '-'
            for change in changes
        ]

        # Determine text based on number of weeks
        if num_weeks and num_weeks > 5:
            text_with_arrows = [f'<b>{value}</b>' for value in df[company]]
        else:
            text_with_arrows = [
                f'{arrow}<br><b>{value}</b>'
                for value, arrow in zip(df[company], arrows)
            ]

        fig.add_trace(go.Bar(
            x=combined_labels,
            y=df[company],
            name=display_name,
            text=text_with_arrows,
            textposition='outside',  # This is where you add the textposition parameter
            textfont_size=12,  # Adjust the font size as needed
            marker_color=company_colors.get(company, 'grey')
        ))

        # Collect the x position for adding separator lines between companies
        if i < len(companies) - 1:
            x_positions.append((i + 1) * len(df['Date']) - 0.5)

    tickvals = [(i + 0.5) * len(df['Date']) for i in range(len(companies))]
    ticktext = [label_mapping.get(company, company.split()[0])
                for company in companies]

    # Adding vertical separator lines between companies
    for pos in x_positions:
        fig.add_shape(
            type="line",
            x0=pos, x1=pos,
            y0=yaxis_range[0], y1=yaxis_range[1],
            line=dict(color="grey", width=1)
        )

    fig.update_layout(
        barmode='group',
        title=title,
        yaxis=dict(range=yaxis_range),
        xaxis=dict(
            tickangle=0,
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            tickfont=dict(size=13, family="Arial", color="black",
                          weight="bold"),  # Updated font size and weight
            ticks='outside'
        ),
        hovermode="x",
        showlegend=False
    )

    return fig


# Create insights section
def create_insights_section(filtered_df, azteca_companies, competition_companies, title):
    azteca_insights = calculate_relevant_insights(
        filtered_df, azteca_companies, title)
    competition_insights = calculate_competition_insights(
        filtered_df, competition_companies, title)
    return html.Div([
        html.H4(f"Summary and Insights: {title}"),
        html.P(f"TV Azteca: {azteca_insights}"),
        html.P(f"Competition: {competition_insights}")
    ])

# Create the layout for the tabs


def create_azteca_vs_competition():
    marks = {i: df['Date'][i] for i in range(0, len(df), 4)}

    return html.Div([
        dcc.Tabs(id="azteca-vs-competition-tabs", value='nota', children=[
            dcc.Tab(label='Nota', value='nota'),
            dcc.Tab(label='Video', value='video'),
        ]),
        html.Div(id='azteca-vs-competition-content'),
        dcc.RangeSlider(
            id='week-slider',
            min=0,
            max=len(df) - 1,
            value=[0, len(df) - 1],
            marks=marks,
            step=1  # Allow the slider to move in increments of 1 week
        ),
        html.Div(id='azteca-vs-competition-insights')
    ])


def create_tv_azteca():
    marks = {i: df['Date'][i] for i in range(0, len(df), 4)}

    return html.Div([
        dcc.Tabs(id="tv-azteca-tabs", value='nota', children=[
            dcc.Tab(label='Nota', value='nota'),
            dcc.Tab(label='Video', value='video'),
        ]),
        html.Div(id='tv-azteca-content'),
        dcc.RangeSlider(
            id='azteca-week-slider',
            min=0,
            max=len(df) - 1,
            value=[0, len(df) - 1],
            marks=marks,
            step=1  # Allow the slider to move in increments of 1 week
        ),
        html.Div(id='tv-azteca-insights')
    ])


app = Dash(__name__)

app.layout = html.Div([
    html.H2("General Benchmarks"),
    dcc.Tabs(id="general-benchmarks-tabs", value='tv-azteca-vs-competition', children=[
        dcc.Tab(label='Tv Azteca vs Competition',
                value='tv-azteca-vs-competition'),
        dcc.Tab(label='Tv Azteca', value='tv-azteca'),
    ]),
    html.Div(id='general-benchmarks-content')
])


@app.callback(
    Output('general-benchmarks-content', 'children'),
    Input('general-benchmarks-tabs', 'value')
)
def render_general_benchmarks_content(tab):
    if tab == 'tv-azteca-vs-competition':
        return create_azteca_vs_competition()
    elif tab == 'tv-azteca':
        return create_tv_azteca()


@app.callback(
    [Output('azteca-vs-competition-content', 'children'),
     Output('azteca-vs-competition-insights', 'children')],
    [Input('azteca-vs-competition-tabs', 'value'),
     Input('week-slider', 'value')]
)
def update_azteca_vs_competition_content(tab, week_range):
    filtered_df = df.iloc[week_range[0]:week_range[1] + 1]

    if tab == 'nota':
        azteca_companies = [
            col for col in df.columns if 'Note' in col and 'Azteca' in col]
        competition_companies = [
            col for col in df.columns if 'Note' in col and 'Azteca' not in col]
        fig = create_grouped_bar_chart(
            filtered_df, azteca_companies + competition_companies, title="Azteca vs Competition - Nota")
        insights = create_insights_section(
            filtered_df, azteca_companies, competition_companies, "TV Azteca vs Competition (Nota)")
    elif tab == 'video':
        azteca_companies = [
            col for col in df.columns if 'Video' in col and 'Azteca' in col]
        competition_companies = [
            col for col in df.columns if 'Video' in col and 'Azteca' not in col]
        fig = create_grouped_bar_chart(
            filtered_df, azteca_companies + competition_companies, title="Azteca vs Competition - Video")
        insights = create_insights_section(
            filtered_df, azteca_companies, competition_companies, "TV Azteca vs Competition (Video)")

    return dcc.Graph(figure=fig), insights


@app.callback(
    [Output('tv-azteca-content', 'children'),
     Output('tv-azteca-insights', 'children')],
    [Input('tv-azteca-tabs', 'value'),
     Input('azteca-week-slider', 'value')]
)
def update_tv_azteca_content(tab, week_range):
    filtered_df = df.iloc[week_range[0]:week_range[1] + 1]

    azteca_columns = ['Azteca UNO (Note)', 'Azteca UNO (Video)', 'Azteca 7 (Note)', 'Azteca 7 (Video)',
                      'Deportes (Note)', 'Deportes (Video)', 'ADN40 (Note)', 'ADN40 (Video)',
                      'A+ (Note)', 'A+ (Video)', 'Noticias (Note)', 'Noticias (Video)']

    if tab == 'nota':
        fig = create_grouped_bar_chart(filtered_df, [
                                       col for col in azteca_columns if 'Note' in col], title="Tv Azteca - Nota")
        insights = create_insights_section(filtered_df, [
                                           col for col in azteca_columns if 'Note' in col], [], "TV Azteca (Nota)")
    elif tab == 'video':
        fig = create_grouped_bar_chart(filtered_df, [
                                       col for col in azteca_columns if 'Video' in col], title="Tv Azteca - Video")
        insights = create_insights_section(filtered_df, [
                                           col for col in azteca_columns if 'Video' in col], [], "TV Azteca (Video)")

    return dcc.Graph(figure=fig), insights


if __name__ == '__main__':
    app.run_server(debug=True)
