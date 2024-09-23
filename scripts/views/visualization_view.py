from dash import dcc, html,dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_cytoscape as cyto
cyto.load_extra_layouts()
from dash.exceptions import PreventUpdate

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from maindash import app, type_storage
from views.visu_co_occu import layout_co_occurence_networks
from views.visu_features import layout_features_selection
from views.visu_perfor import layout_performance_metrics

def layout_visualization():
    return html.Div([
            #html.H3('Visualization Page'),
            dcc.Store(id='legend-store', data=[],storage_type=type_storage),
            dcc.Store(id='tab-status', storage_type=type_storage),
            dcc.Tabs(id="subtabs", value='subtab-cooccurrence',style={'margin-bottom': '20px','display':'none'},persistence=True,persistence_type=type_storage, children=[
                dcc.Tab(label='Co-occurrence networks', value='subtab-cooccurrence'),
                dcc.Tab(label='Features Selection', value='subtab-features-selection'),
                dcc.Tab(label='Performance metrics', value='subtab-performance')
            ]),
            html.Div(id='subtabs-content'),
        ])

@app.callback(Output('subtabs-content', 'children'),
              Output('subtabs', 'style'),
              [Input('subtabs', 'value'),
               State("legend-store",'data'),
               State('subtabs', 'style'),
               State("info-current-file-store",'data'),
               Input("status-run-model","modified_timestamp"),
               State("status-run-model","data"),
               State("status-sliders-co-occurence","data"),
               State("status-sliders-features-selection","data"),
               State("status-legend-covariates","data")])
def render_subcontent(subtab,legend_store,subtabs_style,info_current_file_store,ts,status_run_model,values_co_occurence,values_features_selection,legend_covariates):

    ctx = callback_context

    if not ctx.triggered:
        trigger = 'No input has triggered yet'
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if status_run_model=='not-yet':
        return "The inference has not been launched. Press Run model in the Model tab to view results.",{'margin-bottom': '20px','display':'none'}
    elif status_run_model=="in-progress":
        return "The model is running. You can view the current status in the Model tab. Come back later to see the results",{'margin-bottom': '20px','display':'none'}
    elif status_run_model=="error":
        return "An error occurred during model execution. Close the current tab and start a new simulation.",{'margin-bottom': '20px','display':'none'}
    elif status_run_model=="completed":
        if subtab == 'subtab-cooccurrence':
            return layout_co_occurence_networks(legend_store,info_current_file_store,values_co_occurence),{'margin-bottom': '20px'}
        elif subtab == 'subtab-performance':
            return layout_performance_metrics(),{'margin-bottom': '20px'}
        elif subtab== 'subtab-features-selection':
            return layout_features_selection(legend_store,info_current_file_store,values_features_selection,legend_covariates),{'margin-bottom': '20px'}
    else:
        print("info current file status run model not correct")
        return None,{'margin-bottom': '20px','display':'none'}




