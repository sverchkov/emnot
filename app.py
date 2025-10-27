"""EMNOT: Evaluate Metadata Normalization to Ontology Terms"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Static data loading
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# App instamce
app = Dash(
#    name=__name__,
#    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Layout
app.layout = html.Div(
    id="app-container",
    children=[
        # Left panel
        html.Div(
            id="left-column",
            children=[
                html.H1(children='Evaluate Metadata Normalization to Ontology Terms', style={'textAlign':'center'}),
                dcc.Dropdown([], placeholder='Terms to filter by', id='dropdown-filter1'),
                dcc.Dropdown([], placeholder='Terms to filter by', id='dropdown-filter2'),
                dcc.Dropdown(
                    df.country.drop_duplicates(),
                    placeholder='Select sample',
                    closeOnSelect=False,
                    id='dropdown-selection'
                )
            ]
        ),
        # Right panel
        html.Div(
            id="right-column",
            children=[
                html.Div(),
                html.Div(),
                html.Div(),
                dcc.Graph(id='graph-content')
            ]
        )
    ]
)

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

# Server side
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

# Script entry
if __name__ == '__main__':
    app.run(debug=True)
