from flask import jsonify, request, render_template
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import serialize_queryset
from flask import send_file


import matplotlib
from plotly.subplots import make_subplots
from queue import PriorityQueue
from json import dumps
import plotly
from plotly import utils
import plotly.graph_objects as go
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import ipywidgets
# plt.switch_backend('QtAgg4')
# plt.ion()
# matplotlib.use('QtAgg')
from matplotlib.figure import Figure
from matplotlib import *

import numpy as np
from io import BytesIO
from PySide6 import QtWidgets




@app.route("/")
def hello():
    if request.method == "GET":
        return "Hello world"


@app.route("/api")
def serve():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)
        
        # print(json_response)
        return jsonify(json_response)


@app.route('/get_plot')
def get_image():
    
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)
        country_year = {}
        country_pop = {}
        
        for obj in json_response:
            if(obj['country'] not in country_year):
                country_year[obj['country']]=[]
            if(obj['country'] not in country_pop):
                country_pop[obj['country']]=[]    
            country_year[obj['country']].append(int(obj['year']))
            country_pop[obj['country']].append(obj['population'])
               
        # fig = create_figure(years_array,pop_array)
        return create_fig(country_year,country_pop)

@app.route('/get_stats')
def get_stats():
    if request.method == "GET":
        num = json.loads(request.args.get("Number"))
        
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(Population.year.in_(years))
        
        json_response = serialize_queryset(queryset)
        res = []
        for obj in json_response:
            if(obj['country']!='World' and obj['country']!='Less developed regions'):
                res.append((obj['population'], obj['country']))
        result = res[:num]
        values=[]
        labels=[]
        for item in result:
            values.append(item[0])
            labels.append(item[1]) 
        
        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], 
                            subplot_titles=[ "Top {} countries".format(num), "Bottom {} countries".format(num)])
                                            
 
        fig.add_trace(go.Pie(values=values, labels=labels, name="Least Populated {} countries".format(num)),row=1, col=1)           
        res.sort(reverse=True)    
        result = res[:num]
        values=[]
        labels=[]
        for item in result:
            values.append(item[0])
            labels.append(item[1])
        fig.add_trace(go.Pie(values=values, labels=labels, name ="Most Populated {} countries".format(num)), row=1, col=2)  
                       
        return fig.to_html(full_html=False)

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')

def create_figure(country_year,country_pop):
    fig = Figure()
    
    axis = fig.add_subplot(1, 1, 1)
    
    for country in country_year :
        
        xpoints = np.array(country_year[country])
        ypoints = np.array(country_pop[country])
        axis.plot(xpoints, ypoints)
    countries=[]
    for country in country_year:
        countries.append(country)
    axis.legend(countries)        
    
    return fig

def create_fig(country_year,country_pop):
    fig = go.Figure()
    layout = go.Layout(
    title='Population vs Year Index',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Population')
    )
    for country in country_year :
        fig.add_trace(go.Scatter(x=country_year[country], y=country_pop[country],mode="lines", 
                                 name=country))
    fig.update_layout(layout)    
    return fig.to_html(full_html=False)
    