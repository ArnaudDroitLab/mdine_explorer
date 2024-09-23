from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os

import zipfile
from io import BytesIO

from maindash import app

button_hover_style = {
    'background': '#4A90E2'
}

button_style = {
    'background': '#4CAF50',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'margin': '10px',
    'display': 'inline-block',
    'vertical-align': 'middle',
    'hover': button_hover_style
}

def layout_export_results(status_run_model):
    if status_run_model=="not-yet":
        return html.H5("The inference has not been launched. Press Run model in the Model tab to download futur results.")
    elif status_run_model=="in-progress":
        return html.H5("The model is running. You can view the current status in the Model tab. Come back later to download the results")
    elif status_run_model=="completed":
        return make_real_layout()
    else:
        raise ValueError
    

def make_real_layout():
    return html.Div([
            html.H5("The inference has been completed. You can download the raw results below.",style={"margin-top":"20px","margin-bottom":"20px"}),
            html.Div([
                html.Button("Download raw results", id="download-button",style=button_style),
                dcc.Download(id="download")
            ]),

            html.P('''A .zip file 
                   is downloaded containing one or two inference files 
                   (depending on whether the data has been split into two groups). 
                   The data is in .nc format. They can be opened in several
                   different software programs or programming languages. 
                   In Python, in particular, the arviz library makes it easy to 
                   open this file with the command:''',style={"margin-top":"20px"}),

            html.Pre("import arviz as az\nidata = az.from_netcdf('idata.nc')\nprint(idata)",style={"margin-top":"10px"}),
            html.P('''With this data, you can redo all the figures shown in the visualization 
                   section. In particular, downloading inference data can be useful if you wish 
                   to observe other performance metrics.''',style={"margin-top":"20px"})




        ])



# Callback for file download
@app.callback(
    Output("download", "data"),
    Input("download-button", "n_clicks"),
    State("info-current-file-store","data"),
    State("status-run-model","data"),
    prevent_initial_call=True
)

def download_file(n_clicks,info_current_file_store,status_run_model):

    if status_run_model!="completed":
        raise PreventUpdate
    
    two_groups=info_current_file_store["second_group"]

    list_files=[]
   
    if two_groups!=None:
        #Two groups
        list_files.append(os.path.join(info_current_file_store["session_folder"],"first_group","idata.nc"))
        list_files.append(os.path.join(info_current_file_store["session_folder"],"second_group","idata.nc"))

    else:
        list_files.append(os.path.join(info_current_file_store["session_folder"],"idata.nc"))

            

    # ZIP filename
    zip_filename = "idata_raw_results.zip"

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in list_files:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)

    zip_buffer.seek(0)

    return dcc.send_bytes(zip_buffer.getvalue(), filename=zip_filename)
