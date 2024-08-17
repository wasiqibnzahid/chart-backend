from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats

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

# Calculating averages
tv_azteca_columns = [
    'Azteca UNO (Note)', 'Azteca UNO (Video)', 'Azteca 7 (Note)', 'Azteca 7 (Video)',
    'Deportes (Note)', 'Deportes (Video)', 'ADN40 (Note)', 'ADN40 (Video)',
    'A+ (Note)', 'A+ (Video)', 'Noticias (Note)', 'Noticias (Video)'
]

competition_columns = [
    'Milenio (Note)', 'Milenio (Video)', 'El Heraldo (Note)', 'El Heraldo (Video)',
    'El Universal (Note)', 'El Universal (Video)', 'Televisa (Note)', 'Televisa (Video)',
    'Terra (Note)', 'Terra (Video)', 'AS (Note)', 'AS (Video)',
    'Infobae (Note)', 'Infobae (Video)', 'NY Times (Note)', 'NY Times (Video)'
]

df['TV Azteca Avg'] = df[tv_azteca_columns].mean(axis=1).round(1)
df['Competition Avg'] = df[competition_columns].mean(axis=1).round(1)

df['TV Azteca Note Avg'] = df[[col for col in tv_azteca_columns if 'Note' in col]].mean(axis=1).round(1)
df['Competition Note Avg'] = df[[col for col in competition_columns if 'Note' in col]].mean(axis=1).round(1)

df['TV Azteca Video Avg'] = df[[col for col in tv_azteca_columns if 'Video' in col]].mean(axis=1).round(1)
df['Competition Video Avg'] = df[[col for col in competition_columns if 'Video' in col]].mean(axis=1).round(1)

# Calculate percentage changes and apply formatting
def pct_change(series):
    return series.pct_change().apply(lambda x: f"<span style='color:green;'>▲ {x*100:.1f}%</span>" if x > 0 else f"<span style='color:red;'>▼ {abs(x)*100:.1f}%</span>" if x < 0 else "")

df['TV Azteca Avg Change'] = pct_change(df['TV Azteca Avg'])
df['Competition Avg Change'] = pct_change(df['Competition Avg'])

df['TV Azteca Note Change'] = pct_change(df['TV Azteca Note Avg'])
df['Competition Note Change'] = pct_change(df['Competition Note Avg'])

df['TV Azteca Video Change'] = pct_change(df['TV Azteca Video Avg'])
df['Competition Video Change'] = pct_change(df['Competition Video Avg'])

def add_trendline(x, y, fig, line_name="Trendline", color='blue', ci_fixed=0.75, show_trendline=True):  # Added show_trendline parameter
    if not show_trendline:
        return fig  # If trendline is not to be shown, return the original figure

    # Convert the x-values to numeric indices for regression
    x_indices = np.arange(len(x))

    # Perform linear regression to fit a trendline
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_indices, y)
    trendline = slope * x_indices + intercept

    # Use a smaller fixed confidence interval value
    ci = ci_fixed  # Reduced fixed value for the confidence interval

    upper_bound = trendline + ci
    lower_bound = trendline - ci

    # Add the trendline to the plot
    fig.add_trace(go.Scatter(
        x=x, y=trendline,
        mode='lines',
        name=line_name,
        line=dict(color=color, width=2, dash='dash'),
    ))

    if show_trendline:  # Add the confidence interval only if the trendline is shown
        # Add the confidence interval as a filled area
        fig.add_trace(go.Scatter(
            x=x, y=upper_bound,
            mode='lines',
            name='Upper Bound',
            line=dict(color=color, width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=x, y=lower_bound,
            mode='lines',
            name='Lower Bound',
            fill='tonexty',
            line=dict(color=color, width=0),
            fillcolor='rgba(200,100,250,0.4)',  # Customize the fill color and transparency
            showlegend=False
        ))

    return fig









# Create the main figure
def create_figure(x, y1, y2, y1_name, y2_name, y1_change, y2_change):
    fig = go.Figure()

    # Add the trace for TV Azteca with values and percentage changes
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        mode='lines+markers+text',
        name=y1_name,
        marker=dict(size=10, color='blue'),
        line=dict(color='blue', shape='spline', smoothing=1.3, width=3),  # Adjusted the width to 3
        text=[f"<span style='font-size:10px;'>{c}</span><br><b>{v}</b>" for v, c in zip(y1, y1_change)],
        textposition='top center',
        hoverinfo='text'
    ))

    # Add the trace for Competition with values and percentage changes
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        mode='lines+markers+text',
        name=y2_name,
        marker=dict(size=10, color='orange'),
        line=dict(color='orange', shape='spline', smoothing=1.3, width=3),  # Adjusted the width to 3
        text=[f"<b>{v}</b><br><span style='font-size:10px;'>{c}</span>" for v, c in zip(y2, y2_change)],
        textposition='bottom center',
        hoverinfo='text'
    ))

    # Adding trendlines for both series
    fig = add_trendline(x, y1, fig, line_name=f'{y1_name} Trendline', color='blue')
    fig = add_trendline(x, y2, fig, line_name=f'{y2_name} Trendline', color='green')

    # Creating frames for the animation
    frames = [
        go.Frame(data=[
            go.Scatter(x=x[:k+1], y=y1[:k+1]),
            go.Scatter(x=x[:k+1], y=y2[:k+1])
        ]) for k in range(1, len(x))
    ]

    # Adding animation buttons with slower transition
    fig.update_layout(
        title_text="Benchmark Averages",
        xaxis=dict(title='', showticklabels=True),
        yaxis=dict(title='', showticklabels=True, range=[30, 80]),  # Updated the y-axis range
        showlegend=True,
        transition_duration=1000,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=1.05,
                y=0.05,
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None, dict(frame=dict(duration=2000, redraw=True),
                                          fromcurrent=True,
                                          transition=dict(duration=500, easing='linear'))]),
                    dict(label="Stop",
                         method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False),
                                            mode="immediate",
                                            transition=dict(duration=0))])
                ]
            )
        ]
    )

    fig.frames = frames

    return fig



