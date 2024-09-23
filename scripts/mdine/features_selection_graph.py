import arviz as az
import networkx as nx
import re


def get_gml_features_selection_graph(idata,list_taxa,list_covariates,legend_store,color_covariates,hdi,filename_gml):
    G = nx.Graph()
    hdi_beta_matrix = az.hdi(idata, var_names=["beta_matrix"], hdi_prob=hdi).beta_matrix.values
    beta_matrix=idata.posterior.beta_matrix.mean(dim=["chain", "draw"]).values

    dict_element_color=get_dict_element_color(legend_store)

    for i in range(len(list_covariates)):
        G.add_node(list_covariates[i], color=color_covariates, size=100)

    for j in range(len(list_taxa)):
        G.add_node(list_taxa[j], color=dict_element_color.get(list_taxa[j],'#f7da1d'), size=100)


        for k in range(len(list_covariates)):

            lower_hdi=hdi_beta_matrix[k][j][0]
            higher_hdi=hdi_beta_matrix[k][j][1]

            if round(float(lower_hdi),3)*round(float(higher_hdi),3)>=0:
                # Don't contain zero
                coefficient = beta_matrix[k][j]
                color = '#18B532' if coefficient > 0 else '#E22020'
                G.add_edge(list_taxa[j], list_covariates[k], color=color, type='solid',width=abs(coefficient))

    nx.write_gml(G, filename_gml)

def get_elements_features_selection_graph(list_taxa,list_covariates,legend_store,legend_covariates):
    elements=[]
    nb_species=len(list_taxa)
    nb_covariates=len(list_covariates)

    ## Construction of the linear layout
    x_origin=200
    y_origin=200
    x_step=400
    y_step=500

    for i in range(nb_covariates):
        
        x=x_origin+(i-(nb_covariates-1)/2)*x_step
        y=y_origin
        elements.append({'data': {'id': str(list_covariates[i]), 'label': str(list_covariates[i])},'position': {'x':x,'y':y}})

    for j in range(nb_species):
        x=x_origin+(j-(nb_species-1)/2)*x_step
        y=y_origin+y_step
        elements.append({'data': {'id': str(list_taxa[j]), 'label': str(list_taxa[j])},'position': {'x':x,'y':y}})
        for k in range (nb_covariates):
            elements.append({'data': {'source': list_covariates[k], 'target': list_taxa[j]}})


    # Add legend elements
    elements_legend=get_legend_features_selection_graph(legend_store,legend_covariates)
    for el in elements_legend:
        elements.append(el)
    
    return elements

def is_valid_hex_color(hex_color):
    return re.fullmatch(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color) is not None

def get_stylesheet_features_selection_graph(idata,list_taxa,list_covariates,legend_store,legend_covariates,hdi,node_size,edge_width,font_size):
    hdi_beta_matrix = az.hdi(idata, var_names=["beta_matrix"], hdi_prob=hdi).beta_matrix
    beta_matrix=idata.posterior.beta_matrix.mean(dim=["chain", "draw"])

    dict_element_color=get_dict_element_color(legend_store)

    stylesheet=[]

    color_covariates=legend_covariates["color"] if is_valid_hex_color(legend_covariates["color"]) else '#2acedd'
    for i in range(len(list_covariates)):
        style_node={
        'selector': f'node[id = "{list_covariates[i]}"]',
        'style': {
            'background-color': color_covariates,
            'label': 'data(label)',
            'width': node_size,
            'height': node_size,
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': f'{font_size}px'
            }
        }
        stylesheet.append(style_node)

    for j in range(len(list_taxa)):
        style_node={
        'selector': f'node[id = "{list_taxa[j]}"]',
        'style': {
            'background-color': dict_element_color.get(list_taxa[j],'#f7da1d'),
            'label': 'data(label)',
            'width': node_size,
            'height': node_size,
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': f'{font_size}px'
            }
        }
        stylesheet.append(style_node)


        for k in range(len(list_covariates)):

            lower_hdi=hdi_beta_matrix[k][j][0]
            higher_hdi=hdi_beta_matrix[k][j][1]
        

            if round(float(lower_hdi),3)*round(float(higher_hdi),3)>=0:
                
            
                #Same sign, do not contains null value. Create edge
                coefficient = beta_matrix[k][j]
                color = '#18B532' if coefficient > 0 else '#E22020'
                width = abs(round(float(coefficient),3)) * edge_width #Same sign, do not contains null value. Create edge
                style_edge={
                    'selector': f'edge[source = "{list_covariates[k]}"][target = "{list_taxa[j]}"]',
                    'style': {
                        'line-color': color,
                        'width': width,
                        'curve-style': 'bezier',
                        'target-arrow-shape': 'none',
                    }
                }
                
            else:
                style_edge={
                    'selector': f'edge[source = "{list_covariates[k]}"][target = "{list_taxa[j]}"]',
                    'style': {
                        'display': 'none',
                    }
                }
            stylesheet.append(style_edge)


    # Add legend style
    style_elements_legend=get_legend_style_features_selection_graph(legend_store,legend_covariates)
    for el in style_elements_legend:
        stylesheet.append(el)
    
    return stylesheet

