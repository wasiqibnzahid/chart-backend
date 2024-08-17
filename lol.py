from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go

# Assuming you have the data already prepared as shown before
# This includes df and quarterly_df (for the new page)

# Helper function to create the bar charts
def create_bar_chart(df, columns, yaxis_range=[0, 100], title=""):
    fig = go.Figure()

    for column in columns:
        fig.add_trace(go.Bar(
            x=df['Date'],
            y=df[column],
            name=column,
            marker=dict(line=dict(color='rgb(248, 248, 249)', width=1.5)),
            text=df[column],
            textposition='auto',
        ))

    fig.update_layout(
        barmode='stack',
        title=title,
        yaxis=dict(range=yaxis_range),
        xaxis=dict(tickangle=-45),
        hovermode="x",
    )

    return fig

# Tv Azteca vs Competition subsection
def create_azteca_vs_competition():
    return html.Div([
        dcc.Tabs(id="azteca-vs-competition-tabs", value='nota', children=[
            dcc.Tab(label='Nota', value='nota'),
            dcc.Tab(label='Video', value='video'),
        ]),
        html.Div(id='azteca-vs-competition-content')
    ])

# Tv Azteca subsection
def create_tv_azteca():
    return html.Div([
        dcc.Tabs(id="tv-azteca-tabs", value='nota', children=[
            dcc.Tab(label='Nota', value='nota'),
            dcc.Tab(label='Video', value='video'),
        ]),
        html.Div(id='tv-azteca-content')
    ])

# Main layout
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

# Callbacks for the Azteca vs Competition section
@app.callback(
    Output('azteca-vs-competition-content', 'children'),
    Input('azteca-vs-competition-tabs', 'value')
)
def update_azteca_vs_competition_content(tab):
    if tab == 'nota':
        fig = create_bar_chart(quarterly_df, [col for col in df.columns if 'Note' in col], title="Azteca vs Competition - Nota")
    elif tab == 'video':
        fig = create_bar_chart(quarterly_df, [col for col in df.columns if 'Video' in col], title="Azteca vs Competition - Video")

    return dcc.Graph(figure=fig)

# Callbacks for the Tv Azteca section
@app.callback(
    Output('tv-azteca-content', 'children'),
    Input('tv-azteca-tabs', 'value')
)
def update_tv_azteca_content(tab):
    azteca_columns = ['Azteca UNO (Note)', 'Azteca UNO (Video)', 'Azteca 7 (Note)', 'Azteca 7 (Video)', 
                      'Deportes (Note)', 'Deportes (Video)', 'ADN40 (Note)', 'ADN40 (Video)', 
                      'A+ (Note)', 'A+ (Video)', 'Noticias (Note)', 'Noticias (Video)']

    if tab == 'nota':
        fig = create_bar_chart(quarterly_df, [col for col in azteca_columns if 'Note' in col], title="Tv Azteca - Nota")
    elif tab == 'video':
        fig = create_bar_chart(quarterly_df, [col for col in azteca_columns if 'Video' in col], title="Tv Azteca - Video")

    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
