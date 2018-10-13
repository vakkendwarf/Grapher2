import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *
import Sql as Sqli
from os import system, name
from collections import deque
import datetime

first = True


def is_first():
    global first
    if first:
        first = False
        return True
    else:
        return False


def clear():
    if name == 'nt':
        _ = system('cls')


def get_db_output(n):

    arr = Sqli.pull_last_n_entries(n)

    index = []
    date = []
    amount = []

    index, date, amount = list(map(list, zip(*arr)))

    return date, amount


def get_last_entry():
    newentry = Sqli.pull_last_n_entries(1)
    index, date, amount = list(map(list, zip(*newentry)))
    return date[0], amount[0]


def set_up_server():
    myapp = dash.Dash()
    myserver = myapp.server

    return myapp, myserver


def set_up_layout():
    app.layout = html.Div([
        html.H1('Grapher 2.2 on C v5.0'),
        dcc.Graph(id='overall'),
        dcc.Graph(id='overalltwothousand'),
        dcc.Interval(id='dynamic-update', interval=500, n_intervals=0),
    ])

    return app.layout


print("GETTING DB CONTENTS FOR THE FIRST TIME")

locdate, locamount = get_db_output(100)
locdate = deque(locdate)
locamount = deque(locamount)

print("SETTING UP SERVER")

app, server = set_up_server()

print("SETTING UP LAYOUT")

app.layout = set_up_layout()

print("STARTING INTERVAL UPDATE")


@app.callback(Output('overall', 'figure'), [Input('dynamic-update', 'n_intervals')])
def update_graph(n):

    clear()

    print("UPDATING GRAPH...")

    if is_first():
        a, b = locdate, locamount
    else:
        newdate, newamount = get_last_entry()
        newdate = datetime.datetime.now()
        print(newdate)
        print(str(newamount))
        locdate.append(newdate)
        locamount.append(newamount)
        locdate.popleft()
        locamount.popleft()
        a, b = locdate, locamount

    a = list(a)
    b = list(b)
    trace = Scatter(
        x=a,
        y=b
    )

    graphlayout = dict(title='Wiadomości SKN x Z od 16.03.2018 ({})'.format(n),
                  xaxis=dict(title="Data"),
                  yaxis=dict(title="Ilość Wiadomości")
                  )
    fig = dict(data=[trace], layout=graphlayout)
    return fig


if __name__ == '__main__':
    app.run_server()

