from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Data setup
data = {
    'Date': [
        '17-Jun4', '24-Jun4', '01-Jul4', '08-Jul4', '15-Jul4', 
        '22-Jul4', '29-Jul4', '05-Aug4', '12-Aug4', '19-Aug4', 
        '26-Aug4', '02-Sep4', '09-Sep4', '16-Sep4', '23-Sep4',
        '30-Sep4', '07-Oct4', '14-Oct4', '21-Oct4', '28-Oct4', 
        '04-Nov4', '11-Nov4', '18-Nov4', '25-Nov4', '02-Dec4', 
        '09-Dec4', '16-Dec4', '23-Dec4', '31-Dec4'
    ],
    'Azteca UNO (Note)': [78, 74, 77, 78, 61, 64, 70, 72, 71, 69, 68, 72, 73, 75, 74, 75, 74, 72, 73, 70, 71, 69, 70, 67, 73, 71, 70, 68, 72],
    'Azteca UNO (Video)': [63, 81, 79, 76, 67, 66, 74, 73, 75, 74, 73, 71, 70, 72, 74, 72, 70, 71, 69, 72, 73, 71, 72, 70, 74, 73, 72, 71, 73],
    'Azteca 7 (Note)': [63, 64, 64, 63, 67, 68, 72, 71, 70, 69, 67, 66, 65, 67, 70, 69, 68, 67, 66, 69, 70, 68, 69, 67, 68, 67, 66, 65, 67],
    'Azteca 7 (Video)': [59, 80, 65, 65, 72, 73, 74, 73, 72, 71, 70, 69, 68, 70, 71, 70, 69, 68, 67, 70, 71, 69, 70, 68, 71, 70, 69, 68, 70],
    'Deportes (Note)': [64, 61, 60, 64, 66, 65, 73, 72, 71, 70, 69, 67, 66, 68, 70, 69, 68, 67, 66, 68, 70, 68, 69, 67, 69, 68, 67, 66, 68],
    'Deportes (Video)': [53, 59, 64, 60, 58, 60, 74, 73, 72, 71, 70, 69, 67, 68, 70, 69, 68, 67, 66, 69, 70, 68, 69, 67, 70, 69, 68, 67, 69],
    'ADN40 (Note)': [64, 83, 59, 68, 66, 67, 71, 70, 69, 68, 67, 66, 65, 67, 69, 68, 67, 66, 65, 67, 69, 67, 68, 66, 67, 66, 65, 64, 66],
    'ADN40 (Video)': [53, 54, 67, 70, 66, 68, 74, 73, 72, 71, 70, 69, 68, 67, 69, 68, 67, 66, 65, 68, 69, 67, 68, 66, 68, 67, 66, 65, 67],
    'A+ (Note)': [76, 75, 80, 78, 72, 74, 73, 72, 71, 70, 69, 67, 66, 68, 71, 70, 69, 68, 67, 70, 71, 69, 70, 68, 70, 69, 68, 67, 69],
    'A+ (Video)': [64, 83, 85, 84, 75, 77, 74, 73, 72, 71, 70, 69, 67, 68, 70, 69, 68, 67, 66, 69, 70, 68, 69, 67, 69, 68, 67, 66, 68],
    'Noticias (Note)': [71, 63, 64, 64, 63, 65, 72, 71, 70, 69, 68, 67, 66, 67, 70, 69, 68, 67, 66, 69, 70, 68, 69, 67, 68, 67, 66, 65, 67],
    'Noticias (Video)': [63, 75, 77, 78, 83, 82, 74, 73, 72, 71, 70, 69, 68, 69, 71, 70, 69, 68, 67, 70, 71, 69, 70, 68, 71, 70, 69, 68, 70],
    'Milenio (Note)': [81, 83, 64, 84, 82, 80, 50, 49, 48, 47, 46, 45, 44, 45, 47, 46, 45, 44, 43, 45, 47, 45, 46, 44, 46, 45, 44, 43, 45],
    'Milenio (Video)': [65, 54, 80, 46, 49, 47, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'El Heraldo (Note)': [90, 83, 87, 80, 80, 82, 53, 52, 51, 50, 49, 48, 47, 48, 50, 49, 48, 47, 46, 48, 50, 48, 49, 47, 49, 48, 47, 46, 48],
    'El Heraldo (Video)': [89, 81, 34, 81, 81, 83, 55, 54, 53, 52, 51, 50, 49, 50, 52, 51, 50, 49, 48, 50, 52, 50, 51, 49, 51, 50, 49, 48, 50],
    'El Universal (Note)': [55, 34, 45, 56, 34, 36, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'El Universal (Video)': [45, 35, 50, 30, 30, 32, 54, 53, 52, 51, 50, 49, 48, 49, 51, 50, 49, 48, 47, 49, 51, 49, 50, 48, 50, 49, 48, 47, 49],
    'Televisa (Note)': [71, 50, 84, 56, 53, 55, 50, 49, 48, 47, 46, 45, 44, 45, 47, 46, 45, 44, 43, 45, 47, 45, 46, 44, 46, 45, 44, 43, 45],
    'Televisa (Video)': [38, 54, 82, 30, 30, 32, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'Terra (Note)': [87, 84, 71, 53, 45, 47, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'Terra (Video)': [89, 74, 61, 26, 25, 27, 54, 53, 52, 51, 50, 49, 48, 49, 51, 50, 49, 48, 47, 49, 51, 49, 50, 48, 50, 49, 48, 47, 49],
    'AS (Note)': [70, 82, 49, 35, 45, 47, 50, 49, 48, 47, 46, 45, 44, 45, 47, 46, 45, 44, 43, 45, 47, 45, 46, 44, 46, 45, 44, 43, 45],
    'AS (Video)': [72, 31, 51, 26, 55, 57, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'Infobae (Note)': [60, 45, 44, 35, 25, 27, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47],
    'Infobae (Video)': [45, 33, 30, 53, 45, 47, 54, 53, 52, 51, 50, 49, 48, 49, 51, 50, 49, 48, 47, 49, 51, 49, 50, 48, 50, 49, 48, 47, 49],
    'NY Times (Note)': [36, 45, 45, 37, 25, 27, 50, 49, 48, 47, 46, 45, 44, 45, 47, 46, 45, 44, 43, 45, 47, 45, 46, 44, 46, 45, 44, 43, 45],
    'NY Times (Video)': [25, 25, 25, 25, 25, 27, 52, 51, 50, 49, 48, 47, 46, 47, 49, 48, 47, 46, 45, 47, 49, 47, 48, 46, 48, 47, 46, 45, 47]
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
        percentage_change = ((final_value - initial_value) / initial_value) * 100

        if abs(percentage_change) >= 5:  
            if abs(percentage_change) < 10:
                change_description = "mildly"
            elif abs(percentage_change) < 20:
                change_description = "moderately"
            else:
                change_description = "significantly"
            
            change_type = "decreased" if percentage_change < 0 else "increased"
            significant_changes.append((company, change_type, change_description, percentage_change))

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"TV Azteca {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = "No significant changes were observed across the TV Azteca companies."

    return insight

def calculate_competition_insights(filtered_df, companies, title):
    significant_changes = []

    for company in companies:
        initial_value = filtered_df[company].iloc[0]
        final_value = filtered_df[company].iloc[-1]
        percentage_change = ((final_value - initial_value) / initial_value) * 100

        if abs(percentage_change) >= 5:
            if abs(percentage_change) < 10:
                change_description = "mildly"
            elif abs(percentage_change) < 20:
                change_description = "moderately"
            else:
                change_description = "significantly"
            
            change_type = "decreased" if percentage_change < 0 else "increased"
            significant_changes.append((company, change_type, change_description, percentage_change))

    if significant_changes:
        most_relevant = max(significant_changes, key=lambda x: abs(x[3]))
        insight = f"Competition {most_relevant[1]} {most_relevant[2]} by {abs(most_relevant[3]):.1f}%, especially in {most_relevant[0]}."
    else:
        insight = None

    return insight

def create_insights_section(filtered_df, azteca_companies, competition_companies, title):
    azteca_insights = calculate_relevant_insights(filtered_df, azteca_companies, title)
    competition_insights = calculate_competition_insights(filtered_df, competition_companies, title) if competition_companies else None

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
    ticktext = [label_mapping.get(company, company.split()[0]) for company in companies]

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
        tickfont=dict(size=13, family="Arial", color="black", weight="bold"),  # Updated font size and weight
        ticks='outside'
    ),
    hovermode="x",
    showlegend=False
)


    return fig



# Create insights section
def create_insights_section(filtered_df, azteca_companies, competition_companies, title):
    azteca_insights = calculate_relevant_insights(filtered_df, azteca_companies, title)
    competition_insights = calculate_competition_insights(filtered_df, competition_companies, title)
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
        dcc.Tab(label='Tv Azteca vs Competition', value='tv-azteca-vs-competition'),
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
        azteca_companies = [col for col in df.columns if 'Note' in col and 'Azteca' in col]
        competition_companies = [col for col in df.columns if 'Note' in col and 'Azteca' not in col]
        fig = create_grouped_bar_chart(filtered_df, azteca_companies + competition_companies, title="Azteca vs Competition - Nota")
        insights = create_insights_section(filtered_df, azteca_companies, competition_companies, "TV Azteca vs Competition (Nota)")
    elif tab == 'video':
        azteca_companies = [col for col in df.columns if 'Video' in col and 'Azteca' in col]
        competition_companies = [col for col in df.columns if 'Video' in col and 'Azteca' not in col]
        fig = create_grouped_bar_chart(filtered_df, azteca_companies + competition_companies, title="Azteca vs Competition - Video")
        insights = create_insights_section(filtered_df, azteca_companies, competition_companies, "TV Azteca vs Competition (Video)")

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
        fig = create_grouped_bar_chart(filtered_df, [col for col in azteca_columns if 'Note' in col], title="Tv Azteca - Nota")
        insights = create_insights_section(filtered_df, [col for col in azteca_columns if 'Note' in col], [], "TV Azteca (Nota)")
    elif tab == 'video':
        fig = create_grouped_bar_chart(filtered_df, [col for col in azteca_columns if 'Video' in col], title="Tv Azteca - Video")
        insights = create_insights_section(filtered_df, [col for col in azteca_columns if 'Video' in col], [], "TV Azteca (Video)")

    return dcc.Graph(figure=fig), insights

if __name__ == '__main__':
    app.run_server(debug=True)