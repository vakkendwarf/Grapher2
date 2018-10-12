import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import Sql as Sqli
# import call method from subprocess module
from os import system, name


# define clear functio
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')


print("SETTING UP SERVER")

app = dash.Dash()
server = app.server

print("SETTING UP LAYOUT")

app.layout = html.Div([
    html.H1('Grapher 2.2 on C v5.0'),
    dcc.Graph(id='overall'),
    dcc.Graph(id='daily'),
    dcc.Interval(id='dynamic-update', interval=1000, n_intervals=0)
])

print("???")


@app.callback(Output('overall', 'figure'), [Input('dynamic-update', 'n_intervals')])
def update_graph(n):

    clear()

    print("BEGIN UPDATE_GRAPH")

    arr = Sqli.pull_last_n_entries(100)

    # this needs to be bigger than previously because of how plotly likes to truncate things

    le: int = (len(arr)+1)

    # make empties

    a = [None] * le
    b = [None] * le

    # get our iterator

    k = 0

    for l, i, j in arr:

        # separate the rest of the data into arrays

        a[k] = i
        b[k] = j

        k += 1

    print(str(b[len(arr)-1]) + " Is the last value")

    trace = Scatter(
        x=a,
        y=b
    )

    layoot = dict(title='Wiadomości SKN x Z od 16.03.2018',
                  xaxis=dict(title="Data"),
                  yaxis=dict(title="Ilość Wiadomości")
                  )

    fig = dict(data=[trace], layout=layoot)

    return fig


if __name__ == '__main__':
    app.run_server()

