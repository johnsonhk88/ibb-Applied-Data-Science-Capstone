# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)




#get launch site for Task1
#initial the 
launchSites = []
launchSites.append({"label":"All Sites", "value": "All Sites"})
#get lanuch site name from dataframe
for item in spacex_df["Launch Site"].value_counts().index: # get index name
    launchSites.append({"label": item, "value": item})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id="site-dropdown" , options=launchSites, value = 'All Sites', placeholder = "Select a Launch Site here", searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id="payload-slider", min=0, max= 10000, step=1000, value= [min_payload, max_payload], 
                                                marks={2500: {"label": "2500 (kg)"}, 5000: {"label": "5000 (kg)"}, 7500: {"label": "7500 (kg)"}}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart", component_property="figure"),
              Input(component_id="site-dropdown", component_property="value") )

def select(inputt):
    if inputt == "All Sites":
        #display all sites
        newDF = spacex_df.groupby(["Launch Site"])["class"].sum().to_frame() #groupby lanch site with clas 
        newDF = newDF.reset_index() # reest index
        fig = px.pie(newDF, values="class", names="Launch Site", title="Total Success Launches by Site")
    else:
        #filter select the launch Site with class value counts by failkure success  
        newDF = spacex_df[spacex_df["Launch Site"] == inputt]["class"].value_counts().to_frame()
        newDF["name"] = ["Failure", "Success"]
        fig = px.pie(newDF, values="class", names="name",  title='Total Success Launches for ' + inputt)
    
    return fig
    


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id="success-payload-scatter-chart", component_property="figure"),
             Input(component_id="site-dropdown", component_property="value"),
             Input(component_id="payload-slider", component_property="value"))

def satter(val1, val2):
    print(val1)
    print(val2)
    if val1 == "All Sites":
        newDF = spacex_df
    else:
        newDF = spacex_df[spacex_df["Launch Site"] == val1] # filter Site 

    #filter the payload mass value
    newDF2 = newDF[newDF["Payload Mass (kg)"]>= val2[0]] #select/filer larger than min payload mass
    newDF3 = newDF2[newDF["Payload Mass (kg)"] <= val2[1]] # select/filter less than max payload mass
    fig2 = px.scatter(newDF3, y="class", x="Payload Mass (kg)", color="Booster Version Category")
    return fig2





# Run the app
if __name__ == '__main__':
    app.run_server()
