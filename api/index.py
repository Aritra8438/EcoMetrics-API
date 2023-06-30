from flask import jsonify, request, render_template
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import serialize_queryset
from api.utils.create_figure import create_pie, create_bar, create_fig 



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
        
        return create_pie(json_response, num)

    
@app.route('/get_bar')
def get_bar():
    if request.method == "GET": 
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)   
                
        return create_bar(json_response) 