def create_quarterly_figure(x, y1, y2, y1_name, y2_name, y1_change, y2_change):
    fig = go.Figure()

    # Add the trace for TV Azteca
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        mode='lines+markers+text',
        name=y1_name,
        marker=dict(size=10, color='blue'),  # Updated color
        line=dict(color='blue', shape='spline', smoothing=1.3),  # Updated color
        text=[f"<b>{v:.1f}</b><br><span style='font-size:10px;'>{c}</span>" for v, c in zip(y1, y1_change)],
        textposition='top center',
        hoverinfo='text'
    ))

    # Add the trace for Competition
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        mode='lines+markers+text',
        name=y2_name,
        marker=dict(size=10, color='orange'),  # Updated color
        line=dict(color='orange', shape='spline', smoothing=1.3),  # Updated color
        text=[f"<b>{v:.1f}</b><br><span style='font-size:10px;'>{c}</span>" for v, c in zip(y2, y2_change)],
        textposition='bottom center',
        hoverinfo='text'
    ))

    fig.update_layout(
        title_text="Quarterly Benchmark Averages",
        xaxis=dict(title='Quarter', showticklabels=True),
        yaxis=dict(title='Average', showticklabels=True, range=[0, 100]),
        showlegend=True
    )

    return fig

# Calculating quarterly averages
def calculate_quarterly_averages(df, tv_azteca_columns, competition_columns):
    num_weeks = len(df)
    quarters = []
    for i in range(0, num_weeks, 13):
        quarter_df = df.iloc[i:i+13]
        tv_azteca_avg = quarter_df[tv_azteca_columns].mean(axis=1).mean().round(1)
        competition_avg = quarter_df[competition_columns].mean(axis=1).mean().round(1)
        if i == 0:
            tv_azteca_change = ""
            competition_change = ""
        else:
            prev_quarter_df = df.iloc[i-13:i]
            prev_tv_azteca_avg = prev_quarter_df[tv_azteca_columns].mean(axis=1).mean()
            prev_competition_avg = prev_quarter_df[competition_columns].mean(axis=1).mean()
            tv_azteca_change = f"<span style='color:green;'>▲ {(tv_azteca_avg - prev_tv_azteca_avg)/prev_tv_azteca_avg*100:.1f}%</span>" if tv_azteca_avg > prev_tv_azteca_avg else f"<span style='color:red;'>▼ {(prev_tv_azteca_avg - tv_azteca_avg)/prev_tv_azteca_avg*100:.1f}%</span>"
            competition_change = f"<span style='color:green;'>▲ {(competition_avg - prev_competition_avg)/prev_competition_avg*100:.1f}%</span>" if competition_avg > prev_competition_avg else f"<span style='color:red;'>▼ {(prev_competition_avg - competition_avg)/prev_competition_avg*100:.1f}%</span>"
        quarters.append({
            'Date': f'Q{i//13 + 1}',
            'TV Azteca Avg': tv_azteca_avg,
            'Competition Avg': competition_avg,
            'TV Azteca Change': tv_azteca_change,
            'Competition Change': competition_change
        })
    return pd.DataFrame(quarters)

