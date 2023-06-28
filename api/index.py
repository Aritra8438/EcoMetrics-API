from flask import jsonify, request, render_template
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import *
from api.utils.json_response_to_table import *


@app.route("/")
def hello():
    if request.method == "GET":
        return render_template("index.html", content=69)


@app.route("/table")
def get_table_response():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        pivot = request.args.get("pivot")
        if pivot is None:
            pivot = "Year"
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        if pivot == "Region":
            table = convert_to_table(queryset, years, cities + countries, 1)
            return render_template("table_view.html", table=table)
        elif pivot == "Year":
            table = convert_to_table(queryset, years, cities + countries)
            return render_template("table_view.html", table=table)


@app.route("/api")
def get_json_response():
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
