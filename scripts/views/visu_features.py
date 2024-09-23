from dash import dcc, html,dash_table, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_cytoscape as cyto
cyto.load_extra_layouts()
from dash.exceptions import PreventUpdate
import json
import os
import uuid
import random
import re
import pandas as pd
import numpy as np
import arviz as az

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

from maindash import app, type_storage
from mdine.extract_data_files import get_separate_data,get_df_taxa,get_list_taxa,get_list_covariates
from mdine.features_selection_graph import get_elements_features_selection_graph,get_stylesheet_features_selection_graph, get_gml_features_selection_graph

button_download_style = {
    'background': '#4A90E2',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': 'auto',
    'margin-right': '10%',
}

button_modify_legend_style= {
    'background': '#4A90E2',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': '10%',
    'margin-right': 'auto',
}

button_graph_info_style= {
    'background': '#4A90E2',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': 'auto',
    'margin-right': 'auto',
    
}

button_export_graph_style= {
    'background': '#4A90E2',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': 'auto',
    'margin-right': 'auto',
}

button_save_legend_style= {
    'background': '#4caf50',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': '10%',
    'margin-right': 'auto',
}

button_add_item_style= {
    'background': '#a51e4d',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'margin-left': '10%',
    'margin-right': 'auto',
}

input_field_color_style = {
    'width': '10%',
    'padding': '8px',
    'border': '1px solid #ccc',
    'borderRadius': '5px',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
}

input_field_label_style = {
    'width': '10%',
    'padding': '8px',
    'border': '1px solid #ccc',
    'borderRadius': '5px',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
}

style_dropdown=None
style_div_parent_dropdown={'display': 'flex', 'align-items': 'center'}
style_elements_associated={"margin":'30px'}
style_div_dropdown={'width': '50%'}

