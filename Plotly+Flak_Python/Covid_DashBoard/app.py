import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go  
import dash.dependencies as dd
from flask import Flask , render_template
import api.database as db

my_server = Flask(__name__)

app = dash.Dash(__name__ , server = my_server , routes_pathname_prefix = '/dash/'  )

country_data_cache = {}

def load_all_country_data():
    global country_data_cache
    country_data_cache = db.get_all_countries_data()  

load_all_country_data()


@my_server.route('/')
def index():
    return render_template('index.html')

app.layout = html.Div([
    html.H1("Covid 19 Data Analyzer" , style = { 'textAlign': 'center' }),

    dcc.Dropdown(

        id = 'country_dropdown' , 
        options = db.get_all_countries(),
        value = 'BRA',
        style = {'width': '50%', 'margin': 'auto'}
    ),

    dcc.Graph (id = 'covid_graph')
])


@app.callback(

    dd.Output('covid_graph' , 'figure'),
    [dd.Input('country_dropdown' , 'value')]
)

def update_graph(country):

    data =  country_data_cache.get(country)

    if not data:
        return {

            'data' : [],
            'layout' : go.Layout(title = f'Not available for {country}')

        }
    
    try:

        dates = [entry['date'][:10] for entry in data]
        cases = [entry['total_cases'] for entry in data]

    except TypeError as e:

        print(f"Error processing data: {e}")  

        return {

            'data': [],
            'layout': go.Layout(title=f"Error processing data for {country}")

        }

    fig = go.Figure(data = go.Scatter(x = dates, y = cases, mode = 'lines'))
    fig.update_layout(
        title = f"Confirmed Cases of COVID-19 in {country}",
        xaxis_title = "Date",
        yaxis_title = "Number of Cases"
    )
    
    return fig


if __name__ == '__main__':
    app.run_server(debug = True )