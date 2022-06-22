from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, HoverTool
from datetime import datetime
import numpy as np



TOOLTIPS = [
    ("Value", "$y"),
    ("Date", '$x{%F}')
]

FORMATTERS = {
    '$x' : 'datetime'
}

colors = ('navy', 'red')

def genChartData(obrvs):
    x = [[],[]]
    y = list()
    for obrv in obrvs:
        if('valueQuantity' in obrv):
            name = [obrv['code']['coding'][0]['display']]
            x[0].append(float(obrv['valueQuantity']['value']))
        elif('component' in obrv):
            name = ['','']
            for i, com in enumerate(obrv['component']):
                name[i] = com['code']['coding'][0]['display']
                x[i].append(int(com['valueQuantity']['value']))
        dt =  obrv['effectiveDateTime'].split('T')[0].split('-')
        y.append(datetime(int(dt[0]), int(dt[1]), int(dt[2])))
    return x, y, name

def makeChart(x, y, labels):
    fig = figure(x_axis_type="datetime")
    fig.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    for i, l in enumerate(x):
        if l:
            fig.line(y, l, line_width=2, color=colors[i], legend_label=labels[i])
            fig.circle(y, l, size=5, color=colors[i], alpha=0.5)
    fig.add_tools(HoverTool(
        tooltips=TOOLTIPS,
        formatters=FORMATTERS
    ))
    return fig