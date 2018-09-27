import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import plotly
import datetime

# set plotly credentials (possibly get that into a file in the future)

plotly.tools.set_credentials_file(username='vakken',
                                  api_key='akhX9iY5250qyEXX0mnd',
                                  stream_ids=["hmuf70c6b7",
                                              "5tfvc8uicq",
                                              "0c1oo8v3d2",
                                              "n0mec12ots",
                                              "a6u9gz17yy",
                                              "j4qdhudnvf"])

stream_ids = tls.get_credentials_file()['stream_ids']

def get_stream(no):

    outstream = go.scatter.Stream(
        token=stream_ids[no]
    )

    return outstream


def get_trace(x, y, name, no):

    outscatter = go.Scatter(
        x=x,
        y=y,
        name=name,
        stream=get_stream(no)
    )

    return outscatter

# this is the function for plotting an entire array
# will be functionally replaced with streaming (only the new value will be streamed)
# this will only be used once per day to regenerate the entire graph from database
# (could become troublesome as database grows bigger, only has 190 entries now, might have a million by 2020)


def plotarray(arr):

    # define the length of the array to stop myself from reusing it

    le = (len(arr))

    print("Begin plotting array...")

    # these need to be none instead of zero to avoid edge collapse on the graph

    a = [None] * le
    b = [None] * le
    med1000 = [None] * le
    med1500 = [None] * le
    med2000 = [None] * le

    # give ourselves some kind of index to run through the array

    k = 0

    # separate input data into arrays

    for i, j in arr:

        # only count the per day average (by only using midnight data nodes)

        if i.time() == datetime.time(0, 0, 0):

            # generate averages (per day)

            med1000[k] = k * 1000
            med1500[k] = k * 1500
            med2000[k] = k * 2000

        # separate the rest of the data into arrays

        a[k] = i
        b[k] = j
        print(i)
        print(j)

        k += 1

    # define data sets to prepare for plotting

    tracereal = get_trace(a, b, "Rzeczywista", 0)
    trace1000 = get_trace(a, med1000, "Średnia 1000", 1)
    trace1500 = get_trace(a, med1500, "Średnia 1500", 2)
    trace2000 = get_trace(a, med2000, "Średnia 2000", 3)

    # mash all of it together

    data = [tracereal, trace1000, trace1500, trace2000]

    # give the graphs some info

    layout = dict(title='Wiadomości SKN x Z od 16.03.2018',
                  xaxis=dict(title="Data"),
                  yaxis=dict(title="Ilość Wiadomości")
                  )

    # mash it even more

    fig = dict(data=data, layout=layout)

    # get it all out

    py.plot(fig, filename='overall', auto_open=False)

    print("Array plotting finished.")


def plotdailyarr(arr):

    # this needs to be bigger than previously because of how plotly likes to truncate things

    le: int = (len(arr)+1)

    print("Begin plottting daily array...")

    # make empties

    a = [0] * le
    b = [0] * le

    a[0] = arr[0][0]
    b[0] = 0

    # get our iterator

    k = 0

    for i, j in arr:

        # separating arr

        print(k)
        k += 1
        a[k] = i

        # since this is a per day value, we need to get rid of the empty space in the front

        if k > 1:
            print(arr[k-2][1])
            print(j)
            b[k] = j - arr[k-2][1]
            print(a[k], " : ", b[k])
        else:
            b[k] = 0

    # pinnacle of engineering, ladies and gentlemen, moving average!
    # TODO: get me some way to fill the last 20 values with more averageness

    n = 20
    cumsum, moving_aves = [0], []

    for i, x in enumerate(b, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= n:
            moving_ave = (cumsum[i] - cumsum[i - n]) / n
            moving_aves.append(moving_ave)

    # preparing data for plotting

    trace = get_trace(a, b, "Rzeczywista", 4)
    traceavg = get_trace(a, moving_aves, "Średnia Krocząca", 5)

    # mash mash mash

    data = [trace, traceavg]

    # describe describe

    layout = dict(title='Dzienna ilosć wiadomości SKN x Z od 16.03.2018',
                  xaxis=dict(title="Data"),
                  yaxis=dict(title="Ilość Wiadomości na dzień")
                  )

    # HULK, MASH!

    fig = dict(data=data, layout=layout)

    # Hulk, plot.

    py.plot(fig, filename='daily', auto_open=False)

    # hulk, print.

    print("Daily array plotting finished.")


def streamit(date, amt, graphtype):

    if graphtype == "daily":
        index = 4
    elif graphtype == "total":
        index = 0
    else:
        return TypeError("Wrong graph type supplied.")

    s = py.Stream(stream_ids[index])
    s.open()
    x = date
    y = amt
    s.write(dict(x=x, y=y))
    s.close()
    s.heartbeat()

    print("Streaming successful")
