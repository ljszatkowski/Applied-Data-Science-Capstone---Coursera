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
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'LC40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'SLC40'},
                                        {'label': 'KSC LC-39A', 'value': 'LC39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'SLC4E'},
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.P(dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',10000: '10000'},
                                    value=[min_payload, max_payload])
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        if entered_site == 'LC40':
            fig = px.pie(spacex_df.loc[spacex_df['Launch Site'] == "CCAFS LC-40"].groupby('class').count(), 
            values='Launch Site', 
            names=['Failure','Sucess'],
            title='Total Success Launches at CCAFS LC-40 Launch Site')
            return fig
        else:
            if entered_site == 'SLC40':
                fig = px.pie(spacex_df.loc[spacex_df['Launch Site'] == "CCAFS SLC-40"].groupby('class').count(), 
                values='Launch Site', 
                names=['Failure','Sucess'], 
                title='Total Success Launches at CCAFS SLC-40 Launch Site')
                return fig
            else:
                if entered_site == 'LC39A':
                    fig = px.pie(spacex_df.loc[spacex_df['Launch Site'] == "KSC LC-39A"].groupby('class').count(), 
                    values='Launch Site',
                    names=['Failure','Sucess'], 
                    title='Total Success Launches at KSC LC-39A Launch Site')
                    return fig
                else:
                    if entered_site == 'SLC4E':
                        fig = px.pie(spacex_df.loc[spacex_df['Launch Site'] == "VAFB SLC-4E"].groupby('class').count(), 
                        values='Launch Site', 
                        names=['Failure','Sucess'],
                        title='Total Success Launches at VAFB SLC-4E Launch Site')
                        return fig
    # return the outcomes piechart for a selected site





# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def update_chart(entered_site, slider_range):
    if entered_site == 'ALL':
        low, high = slider_range
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], 
            y="class", 
            x="Payload Mass (kg)",
            labels={
				"class": "Success Rate",
				"Payload Mass (kg)": "Payload Mass in kg",
				"Booster Version Category":"Booster Version"
            },
            color="Booster Version Category", 
            title='Total Success Rate by Site')
        fig.update_yaxes(ticktext=["Failure", "Success"],tickvals=["0", "1"],)
        return fig
    else:
        if entered_site == 'LC40':
            filtered_df = spacex_df.loc[spacex_df['Launch Site'] == "CCAFS LC-40"]
            low, high = slider_range
            mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
            fig = px.scatter(filtered_df[mask], 
                y="class", 
                x="Payload Mass (kg)", 
				labels={
					"class": "Success Rate",
					"Payload Mass (kg)": "Payload Mass in kg",
					"Booster Version Category":"Booster Version"
				},
                color="Booster Version Category", 
                title='Total Success Rate at CCAFS LC-40 Launch Site')
            fig.update_yaxes(ticktext=["Failure", "Success"],tickvals=["0", "1"],)
            return fig
        else:
            if entered_site == 'SLC40':
                filtered_df = spacex_df.loc[spacex_df['Launch Site'] == "CCAFS SLC-40"]
                low, high = slider_range
                mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
                fig = px.scatter(filtered_df[mask], 
                    y="class", 
                    x="Payload Mass (kg)", 
					labels={
						"class": "Success Rate",
						"Payload Mass (kg)": "Payload Mass in kg",
						"Booster Version Category":"Booster Version"
					},
                    color="Booster Version Category", 
                    title='Total Success Rate at CCAFS SLC-40 Launch Site')
                fig.update_yaxes(ticktext=["Failure", "Success"],tickvals=["0", "1"],)
                return fig
            else:
                if entered_site == 'LC39A':
                    filtered_df = spacex_df.loc[spacex_df['Launch Site'] == "KSC LC-39A"]
                    low, high = slider_range
                    mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
                    fig = px.scatter(filtered_df[mask], 
                        y="class", 
                        x="Payload Mass (kg)", 
						labels={
							"class": "Success Rate",
							"Payload Mass (kg)": "Payload Mass in kg",
							"Booster Version Category":"Booster Version"
						},
                        color="Booster Version Category", 
                        title='Total Success Rate at KSC LC-39A Launch Site')
                    fig.update_yaxes(ticktext=["Failure", "Success"],tickvals=["0", "1"],)
                    return fig
                else:
                    if entered_site == 'SLC4E':
                        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == "VAFB SLC-4E"]
                        low, high = slider_range
                        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
                        fig = px.scatter(filtered_df[mask], 
                            y="class", 
                            x="Payload Mass (kg)", 
							labels={
								"class": "Success Rate",
								"Payload Mass (kg)": "Payload Mass in kg",
								"Booster Version Category":"Booster Version"
							},
                            color="Booster Version Category", 
                            title='Total Success Rate at VAFB SLC-4E Launch Site')
                        fig.update_yaxes(ticktext=["Failure", "Success"],tickvals=["0", "1"],)
                        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
