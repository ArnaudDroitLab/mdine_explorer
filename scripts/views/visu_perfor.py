from dash import dcc, html,dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_cytoscape as cyto
cyto.load_extra_layouts()

import os

import pandas as pd
import numpy as np
import arviz as az

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from maindash import app, type_storage
from mdine.performance_metrics import get_energy_figure,get_acceptance_rate,get_trace_beta,get_trace_precision_matrix,get_rhat,get_list_variables_idata



def layout_performance_metrics():
    return html.Div([
            html.H4('Performance metrics'),
            html.Div([
    html.Label("Select the figures you want to plot:", style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='dropdown-performances-metrics',
        options=[
            {'label': 'Energy Graph', 'value': 'energy'},
            {'label': 'Beta Matrix Trace', 'value': 'beta_matrix_trace'},
            {'label': 'Precision Matrix Trace', 'value': 'precision_matrix_trace'},
            {'label': 'R-hat statistic', 'value': 'rhat'}
        ],
        placeholder="Select figures",
        multi=True,
        style={'width': '50%', 'margin': '20px 0'},
        persistence=True,
        persistence_type=type_storage,
    ),
    html.Div(id="output-graph-dropdown",children=[]),

    ])
        ])

@app.callback(
    Output("output-graph-dropdown","children"),
    Input("dropdown-performances-metrics","value"),
    State("info-current-file-store","data"),
    
)
def output_dropdown(list_graphs,info_current_file_store):

    new_children=[]

    two_groups=info_current_file_store["second_group"]
    


    if list_graphs!=None:

        if two_groups!=None:
            #Two groups
            file_idata1=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
            file_idata2=os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc")

            idata1=az.from_netcdf(file_idata1)
            idata2=az.from_netcdf(file_idata2)

        else:
            file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")

            idata=az.from_netcdf(file_idata)

        for graph in list_graphs:

            if graph=="energy":
                if two_groups==None:
                    energy_figure=get_energy_figure(idata)

                    new_children.append(html.H5(
                        "Energy Graph",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                    
                    new_children.append(dcc.Graph(figure=energy_figure,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'energy_graph'}}))
                else:
                    energy_figure1=get_energy_figure(idata1)

                    new_children.append(html.H5(
                        "Energy Graph (First Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                    
                    new_children.append(dcc.Graph(figure=energy_figure1,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'energy_graph_group_1'}}))

                    energy_figure2=get_energy_figure(idata2)

                    new_children.append(html.H5(
                        "Energy Graph (Second Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                    
                    new_children.append(dcc.Graph(figure=energy_figure2,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'energy_graph_group_2'}}))

            elif graph=="acceptance_rate":
                if two_groups==None:
                    acceptance_rate=get_acceptance_rate(idata)

                    new_children.append(html.H5(
                        "Acceptance Rate",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(dcc.Graph(figure=acceptance_rate,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'acceptance_rate'}}))
                else:
                    acceptance_rate1=get_acceptance_rate(idata1)

                    new_children.append(html.H5(
                        "Acceptance Rate (First Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(dcc.Graph(figure=acceptance_rate1,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'acceptance_rate_group_1'}}))

                    acceptance_rate2=get_acceptance_rate(idata2)

                    new_children.append(html.H5(
                        "Acceptance Rate (Second Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(dcc.Graph(figure=acceptance_rate2,style={'width': '90%','margin': '0 auto'},
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'acceptance_rate_group_2'}}))


            elif graph=="beta_matrix_trace":

                if two_groups==None:

                    trace_beta1,trace_beta2=get_trace_beta(idata)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_beta1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_beta2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace2'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Beta Matrix Graph",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                
                    new_children.append(element)

                else:

                    trace_beta1_group1,trace_beta2_group1=get_trace_beta(idata1)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_beta1_group1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace1_group_1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_beta2_group1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace2_group_1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Beta Matrix Graph (First Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                
                    new_children.append(element)

                    trace_beta1_group2,trace_beta2_group2=get_trace_beta(idata2)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_beta1_group2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace1_group_2'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_beta2_group2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'beta_matrix_trace2_group_1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Beta Matrix Graph (Second Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))
                
                    new_children.append(element)


            elif graph=="precision_matrix_trace":
                if two_groups==None:
                    trace_precision1,trace_precision2=get_trace_precision_matrix(idata)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_precision1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_precision2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace2'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Precision Matrix Trace",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(element)

                else:

                    trace_precision1_group1,trace_precision2_group1=get_trace_precision_matrix(idata1)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_precision1_group1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace1_group_1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_precision2_group1,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace2_group_1'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Precision Matrix Trace (First Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(element)

                    trace_precision1_group2,trace_precision2_group2=get_trace_precision_matrix(idata2)

                    element=html.Div([
                        html.Div([
                            dcc.Graph(figure=trace_precision1_group2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace1_group_2'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        
                        html.Div([
                            dcc.Graph(figure=trace_precision2_group2,
                                                  config={"toImageButtonOptions":{'format':'svg','filename':'precision_matrix_trace2_group_2'}}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ])

                    new_children.append(html.H5(
                        "Precision Matrix Trace (Second Group)",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                    ))

                    new_children.append(element)
            elif graph=='rhat':
                if two_groups==None:
                    list_variables_idata=get_list_variables_idata(idata)
                else:
                    list_variables_idata=get_list_variables_idata(idata1)
                try:
                    list_variables_idata.remove("precision_matrix_coef_diag")
                    list_variables_idata.remove("precision_matrix_coef_off_diag")
                except:
                    pass

                options_dropdown=[]
                for variable in list_variables_idata:
                    if variable=='lambda_mdine':
                       options_dropdown.append({'label': "Lambda Lasso Precision Matrix", 'value': 'lambda_mdine'})
                    else:
                        options_dropdown.append({'label': transform_chain(variable), 'value': variable})
                
                element=dcc.Dropdown(
                    id='dropdown-rhat-statistic',
                    options=options_dropdown,
                    placeholder="Select variables",
                    multi=True,
                    style={'width': '50%', 'margin': '20px 0'},
                    persistence=True,
                    persistence_type=type_storage,
                )
            
                new_children.append(html.H5(
                        "R-hat statistic",
                        style={'textAlign': 'center', 'fontWeight': 'bold'}
                ))

                new_children.append(element)
                new_children.append(html.Div(id="graphs_rhat"))

            else:
                print("Error invalid graph name")
        
    return new_children

@app.callback(Output("graphs_rhat","children"),
 Input('dropdown-rhat-statistic','value'),
 State("info-current-file-store","data"),
 State('dropdown-rhat-statistic','options'),  
)
def print_rhat_statistic(value_dropdown,info_current_file_store,options_dropdown):

    two_groups=info_current_file_store["second_group"]
    children=[]
    if two_groups!=None:
                #Two groups
                file_idata1=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
                file_idata2=os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc")

                idata1=az.from_netcdf(file_idata1)
                idata2=az.from_netcdf(file_idata2)

    else:
        file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")

        idata=az.from_netcdf(file_idata)
    
    
    if value_dropdown!=[] and value_dropdown!=None:
        if two_groups!=None:
            rhats1 = get_rhat(idata1, value_dropdown)
            rhats2=get_rhat(idata2, value_dropdown)

            for (var1, rhat1), (var2, rhat2) in zip(rhats1.items(), rhats2.items()):
                rhat_array1=rhat1[var1].values
                rhat_array2=rhat2[var2].values
                pb_divergence1=np.any(rhat_array1 > 1.1)
                pb_divergence2=np.any(rhat_array2 > 1.1)
                if pb_divergence1:
                    message1="At least one R-hat value is greater than 1.1, which may indicate model convergence problems. These values are shown in red."
                else:
                    message1="All R-hat values are below 1.1, suggesting good model convergence."
                if pb_divergence2:
                    message2="At least one R-hat value is greater than 1.1, which may indicate model convergence problems. These values are shown in red."
                else:
                    message2="All R-hat values are below 1.1, suggesting good model convergence."
                if rhat_array1.ndim == 0:
                   
                    df1 = pd.DataFrame({"Valeur": [rhat_array1.item()]})
                    df2 = pd.DataFrame({"Valeur": [rhat_array2.item()]})
                elif rhat_array1.ndim == 1:
                    
                    df1 = pd.DataFrame(rhat_array1, columns=["Valeur"])
                    df2 = pd.DataFrame(rhat_array2, columns=["Valeur"])
                elif rhat_array1.ndim == 2:
                    
                    df1 = pd.DataFrame(rhat_array1, columns=[f"Col{j+1}" for j in range(rhat_array1.shape[1])])
                    df2 = pd.DataFrame(rhat_array2, columns=[f"Col{j+1}" for j in range(rhat_array2.shape[1])])
                else:
                    raise ValueError("Le tableau numpy doit être 1D ou 2D pour être affiché dans une DataTable.")
                
                label=var1
                for option in options_dropdown:
                        if var1==option["value"]:
                            label=option["label"]
                            break

                children.append(html.Div([
                    html.H2(f"{label} (First Group)"),
                    html.H5(message1),
                    dash_table.DataTable(
                        columns=[{"name": col, "id": col} for col in df1.columns],
                        data=df1.to_dict('records'),
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '0px', 
                            #'maxWidth': '180px',
                            'whiteSpace': 'normal'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{' + col + '} > 1.1',
                                    'column_id': col
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            } for col in df1.columns
                        ],
                        export_format="csv",  
                        export_headers='display',
                    )
                ],style={'margin-bottom':"20px"}))
                children.append(html.Div([
                    html.H2(f"{label} (Second Group)"),
                    html.H5(message2),
                    dash_table.DataTable(
                        columns=[{"name": col, "id": col} for col in df2.columns],
                        data=df2.to_dict('records'),
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '0px', 
                            
                            'whiteSpace': 'normal'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{' + col + '} > 1.1',
                                    'column_id': col
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            } for col in df2.columns
                        ],
                        export_format="csv",  
                        export_headers='display',  
                    )
                ],style={'margin-bottom':"20px"}))
        else:
            rhats = get_rhat(idata, value_dropdown)
            for var, rhat in rhats.items():
                rhat_array=rhat[var].values
                pb_divergence=np.any(rhat_array > 1.1)
                if pb_divergence:
                    message="At least one R-hat value is greater than 1.1, which may indicate model convergence problems. These values are shown in red."
                else:
                    message="All R-hat values are below 1.1, suggesting good model convergence."
                if rhat_array.ndim == 0:
                    
                    df = pd.DataFrame({"Valeur": [rhat_array.item()]})
                elif rhat_array.ndim == 1:
                    
                    df = pd.DataFrame(rhat_array, columns=["Valeur"])
                elif rhat_array.ndim == 2:
                    
                    df = pd.DataFrame(rhat_array, columns=[f"Col{j+1}" for j in range(rhat_array.shape[1])])
                else:
                    raise ValueError("Numpy array must be 1D or 2D to be displayed in a DataTable.")
                
                label=var
                for option in options_dropdown:
                        if var==option["value"]:
                            label=option["label"]
                            break

                children.append(html.Div([
                    html.H2(label),
                    html.H5(message),
                    dash_table.DataTable(
                        columns=[{"name": col, "id": col} for col in df.columns],
                        data=df.to_dict('records'),
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '0px', 
                            'whiteSpace': 'normal'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{' + col + '} > 1.1',
                                    'column_id': col
                                },
                                'backgroundColor': 'tomato',
                                'color': 'white'
                            } for col in df.columns
                        ],
                        export_format="csv",  
                        export_headers='display',  
                    )
                ],style={'margin-bottom':"20px"}))


        

    return children

def transform_chain(chain_string):
    words = chain_string.split('_')
    
    words_capitalizes = [word.capitalize() for word in words]
    
    chaine_transformee = ' '.join(words_capitalizes)
    
    return chaine_transformee