def get_legend_features_selection_graph(legend_store,legend_covariates):
    legend=[{'data': {'id': 'legend_parent', 'label': 'Legend'},'classes': 'normal-network',}]
    space_between_nodes=25

    x_origin=0
    y_origin=0

    if legend_store==[]:
        node={'data': {'id': "group_covariates", 'label': legend_covariates["text"], 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin}}#,'locked': True
        legend.append(node)
        node={'data': {'id': "group_default", 'label': "Species", 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin+space_between_nodes}}#,'locked': True
        legend.append(node)
        pos_asso= {'data': {'id': 'positive_association', 'label': 'Positive Association', 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y':y_origin+2*space_between_nodes}}#,'locked': True
        neg_asso= {'data': {'id': 'negative_association', 'label': 'Negative Association', 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin+3*space_between_nodes}}#,'locked': True
        legend.append(pos_asso)
        legend.append(neg_asso)
    else:
        node={'data': {'id': "group_covariates", 'label': legend_covariates["text"], 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin}}#,'locked': True
        legend.append(node)
        for idx,group in enumerate(legend_store):

            node={'data': {'id': group["id"], 'label': group["label"], 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin+(idx+1)*space_between_nodes}}#,'locked': True
            legend.append(node)

        nb_species=len(legend_store)
        pos_asso= {'data': {'id': 'positive_association', 'label': 'Positive Association', 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin+(nb_species+1)*space_between_nodes}}#,'locked': True
        neg_asso= {'data': {'id': 'negative_association', 'label': 'Negative Association', 'parent': 'legend_parent'}, 'classes': 'normal-network','grabbable': False,'position': {'x': x_origin, 'y': y_origin+(nb_species+2)*space_between_nodes}}#,'locked': True
        legend.append(pos_asso)
        legend.append(neg_asso)

    #Legend for differentiel co-occurence-network
    width_edges=30
    legend.append({'data': {'id': 'legend_diff_parent', 'label': 'Legend'}, 'classes': 'diff-network'})
    green_node= {'data': {'id': 'green_diff_node', 'label': 'Higher in second group', 'parent': 'legend_diff_parent'}, 'classes': 'diff-network','grabbable': False,'position': {'x': 0, 'y': 0}}#,'locked': True
    red_node= {'data': {'id': 'red_diff_node', 'label': 'Lower in second group', 'parent': 'legend_diff_parent'}, 'classes': 'diff-network','grabbable': False,'position': {'x': 0, 'y': space_between_nodes}}#,'locked': True
    dashed_edge1= {'data': {'id': 'dashed_edge1', 'label': 'Second group abs association stronger', 'parent': 'legend_diff_parent'}, 'classes': 'diff-network','grabbable': False,'position': {'x': width_edges/6-width_edges/2, 'y': 2*space_between_nodes}}#,'locked': True
    dashed_edge2= {'data': {'id': 'dashed_edge2', 'label': 'Second group abs association stronger', 'parent': 'legend_diff_parent'}, 'classes': 'diff-network','grabbable': False,'position': {'x': -width_edges/6+width_edges/2, 'y': 2*space_between_nodes}}#,'locked': True
    line_full_edge= {'data': {'id': 'line_full_edge', 'label': 'First group abs association stronger', 'parent': 'legend_diff_parent'}, 'classes': 'diff-network','grabbable': False,'position': {'x': 0, 'y': 3*space_between_nodes}}#,'locked': True

    legend.append(green_node)
    legend.append(red_node)
    legend.append(dashed_edge1)
    legend.append(dashed_edge2)
    legend.append(line_full_edge)

    return legend

def get_legend_style_features_selection_graph(legend_store,legend_covariates):
    network_type="normal-network"
    if network_type=="diff-network":
        width_circle=20
        style_legend=[
            {
            'selector': 'node#legend_diff_parent',
            'style': {
                'shape': 'round-rectangle',
                'border-color': '#000000',
                'border-width': 1,
                'label': 'data(label)',
                'text-valign': 'top',
                'text-halign': 'center',
                "layout":'concentric'
            }
        }]
        legend_green_node={
                'selector': 'node[id="green_diff_node"]',
                'style': {
                    'background-color': '#00ff00',
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'right',
                    'shape':'circle',
                    'width': width_circle,
                    'height': width_circle
                }}
        legend_red_node={
                'selector': 'node[id="red_diff_node"]',
                'style': {
                    'background-color': '#ff0000',
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'right',
                    'shape':'circle',
                    'width': width_circle,
                    'height': width_circle
                }}
        legend_dashed_edge1={
                'selector': 'node[id="dashed_edge1"]',
                'style': {
                    'background-color': 'black',    
                    'shape': 'rectangle',           
                    'width': 30/3,                   
                    'height': 3                 
                }
                }
        legend_dashed_edge2={
                'selector': 'node[id="dashed_edge2"]',
                'style': {
                    'label': 'data(label)',  
                    'text-valign': 'center',
                    'text-halign': 'right',
                    'background-color': 'black',       
                    'shape': 'rectangle',           
                    'width': 30/3,                   
                    'height': 3                    
                }
                }
        legend_line_full_edge={
                'selector': 'node[id="line_full_edge"]',
                'style': {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'right',  
                    'background-color': 'black',
                    'shape': 'rectangle',          
                    'width': 30,                   
                    'height': 2                   
                }
                }
        
        style_legend.append(legend_green_node)
        style_legend.append(legend_red_node)
        style_legend.append(legend_dashed_edge1)
        style_legend.append(legend_dashed_edge2)
        style_legend.append(legend_line_full_edge)

        style_normal_legend={
            'selector': '.normal-network',
            'style': {
                'display': 'none',
            }
        }

        style_legend.append(style_normal_legend)

    elif network_type=="normal-network":
        style_legend=[
            {
            'selector': 'node#legend_parent',
            'style': {
                'shape': 'round-rectangle',
                'border-color': '#000000',
                'border-width': 1,
                'label': 'data(label)',
                'text-valign': 'top',
                'text-halign': 'center',
                "layout":'preset'
            }
        }]

        width_circle=20

        if legend_store==[]:
            legend_default={
            'selector': 'node[id="group_default"]',
            'style': {
                'background-color': '#f7da1d',
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'shape':'circle',
                'width': width_circle,
                'height': width_circle
            }}
            style_legend.append(legend_default)
            color_covariates=legend_covariates["color"] if is_valid_hex_color(legend_covariates["color"]) else '#2acedd'
            legend_default={
            'selector': 'node[id="group_covariates"]',
            'style': {
                'background-color': color_covariates,
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'shape':'circle',
                'width': width_circle,
                'height': width_circle
            }}
            style_legend.append(legend_default)
        
        else:
            color_covariates=legend_covariates["color"] if is_valid_hex_color(legend_covariates["color"]) else '#2acedd'
            legend_default={
            'selector': 'node[id="group_covariates"]',
            'style': {
                'background-color': color_covariates,
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'shape':'circle',
                'width': width_circle,
                'height': width_circle
            }}
            style_legend.append(legend_default)

            for group in legend_store:
                legend_group={
                'selector': f'node[id="{group["id"]}"]',
                'style': {
                    'background-color': group["color"],
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'text-halign': 'right',
                    'shape':'circle',
                    'width': width_circle,
                    'height': width_circle
                }}
                style_legend.append(legend_group)

        pos_asso={
            'selector': 'node[id="positive_association"]',
            'style': {
                'background-color': '#00ff00',
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'shape':'round-rectangle',
                'width': 40,
                'height': 5
            }
        }
        neg_asso={
            'selector': 'node[id="negative_association"]',
            'style': {
                'background-color': '#ff0000',
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'right',
                'shape':'round-rectangle',
                'width': 40,
                'height': 5
            }
        }
        style_legend.append(pos_asso)
        style_legend.append(neg_asso)

        style_diff_legend={
            'selector': '.diff-network',
            'style': {
                'display': 'none',
            }
        }

        style_legend.append(style_diff_legend)
    else:
        print("Network type not valid")
        style_legend=None

    return style_legend


def get_dict_element_color(legend_store):
    dict_elements_group={}
    for group in legend_store:
        list_elements=group["elements"]
        if list_elements!=[]:
            for element in list_elements:
                dict_elements_group[element]=group["color"]

    return dict_elements_group