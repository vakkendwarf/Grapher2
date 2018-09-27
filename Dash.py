import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import Graph as mg
import Sql as sqli
import datetime

app = dash.Dash()

app.layout = html.Div([
    html.H1('Grapher 2.1'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Overall', 'value': 'all'},
            {'label': 'Daily', 'value': 'daily'},
        ],
        value='all'
    ),
    dcc.Graph(id='my-graph')
])


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):

    x, y = zip(sqli.pull_entire_db())

    return {
        'data': [{
            'x': x,
            'y': y
        }]
    }


if __name__ == '__main__':
    app.run_server()

