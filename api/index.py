from flask import jsonify, request
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import *


@app.route("/")
def hello():
    if request.method == "GET":
        return "Hello world"


@app.route("/api")
def serve():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        pivot = request.args.get("pivot")
        if pivot == "Region":
            pivoted_queryset = []
            for country in countries:
                queryset = Population.query.filter(
                    Population.year.in_(years), Population.country == country
                )
                pivoted_queryset.append((country, queryset))
            json_response = serialize_pivoted_queryset(pivoted_queryset, "Year")
            return jsonify(json_response)
        elif pivot == "Year":
            pivoted_queryset = []
            for year in years:
                queryset = Population.query.filter(
                    Population.country.in_(countries), Population.year == year
                )
                pivoted_queryset.append((year, queryset))
            json_response = serialize_pivoted_queryset(pivoted_queryset, "Region")
            return jsonify(json_response)
        else:
            queryset = Population.query.filter(
                Population.year.in_(years), Population.country.in_(countries)
            )
            json_response = serialize_queryset(queryset)
            return jsonify(json_response)
