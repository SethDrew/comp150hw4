import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np



def plot():


    data = []


    with open("results/power_bytime.txt") as f:
        results = f.read().split("\n")[:-1]

    names, yvals, xvals = [[x.split(":")[i] for x in results] for i in range(3)]    
    x_dict = {}
    y_dict = {}

    for i in range(len(names)):
        x_dict.setdefault(names[i], []).append(xvals[i])
        y_dict.setdefault(names[i], []).append(yvals[i])

    for name, xvals in x_dict.iteritems():
        data.append(go.Scatter(
                x=xvals, 
                y=y_dict[name],
                name=name,
                mode='lines',
            )
        )

    layout = dict(
        title="Power Over Time for all Simulation Objects",
        hovermode= 'closest',
        xaxis=dict(
            title="time",
            ),
        yaxis=dict(
            title="watts",
            )
        )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename="power_over_time")



def plot_totals():


    data = []


    with open("results/exit_power_totals.txt") as f:
        results = f.read().split("\n")[:-1]

    names, ammounts = [[x.split(":")[i] for x in results] for i in range(2)]    
   
    for name, ammount in zip(names, ammounts):
       fig = {
           'data': [{'labels': names,
                     'values': ammounts,
                     'type': 'pie'}],
           'layout': {'title': 'Total power usage by device'}
            }


    py.plot(fig, filename="power_over_time")

plot_totals()