def layout_features_selection(legend_store,info_current_file_store,values_features_selection,status_legend_covariates):

    switch_networks_diff=None

    if info_current_file_store["phenotype_column"]==None:
        switch_networks_diff=html.Div()
        file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")
    else:
        switch_networks_diff=dcc.RadioItems(
            id='checklist-networks-features-selection',
            options=[
                {'label': 'First group co-occurrence network', 'value': 'first_group'},
                {'label': 'Second group co-occurrence network', 'value': 'second_group'},
            ],
            value="first_group",
            persistence=True,
            persistence_type=type_storage,
            style={'margin': '20px 0'}
        )
        file_idata=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
        
    idata=az.from_netcdf(file_idata)

    list_taxa=get_list_taxa(info_current_file_store)[:-1]
    list_covariates=get_list_covariates(info_current_file_store)
    elements=get_elements_features_selection_graph(list_taxa,list_covariates,legend_store,status_legend_covariates)
    stylesheet=get_stylesheet_features_selection_graph(idata,list_taxa,list_covariates,legend_store,status_legend_covariates,hdi=values_features_selection["credibility"],node_size=values_features_selection["nodes_size"],edge_width=values_features_selection["edges_width"],font_size=values_features_selection["font_size"])

    string_list_covariates=""
    for covariate in list_covariates:
        string_list_covariates+=f"{covariate}, "

    color_covariates=status_legend_covariates["color"] if is_valid_hex_color(status_legend_covariates["color"]) else '#2acedd'
    text_covariates=status_legend_covariates["text"] if status_legend_covariates["text"]!="" else "Covariates"

    return html.Div([
                html.Div(id="state-separate-groups-features-selection",children=[switch_networks_diff]),
                cyto.Cytoscape(
                    id='cytoscape-features-selection',
                    elements=elements,
                    stylesheet=stylesheet,
                    autoRefreshLayout=True,
                    #responsive=True,
                    style={'width': '90%','height':'50vh','backgroundColor': '#f0f0f0','margin': '0 auto'},
                    layout={'name': 'preset'}
                    
                ),
                
                html.Div([
                    html.Button("Modify legend", id="button-modify-legend-features-selection",style=button_modify_legend_style),
                    html.Button("Export network as gml", id="button-export-graph-features-selection",style=button_export_graph_style),
                    dcc.Download(id="download-export-graph-features-selection"),
                    html.Button("Download network as svg", id="button-download-cytoscape-features-selection",style=button_download_style),

                ],style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
                
                html.Div(id="div-sliders-graph-features-selection",children=[

        # Slider Credibility
        html.Div([
            html.Label('Credibility'),
            html.Div(children=[
                html.Div([dcc.Slider(
                id='slider-credibility-features-selection',
                min=0.01,
                max=0.99,
                
                value=values_features_selection["credibility"],
                
                persistence=True,
                persistence_type=type_storage)],style={'width': '95%','display': 'inline-block'}),
                
            # Add a div to plot the value of the slider 
            html.Div(children=[values_features_selection["credibility"]],id='slider-output-container-credibility-features-selection', style={'margin': '0 auto', 'display': 'inline-block', 'width': '5%','vertical-align': 'top'}),

            ]),
        ], style={'width': '90%','margin': '0 auto'}),

        # Slider Edges Width
        html.Div([
            html.Label('Edges Width'),
            html.Div(children=[
                html.Div([dcc.Slider(
                id='slider-edges-width-features-selection',
                min=0,
                max=10,
               
                value=values_features_selection["edges_width"],
                
                persistence=True,
                persistence_type=type_storage)],style={'width': '95%','display': 'inline-block'}),
                
            # Add a div to plot the value of the slider 
            html.Div(children=[values_features_selection["edges_width"]],id='slider-output-container-edges-width-features-selection', style={'margin': '0 auto', 'display': 'inline-block', 'width': '5%','vertical-align': 'top'}),

            ]),
        ], style={'width': '90%','margin': '0 auto'}),

        # Slider Nodes Size
        html.Div([
            html.Label('Nodes Size'),
            html.Div(children=[
                html.Div([dcc.Slider(
                id='slider-nodes-size-features-selection',
                min=20,
                max=300,
                
                value=values_features_selection["nodes_size"],
                persistence=True,
                persistence_type=type_storage)],style={'width': '95%','display': 'inline-block'}),
                
            # Add a div to plot the value of the slider 
            html.Div(children=[values_features_selection["nodes_size"]],id='slider-output-container-nodes-size-features-selection', style={'margin': '0 auto', 'display': 'inline-block', 'width': '5%','vertical-align': 'top'}),

            ]),
        ], style={'width': '90%','margin': '0 auto'}),

        # Slider Font Size
        html.Div([
            html.Label('Font Size'),
            html.Div(children=[
                html.Div([dcc.Slider(
                id='slider-font-size-features-selection',
                min=1,
                max=100,
                
                value=values_features_selection["font_size"],
                persistence=True,
                persistence_type=type_storage)],style={'width': '95%','display': 'inline-block'}),
                
            # Add a div to plot the value of the slider 
            html.Div(children=[values_features_selection["font_size"]],id='slider-output-container-font-size-features-selection', style={'margin': '0 auto', 'display': 'inline-block', 'width': '5%','vertical-align': 'top'}),

            ]),
        ], style={'width': '90%','margin': '0 auto'}),


        ]),

        html.Div(id="div-modify-legend-features-selection",style={'display':'none'},children=[
            html.Div(style={'border-bottom': '3px solid #ccc',"width": "90%","margin": "0 auto","margin-top": "10px"}),
            html.H5("Taxa Legend",style={'fontWeight':'bold','margin-left': '5%',"margin-top": "10px"}),
            html.Div(id='items-container-features-selection'),
            html.Button('Add a group to the legend', id='add-item-features-selection', n_clicks=0,style=button_add_item_style),
            html.Div(style={'border-bottom': '3px solid #ccc',"width": "90%","margin": "0 auto","margin-top": "10px"}),
            html.H5("Covariates Legend",style={'fontWeight':'bold','margin-left': '5%',"margin-top": "10px"}),
            html.Div([
                        html.Div(
                            id="color-box-covariates-features-selection",
                            style={'width': '20px', 'height': '20px', 'backgroundColor': color_covariates, 'margin-left': "1%"}
                        ),
                        dcc.Input(
                            type='text',
                            placeholder='Enter hex color value',
                            value=color_covariates,
                            style={'flex': '0 1 10%', 'margin-right': '1%','width': '10%','padding': '8px','border': '1px solid #ccc','borderRadius': '5px','margin': '10px','vertical-align': 'middle'},
                            id='color-input-covariates-features-selection'
                        ),
                        dcc.Input(
                            type='text',
                            placeholder='Enter label',
                            id='label-input-covariates-features-selection',
                            value=text_covariates,
                            style={'flex': '0 1 15%', 'margin-right': '1%','width': '10%','padding': '8px','border': '1px solid #ccc','borderRadius': '5px','margin': '10px','vertical-align': 'middle',}
                        ),
                        html.Div(
                            style={'flex': '1', 'display': 'flex', 'align-items': 'center'},
                            children=[
                                html.H5(
                                    "Elements associated: ",
                                    style={"margin": '0 10px 0 0'}
                                ),
                                
                                html.Div(string_list_covariates,
                                
                    
                    style={'flex': '1','borderRadius': '5px', 'overflowX': 'auto', 'border': '1px solid #ccc', 'padding': '5px', 'margin': '5px', 'whiteSpace': 'nowrap','width': '400px'})
                            ]
                        ),
                       
                    ], id="choose-color-covariates-features-selection", style={'width': '90%', 'margin': '0 auto', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'display': 'flex', 'align-items': 'center', 'margin-top': '5px'})
        
        ])
                

           ])

@app.callback(
    Output("status-sliders-features-selection","data"),
    Input("slider-credibility-features-selection","value"),
    Input("slider-edges-width-features-selection","value"),
    Input("slider-nodes-size-features-selection","value"),
    Input("slider-font-size-features-selection","value"))
def update_status_sliders(credibility,edges_width,nodes_size,font_size):
    return {"credibility":credibility,"edges_width":edges_width,"nodes_size":nodes_size,"font_size":font_size}

@app.callback(
    Output("slider-output-container-credibility-features-selection", "children"),
    Output("slider-output-container-edges-width-features-selection", "children"),
    Output("slider-output-container-nodes-size-features-selection", "children"),
    Output("slider-output-container-font-size-features-selection", "children"),
    Input("status-sliders-features-selection", "modified_timestamp"),
    State("status-sliders-features-selection", "data"))
def update_output_edges_width(ts,data):
    if ts is None:
        raise PreventUpdate

    return f'{data["credibility"]}',f'{data["edges_width"]}',f'{data["nodes_size"]}',f'{data["font_size"]}'

@app.callback(
    Output("cytoscape-features-selection", "generateImage"),
    Input("button-download-cytoscape-features-selection", "n_clicks"))
def get_image(n_clicks):

    if n_clicks==None:
        raise PreventUpdate
    
    action = "download"
    ftype = "svg"
    filename = "network_features_selection"

    return {
        'type': ftype,
        'action': action,
        'filename': filename
        }

@app.callback(
    Output('cytoscape-features-selection', 'stylesheet',allow_duplicate=True),
    Input('slider-credibility-features-selection', 'value'),
    Input('slider-edges-width-features-selection', 'value'),
    Input('slider-nodes-size-features-selection', 'value'),
    Input('slider-font-size-features-selection', 'value'),
    State('state-separate-groups-features-selection','children'),
    State('legend-store','data'),
    State("info-current-file-store","data"),
    State('status-legend-covariates','data'),prevent_initial_call=True
)
def update_graph(credibility, edges_width, nodes_size,font_size,children,legend_store,info_current_file_store,legend_covariates):

    specific_graph=None

    list_taxa=get_list_taxa(info_current_file_store)[:-1]
    list_covariates=get_list_covariates(info_current_file_store)


    try:
        specific_graph=children[0]['props']['value']
    except:
        specific_graph=None

    print('specific graph: ',specific_graph)

    if specific_graph==None:
        file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")

        idata=az.from_netcdf(file_idata)

        stylesheet=get_stylesheet_features_selection_graph(idata,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)
    else:
        file_idata1=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
        file_idata2=os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc")


        idata1=az.from_netcdf(file_idata1)
        idata2=az.from_netcdf(file_idata2)

        if specific_graph=='first_group':
            stylesheet=get_stylesheet_features_selection_graph(idata1,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)
            
        elif specific_graph=='second_group':
            stylesheet=get_stylesheet_features_selection_graph(idata2,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)
        
        
    return stylesheet

@app.callback(
    Output("download-export-graph-features-selection", "data"),
    Input('button-export-graph-features-selection','n_clicks'),
    State('state-separate-groups-features-selection','children'),
    State('info-current-file-store','data'),
    State('legend-store','data'),
    State('status-sliders-features-selection','data')
)
def download_file(n_clicks,children_specific_graph,info_current_file_store,legend_store,values_features_selection):

    if n_clicks==None:
        raise PreventUpdate

    specific_graph=None
    filename_gml=None

    list_taxa=get_list_taxa(info_current_file_store)[:-1]
    list_covariates=get_list_covariates(info_current_file_store)
    color_covariates='#2acedd'

    try:
        specific_graph=children_specific_graph[0]['props']['value']
    except:
        specific_graph=None

    if specific_graph==None:
        file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")

        filename_gml=os.path.join(info_current_file_store["session_folder"],f"graph_features_selection_credibility_{values_features_selection["credibility"]}.gml")

        idata=az.from_netcdf(file_idata)
        
        get_gml_features_selection_graph(idata,list_taxa,list_covariates,legend_store,color_covariates,values_features_selection["credibility"],filename_gml)

    else:
        file_idata1=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
        file_idata2=os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc")
        idata1=az.from_netcdf(file_idata1)
        idata2=az.from_netcdf(file_idata2)


        if specific_graph=='first_group':
            filename_gml=os.path.join(info_current_file_store["session_folder"],f"graph_features_selection_group_1_credibility_{values_features_selection["credibility"]}.gml")
            get_gml_features_selection_graph(idata1,list_taxa,list_covariates,legend_store,color_covariates,values_features_selection["credibility"],filename_gml)
        elif specific_graph=='second_group':
            filename_gml=os.path.join(info_current_file_store["session_folder"],f"graph_features_selection_group_2_credibility_{values_features_selection["credibility"]}.gml")
            get_gml_features_selection_graph(idata2,list_taxa,list_covariates,legend_store,color_covariates,values_features_selection["credibility"],filename_gml)

    return dcc.send_file(filename_gml)

@app.callback(
    Output('div-sliders-graph-features-selection', 'style'),
    Output('div-modify-legend-features-selection', 'style'),
    Output("button-modify-legend-features-selection","children"),
    Output("button-modify-legend-features-selection","style"),
    Output("items-container-features-selection","children"),
    Output("cytoscape-features-selection","elements"),
    Output("cytoscape-features-selection","stylesheet"),
    Input("button-modify-legend-features-selection","n_clicks"),
    State('legend-store','data'),
    State("info-current-file-store","data"),
    State("cytoscape-features-selection","elements"),
    State('state-separate-groups-features-selection','children'),
    State("cytoscape-features-selection","stylesheet"),
    State('status-sliders-features-selection','data'),
    State("status-legend-covariates","data")
)
def display_selected_nodes(n_clicks,legend_store,info_current_file_store,cytoscape_elements,state_separate_groups,current_stylesheet,values_features_selection,legend_covariates):

    credibility=values_features_selection["credibility"]
    edges_width=values_features_selection["edges_width"]
    nodes_size=values_features_selection["nodes_size"]
    font_size=values_features_selection["font_size"]

    if n_clicks==None:
        raise PreventUpdate
    elif n_clicks%2==0:
        # Return to sliders

        specific_graph=None

        list_taxa=get_list_taxa(info_current_file_store)[:-1]
        list_covariates=get_list_covariates(info_current_file_store)
        elements=get_elements_features_selection_graph(list_taxa,list_covariates,legend_store,legend_covariates)

        try:
            specific_graph=state_separate_groups[0]['props']['value']
        except:
            specific_graph=None

        if specific_graph==None:
            file_idata=os.path.join(info_current_file_store["session_folder"],"idata.nc")

            idata=az.from_netcdf(file_idata)

            stylesheet=get_stylesheet_features_selection_graph(idata,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)
        else:

            file_idata1=os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc")
            file_idata2=os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc")


            idata1=az.from_netcdf(file_idata1)
            idata2=az.from_netcdf(file_idata2)

            if specific_graph=='first_group':
                stylesheet=get_stylesheet_features_selection_graph(idata1,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)
            elif specific_graph=='second_group':
                stylesheet=get_stylesheet_features_selection_graph(idata2,list_taxa,list_covariates,legend_store,legend_covariates,hdi=credibility,node_size=nodes_size,edge_width=edges_width,font_size=font_size)

        return None,{'display':'none'},"Modify legend",button_modify_legend_style,[],elements,stylesheet
    else:
        # Become Save Legend
        # Display Legend attributes
        remaining_taxa=get_list_remaining_taxa(legend_store,info_current_file_store)
        list_items=create_items(legend_store,remaining_taxa)

            

        return {'display':'none'},None,"Save legend",button_save_legend_style,list_items,cytoscape_elements,current_stylesheet
    



@app.callback(
    Output('legend-store', 'data',allow_duplicate=True),
    Output('items-container-features-selection', 'children',allow_duplicate=True),
    Input('add-item-features-selection', 'n_clicks'),
    Input({'type': 'trash-icon-features-selection', 'index': ALL}, 'n_clicks'),
    State('legend-store', 'data'),
    State('items-container-features-selection', 'children'),
    State("info-current-file-store","data"),prevent_initial_call=True
)
def display_items(add_clicks, trash_clicks,legend,children,info_current_file_store):

    if children is None:
        children = []

    nb_children=len(children)

    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'add-item-features-selection' in triggered_id and add_clicks!=0:
        new_color=random_hex_color()
        new_element_id = str(uuid.uuid4())
        new_group = {
        'id': new_element_id,
        'color': new_color,
        'label': f'Group {nb_children + 1}',
        'elements': []
        
        }
        legend.append(new_group)

    else:
        # difference between initial call and true call of trash icon
        trash=False
        for clicks in trash_clicks:
            if clicks!=None:
                trash=True
        if trash==True:
            trash_index = eval(triggered_id)['index']
            legend=[group for group in legend if group['id']!=trash_index]
    
    remaining_taxa=get_list_remaining_taxa(legend,info_current_file_store)

    list_items=create_items(legend,remaining_taxa)

    return legend,list_items

def random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@app.callback(
    Output('legend-store', 'data',allow_duplicate=True),
    Output({'type': 'color-box-features-selection', 'index': ALL}, 'style'),
    Input({'type': 'color-input-features-selection', 'index': ALL}, 'value'),
    Input({'type': 'label-input-features-selection', 'index': ALL}, 'value'),
    State('legend-store', 'data'),
    prevent_initial_call=True
)
def update_group_data(new_color_list,new_label_list, store_data):

    

    ctx = callback_context

    if [trigger['prop_id'].split('.')[0] for trigger in ctx.triggered]==['']:
        raise PreventUpdate

    triggered_inputs = [json.loads(trigger['prop_id'].split('.')[0]) for trigger in ctx.triggered]

    

    list_id=remove_duplicates([triggered_input['index'] for triggered_input in triggered_inputs])

    if len(new_color_list)==len(store_data):
        ## All components have triggered the callback
        for idx,group in enumerate(store_data):
            group['color'] = new_color_list[idx] 
            group['label'] = new_label_list[idx]
    else:
        ##Only one component has triggered
        triggered_id=triggered_inputs[0]
        for group in store_data:
            if group['id']==triggered_id:
                group['color'] = new_color_list[0] 
                group['label'] = new_label_list[0]
                break

    list_color_box=[]
    for color_value in new_color_list:
        if is_valid_hex_color(color_value):
            list_color_box.append({'width': '20px', 'height': '20px', 'backgroundColor': color_value,'margin-left':"1%"})
        else:
            list_color_box.append({'width': '20px', 'height': '20px', 'backgroundColor': "#FFFFFF",'margin-left':"1%"})


    return store_data,list_color_box

@app.callback(
    Output('legend-store', 'data',allow_duplicate=True),
    Output({'type': 'dropdown-group-items-features-selection', 'index': ALL}, 'options'),
    Input({'type': 'dropdown-group-items-features-selection', 'index': ALL}, 'value'),
    State('legend-store', 'data'),
    State('info-current-file-store', 'data'),
    prevent_initial_call=True
)
def update_group_data(list_value_dropdown, store_data,info_current_file_store):

    ctx = callback_context

    if [trigger['prop_id'].split('.')[0] for trigger in ctx.triggered]==['']:
        raise PreventUpdate

    triggered_inputs = [json.loads(trigger['prop_id'].split('.')[0]) for trigger in ctx.triggered]
    list_id=remove_duplicates([triggered_input['index'] for triggered_input in triggered_inputs])


    if len(list_value_dropdown)==len(store_data):
        ## All components have triggered the callback
        for idx,group in enumerate(store_data):
            group['elements'] = list_value_dropdown[idx]
            
    else:
        ##Only one component has triggered
        triggered_id=triggered_inputs[0]
        for group in store_data:
            if group['id']==triggered_id:
                
                group['elements'] = list_value_dropdown[0] 
                
    remaining_taxa=get_list_remaining_taxa(store_data,info_current_file_store)

    options_dropdown=[]
    for taxa in remaining_taxa:
        options_dropdown.append({'label': taxa, 'value': taxa})

    return_list_dropdown_options=[]

   

    for value_dropdown in list_value_dropdown:
        others_options=[]
        for element in value_dropdown:
            others_options.append({'label': element, 'value': element})
        return_list_dropdown_options.append(options_dropdown+others_options)

    


    return store_data,return_list_dropdown_options

def is_valid_hex_color(hex_color):
    return re.fullmatch(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color) is not None

def remove_duplicates(original_list):
    seen = set()
    unique_list = []
    for item in original_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list

def get_list_remaining_taxa(data_legend_store,info_current_file_store):
    
    list_remaining_taxa=get_list_taxa(info_current_file_store)[:-1]
    
    if data_legend_store!=[]:
        for group in data_legend_store:
            if len(group["elements"])!=0:
                for element in group["elements"]:
                    list_remaining_taxa.remove(element)
                        

    return list_remaining_taxa
def print_legend_store(legend_store):
    for group in legend_store:
        print(f"{group["label"]}, color: {group["color"]}, elements: {group["elements"]}")

def create_items(legend_store,remaining_taxa):
    options_dropdown=[]
    list_items=[]
    for taxa in remaining_taxa:
        options_dropdown.append({'label': taxa, 'value': taxa})
    
    for group in legend_store:
        options_dropdown=[]
        for taxa in remaining_taxa:
            options_dropdown.append({'label': taxa, 'value': taxa})
        for element in group["elements"]:
            options_dropdown.append({'label': element, 'value': element})

        color_value=group["color"] if is_valid_hex_color(group["color"]) else '#FFFFFF'

        element = html.Div([
                        html.Div(
                            id={'type': 'color-box-features-selection', 'index': group["id"]},
                            style={'width': '20px', 'height': '20px', 'backgroundColor': color_value, 'margin-left': "1%"}
                        ),
                        dcc.Input(
                            type='text',
                            placeholder='Enter hex color value',
                            value=group["color"],
                            style={'flex': '0 1 10%', 'margin-right': '1%','width': '10%','padding': '8px','border': '1px solid #ccc','borderRadius': '5px','margin': '10px','vertical-align': 'middle'},
                            id={'type': 'color-input-features-selection', 'index': group["id"]}
                        ),
                        dcc.Input(
                            type='text',
                            placeholder='Enter label',
                            id={'type': 'label-input-features-selection', 'index': group["id"]},
                            value=group["label"],
                            style={'flex': '0 1 15%', 'margin-right': '1%','width': '10%','padding': '8px','border': '1px solid #ccc','borderRadius': '5px','margin': '10px','vertical-align': 'middle',}
                        ),
                        html.Div(
                            style={'flex': '1', 'display': 'flex', 'align-items': 'center'},
                            children=[
                                html.H5(
                                    "Elements associated: ",
                                    style={"margin": '0 10px 0 0'}
                                ),
                                dcc.Dropdown(
                                    id={'type': 'dropdown-group-items-features-selection', 'index': group["id"]},
                                    value=group["elements"],
                                    options=options_dropdown,
                                    placeholder="Select elements",
                                    multi=True,
                                    style={'flex': '1','margin-right':"3%"},
                                    persistence=True,
                                    persistence_type=type_storage,
                                )
                            ]
                        ),
                        html.I(
                            className="fas fa-trash",
                            id={'type': 'trash-icon-features-selection', 'index': group["id"]},
                            style={'color': 'red', 'cursor': 'pointer', 'margin': '5px', 'margin-left': 'auto', 'margin-right': '3%'}
                        ),
                    ], id=group["id"], style={'width': '90%', 'margin': '0 auto', 'border': '1px solid black', 'border-radius': '10px', 'padding': '10px', 'display': 'flex', 'align-items': 'center', 'margin-top': '5px'})
        list_items.append(element)

    return list_items

@app.callback(
    Output('status-legend-covariates', 'data'),
    Input('color-input-covariates-features-selection', 'value'),
    Input('label-input-covariates-features-selection', 'value'))
def update_status_legend_covariates(color,text):
    return {"color":color,"text":text}

@app.callback(
    Output('color-box-covariates-features-selection', 'style'),
    Input('status-legend-covariates', 'modified_timestamp'),
    State('status-legend-covariates', 'data'))
def update_color_box(ts,data):
    if ts is None:
        raise PreventUpdate
    
    color=data["color"] if is_valid_hex_color(data["color"]) else '#2acedd'

    return {'width': '20px', 'height': '20px', 'backgroundColor': color, 'margin-left': "1%"}