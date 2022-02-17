# Importing libraries
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output

#Using the world happiness database.
happiness = pd.read_csv("world_happiness_dataset.csv")
#Different regions being stored in dictionary for use in Radio Buttons
region_options = [{'label' : i , 'value' : i} for i in happiness['region'].unique()]
#Different options of data such as happiness score and happiness rank,
# graph will be displayed based on type of choice of data.
radio_options = [{'label':'Happiness Score', 'value':'happiness_score'} , {'label':'Happiness Rank', 'value':'happiness_rank'}]

#Creating a dashboard with dash
app = dash.Dash()
#Defining the HTML layout as per our requirements
app.layout = html.Div(children=[
    html.H1('World Happiness Dashboard', style={'textAlign':'center'}),
    html.Br(),
    html.Label('Select Region:'),
    #Radio buttons that help the user to select the region.
    dcc.RadioItems(id = 'region-radio', options = region_options, value='North America'),

    html.Br(),
    html.Label('Select Country:'),
    #Dropdown menu that help the user to select the country based on the region.
    dcc.Dropdown(id = 'country-dropdown'),

    html.Br(),
    html.Label('Score or Rank?'),
    #Radio Buttons that help user select the type of data to be displayed: Score or rank
    dcc.RadioItems(id = 'data-radio', options=radio_options, value='happiness_score'),
    #Graph
    dcc.Graph(id = 'happiness-graph'),
    #HTML div, displays the avg of the selected data for the selected country
    html.Div(id='avg-div')
])

#callback function 1 : Takes the region as input and
# sets the dropdown menu based on the input of the region from the user
@app.callback(
    Output(component_id='country-dropdown', component_property='options'),
    Output(component_id='country-dropdown', component_property='value'),
    Input(component_id='region-radio',component_property='value')
)
def updateDropdown(selectedRegion):
    filteredDataset = happiness[happiness['region'] == selectedRegion]
    country_options = [{'label': i, 'value':i} for i in filteredDataset['country'].unique()]
    return country_options, country_options[0]['value']

#callback function 2: Takes the output of callback function 1 as input
# i.e. takes the selected country from the dropdown
# and also the radio button that selects the type of data
# Outputs the graph and avg of the selected data.
@app.callback(
    Output(component_id='happiness-graph',component_property='figure'),
    Output(component_id='avg-div', component_property='children'),
    Input(component_id='country-dropdown',component_property='value'),
    Input(component_id='data-radio',component_property='value')
)
def updateGraph(selectedCountry, selectedData):
    filteredDataset = happiness[happiness['country'] == selectedCountry]
    listOfTypeOfData = selectedData.split("_")
    stringOfTypeOfData = listOfTypeOfData[0].capitalize() + " " + listOfTypeOfData[1].capitalize()
    lineFigure = px.line(filteredDataset,x='year',y=selectedData, title=f'{stringOfTypeOfData} of {selectedCountry}',
                         labels={'year' : 'Year', selectedData : stringOfTypeOfData }, markers=True)
    selectedAvg = filteredDataset[selectedData].mean()
    return lineFigure, f'The average {stringOfTypeOfData} for {selectedCountry} is {selectedAvg}'

# App is run using the app.run_server() command.
if __name__ == '__main__':
    app.run_server(debug=True)
