"""EMNOT: Evaluate Metadata Normalization to Ontology Terms"""

from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import json

# App instamce
app = Dash(
#    name=__name__,
#    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

def str_to_list(s):
    if s is None: return None
    if s == '[]': return []
    parts = s.strip('[]').split(', ')
    return [p.strip('\'"') for p in parts]

# Load data for grid
df = pd.read_csv('data/method_comparisons.csv').rename(columns=lambda s: s.replace('.','_'))
for i, col in enumerate(df.columns):
    if i < 1:
        continue
    df.loc[~df[col].isna(), col] = df.loc[~df[col].isna(), col].apply(str_to_list)

# Dash grid
grid = dag.AgGrid(
    id="main-grid",
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i, "filter": True} for i in df.columns],
    dashGridOptions={
        'rowSelection': {'mode': 'single'}
    }
)

def subgrid_updater(col):
    def update_subgrid(selection):
        if selection:
            s = selection[0]
            if s[col] is None: return []
            return [{col: x} for x in s[col]]
        return no_update
    return update_subgrid

def make_detail_cards():

    sub_grids = []

    for i, col in enumerate(df.columns):
        # To-do: make this content based
        if i == 0: continue

        sub_grid_id = f"column-{i}-detailed-grid"

        sub_grids.append(
            dag.AgGrid(
                id=sub_grid_id,
                rowData=[],
                columnDefs=[{"field": col}]
            )
        )

        callback(
            Output(sub_grid_id, "rowData"),
            Input("main-grid", "selectedRows")
        )(subgrid_updater(col))
        

    return [
        html.Div(
            # set a class? will explicitly set style for now
            style={
                'float': 'left',
                'width': '350px'
            },
            children=[sub_grid]
        )
        for sub_grid in sub_grids
    ]
        

# Layout
app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            children=[
                html.H1(children='Evaluate Metadata Normalization to Ontology Terms', style={'textAlign':'center'}),
            ]
        ),
        # Top panel
        html.Div(
            children=[grid]
        ),
        # Detailed panels
        html.Div(children=make_detail_cards())
    ]
)

# Script entry
if __name__ == '__main__':
    app.run(debug=True)
