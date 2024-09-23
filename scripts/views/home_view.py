import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

from maindash import app

def layout_home():
    layout=html.Div(children=[

    html.P('''MDiNE Explorer is a user-friendly interface for analyzing differential networks of
           species. MDiNE Explorer exploits the original MDiNE framework to have robust inferences 
           on the associations between taxa. Moreover, the tool allows the user to identify 
           core variables associated with species, exploiting powerful Bayesian feature 
           selection strategies, such as the Horseshoe, LASSO or Ridge. The model is 
           divided into 3 main steps, the data import and pre-processing, the model and 
           the network vizualization. Result export is also possible in the corresponding 
           tab. Below, we provide general guidelines and details for each step. 
           Technicalities are provided in each section separately.''',
           style={"margin-top":"1em",'margin-left':'10px','text-indent':'15px'}),

    html.H5("Data Step",style={'fontWeight': 'bold',"margin-top":"2em",'margin-left':'10px'}),

    html.Div(id='data-step',style={'margin-left':'10px','text-indent':'15px'},children=[
        html.P('''MDiNE Explorer requires a .tsv text file including both taxa and covariables. 
               Column names must be included. The user could specify the reference taxa 
               and whether the model must be fitted in both two groups. If this option is
                not chosen by the user, one network will be constructed combining all the 
               samples. Certain filters are possible, removing taxa with high proportions
            of zeros and/or with small variability. A summary of the original and filtered 
            data is provided for general information.''',style={"margin-top":"1em"})]),

    html.H5("Model Step",style={'fontWeight': 'bold',"margin-top":"2em",'margin-left':'10px'}),

    html.Div(id='model-step',style={'margin-left':'10px','text-indent':'15px'},children=[
        html.P('''This section allows the user to select the appropriate model for both 
            the precision matrices and the covariables. For the former, only the 
            Graphical LASSO is available, while for the latter, three different 
            choices of priors are offered to the user: the Bayesian LASSO, the 
            Bayesian Ridge, and the Horseshoe.  This step requires particular 
            attention from the user to provide accurate and reliable results. 
            See the related section for additional details.
            ''',style={"margin-top":"1em"})]),

    html.H5("Visualization Step",style={'fontWeight': 'bold',"margin-top":"2em",'margin-left':'10px'}),

    html.Div(id='visu-step',style={'margin-left':'10px','text-indent':'15px'},children=[
        html.P('''After running the model, networks of species can be interactively visualized 
            through the corresponding visualization tab. This section offers the possibility 
            to the user to analyze networks in each of the two groups or in differentially 
            way. User can change the levels of credibility intervals and have graphical 
            options to include taxonomic information. Additionnally, visualizing associations 
            between covariables and taxa is also possible. Performance metrics of the 
            underlying sampler is provided for sanity check.
            ''',style={"margin-top":"1em"})]),
            ])
    
    return layout