quarterly_df = calculate_quarterly_averages(df, tv_azteca_columns, competition_columns)

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Benchmark Averages"),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Weekly Averages', value='tab-1'),
        dcc.Tab(label='Quarterly Averages', value='tab-2'),
    ]),
    dcc.Dropdown(
        id='graph-dropdown',
        options=[
            {'label': 'General Averages (Nota and Video)', 'value': 'general'},
            {'label': 'Promedio de la Nota TVA', 'value': 'nota'},
            {'label': 'Promedio de Video', 'value': 'video'}
        ],
        value='general'
    ),
    html.Div(id='tabs-content')
])

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('graph-dropdown', 'value')
)
def render_content(tab, selected_value):
    if tab == 'tab-1':
        return html.Div([
            dcc.RangeSlider(
    id='year-slider',
    min=0,
    max=39,  # This keeps the full range as before
    value=[13, 39],  # Default range remains the same
    marks={
        0: {'label': 'Q1 2024', 'style': {'visibility': 'visible'}},
        13: {'label': 'Q2 2024', 'style': {'visibility': 'visible'}},
        26: {'label': 'Q3 2024', 'style': {'visibility': 'visible'}},
        39: {'label': 'Q4 2024', 'style': {'visibility': 'visible'}}
    },
    step=1,  # This allows the slider to move freely to any point
    allowCross=True
            ),
            dcc.Graph(id='graph-output')
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(id='quarterly-graph-output')
        ])

# Additional callbacks to update graphs, etc.
@app.callback(
    Output('graph-output', 'figure'),
    [Input('graph-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_value, selected_range):
    # Dynamically slice the dataframe based on selected range
    filtered_df = df.iloc[selected_range[0]:selected_range[1] + 1]

    if selected_value == 'general':
        return create_figure(
            filtered_df['Date'], filtered_df['TV Azteca Avg'], filtered_df['Competition Avg'],
            'TV Azteca Avg', 'Competition Avg',
            filtered_df['TV Azteca Avg Change'], filtered_df['Competition Avg Change']
        )
    elif selected_value == 'nota':
        return create_figure(
            filtered_df['Date'], filtered_df['TV Azteca Note Avg'], filtered_df['Competition Note Avg'],
            'TV Azteca Note Avg', 'Competition Note Avg',
            filtered_df['TV Azteca Note Change'], filtered_df['Competition Note Change']
        )
    elif selected_value == 'video':
        return create_figure(
            filtered_df['Date'], filtered_df['TV Azteca Video Avg'], filtered_df['Competition Video Avg'],
            'TV Azteca Video Avg', 'Competition Video Avg',
            filtered_df['TV Azteca Video Change'], filtered_df['Competition Video Change']
        )

@app.callback(
    Output('quarterly-graph-output', 'figure'),
    Input('graph-dropdown', 'value')
)
def update_quarterly_graph(selected_value):
    if selected_value == 'general':
        return create_quarterly_figure(
            quarterly_df['Date'], quarterly_df['TV Azteca Avg'], quarterly_df['Competition Avg'],
            'TV Azteca Avg', 'Competition Avg',
            quarterly_df['TV Azteca Change'], quarterly_df['Competition Change']
        )
    elif selected_value == 'nota':
        nota_quarterly_df = calculate_quarterly_averages(df, [col for col in tv_azteca_columns if 'Note' in col], [col for col in competition_columns if 'Note' in col])
        return create_quarterly_figure(
            nota_quarterly_df['Date'], nota_quarterly_df['TV Azteca Avg'], nota_quarterly_df['Competition Avg'],
            'TV Azteca Note Avg', 'Competition Note Avg',
            nota_quarterly_df['TV Azteca Change'], nota_quarterly_df['Competition Change']
        )
    elif selected_value == 'video':
        video_quarterly_df = calculate_quarterly_averages(df, [col for col in tv_azteca_columns if 'Video' in col], [col for col in competition_columns if 'Video' in col])
        return create_quarterly_figure(
            video_quarterly_df['Date'], video_quarterly_df['TV Azteca Avg'], video_quarterly_df['Competition Avg'],
            'TV Azteca Video Avg', 'Competition Video Avg',
            video_quarterly_df['TV Azteca Change'], video_quarterly_df['Competition Change']
        )

if __name__ == '__main__':
    app.run_server(debug=True)