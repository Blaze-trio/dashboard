#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div(style={
    'backgroundColor': '#f9f9f9',
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px'
}, children=[
    dcc.Location(id='url', refresh=False),

    html.H1("🚗 Dashboard for VolksWagonTrio Company", style={
        'textAlign': 'center',
        'color': '#2c3e50',
        'fontSize': '32px',
        'marginBottom': '30px'
    }),

    html.Div(style={'marginBottom': '20px'}, children=[
        html.Label("📊 Select Statistics:", style={
            'fontWeight': 'bold',
            'marginRight': '10px'
        }),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '50%'}
        )
    ]),

    html.Div(style={'marginBottom': '30px'}, children=[
        html.Label("📅 Select Year (if applicable):", style={
            'fontWeight': 'bold',
            'marginRight': '10px'
        }),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='select-year',
            placeholder='Please select a year',
            style={'width': '50%'}
        )
    ]),

    html.Div(id='output-container', className='chart-grid', style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',
        'gap': '20px',
        'padding': '10px'
    })
])

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        #TASK 2.5: Create and display graphs for Recession Report Statistics

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        # grouping data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Automobile Sales Fluctuation over Recession Period (Yearly Average)"
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type as a Bar Chart
        # Grouping data by Vehicle_Type and calculating the mean of Automobile_Sales
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Vehicle Sales by Vehicle Type during Recession"
            )
        )

        # Plot 3: Pie Chart for total advertising expenditure share by vehicle type during recessions
        # grouping data for plotting
        # Hint: Use Vehicle_Type and Advertising_Expenditure columns
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type during Recession"
            )
        )

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        # grouping data for plotting
        # Hint: Use unemployment_rate, Vehicle_Type and Automobile_Sales columns
        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        # Return the four graphs arranged in two rows
        return [
            html.Div(
                style={'gridColumn': '1 / -1', 'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                children=[R_chart1, R_chart2]
            ),
            html.Div(
                style={'gridColumn': '1 / -1', 'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                children=[R_chart3, R_chart4]
            )
        ]
    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots 
    # Check for Yearly Statistics.
    elif selected_statistics == 'Yearly Statistics' and selected_year and selected_year != 'select-year':
        # Filter data for the selected year
        yearly_data = data[data['Year'] == int(selected_year)]
                                  
        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        # grouping data for plotting.
        # Hint: Use the columns Year and Automobile_Sales.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales Trend (Whole Period)"
            )
        )
                
        # Plot 2: Total Monthly Automobile sales using line chart.
        # grouping data for plotting.
        # Hint: Use the columns Month and Automobile_Sales.
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title="Total Monthly Automobile Sales"
            )
        )
                
        # Plot 3: Plot bar chart for average number of vehicles sold during the given year.
        # grouping data for plotting.
        # Hint: Use the columns Year and Automobile_Sales
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Vehicles Sold by Vehicle Type in the Year {}".format(selected_year)
            )
        )
                
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart.
        # grouping data for plotting.
        # Hint: Use the columns Vehicle_Type and Advertising_Expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertisement Expenditure for Each Vehicle"
            )
        )
                
        # TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(
                style={'gridColumn': '1 / -1', 'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                children=[Y_chart1, Y_chart2]
            ),
            html.Div(
                style={'gridColumn': '1 / -1', 'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                children=[Y_chart3, Y_chart4]
            )
        ]
    else:
        return html.Div("Please select a valid report type and (if applicable) a year.")

# Run the Dash app
if __name__ == '__main__':
    app.run(port=8051)
