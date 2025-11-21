"""EMNOT: Evaluate Metadata Normalization to Ontology Terms"""

import ast
import json
from collections.abc import Mapping, Collection

from dash import Dash, html, dcc, callback, Output, Input, no_update
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

#import plotly.express as px

import pandas as pd

# App instamce
app = Dash(
#    name=__name__,
#    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

# Load data for grid
df = pd.read_csv('data/method_comparisons.csv', nrows=200000).rename(columns=lambda s: s.replace('.','_'))

# Dash grid
grid = dag.AgGrid(
    id="main-grid",
    rowData=df.to_dict("records"),
    columnDefs=[{"field": i, "filter": True, 'cellDataType': 'text'} for i in df.columns],
    dashGridOptions={
        'rowSelection': {'mode': 'single'}
    }
)

def subgrid_updater(col):
    def update_subgrid(selection):
        if selection:
            content_obj = selection[0][col]
            if content_obj is None: return []
            
            try:
                content_obj = ast.literal_eval(content_obj)
            except:
                print(f'Did not parse "{content_obj}"')
            
            if isinstance(content_obj, Mapping):
                #print(f'{col} is a mapping')
                return [{'key': k, 'value': v} for k, v in content_obj.items()]
            if isinstance(content_obj, Collection):
                #print(f'{col} is a collection')
                return [{'value': v} for v in content_obj]
            #print(f'{col} is something else')
            return [{'value': content_obj}] # Fallback, do we need?
        return no_update
    return update_subgrid

def make_detail_cards():

    elements = []

    for i, col in enumerate(df.columns):
        # To-do: make this content based
        if i == 0: continue

        sub_grid_id = f"column-{i}-detailed-grid"

        sub_grid = dag.AgGrid(
            id=sub_grid_id,
            rowData=[],
            columnDefs=[{"field": "key"}, {"field": "value"}],
            defaultColDef={
                'resizable': True,
                'cellStyle': {'wordBreak': 'normal'},
                'wrapText': True,
                'autoHeight': True
            },
            dashGridOptions = {'enableCellTextSelection': True, 'ensureDomOrder': True},
            # Order of colIDs here will change display order
            columnState=[{'colId': 'key'}, {'colId': 'value', 'sort': 'asc'}]
        )

        callback(
            Output(sub_grid_id, "rowData"),
            Input("main-grid", "selectedRows")
        )(subgrid_updater(col))
        
        elements.append({
            'title': col,
            'grid': sub_grid
        })

    return elements
        

# Layout
app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(
                    html.I(className='bi bi-github'),
                    href='https://github.com/sverchkov/emnot'
                ))
            ],
            brand='Evaluate Metadata Normalization to Ontology Terms'
        ),
        # Top panel
        html.Div(
            children=[grid]
        ),
        # Detailed panels
        html.Div(children=[
            dbc.Card(
                children=[
                    html.H5(card_content['title'], className='card-title'),
                    card_content['grid']
                ],
                body=True
            )
            for card_content in make_detail_cards()
        ])
    ]
)

# Script entry
if __name__ == '__main__':
    app.run(debug=True)
