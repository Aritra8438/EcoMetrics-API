"""Module produces json objects"""
import json
from flask import jsonify, request, render_template, abort

from .database import app
from .models import Population
from .utils.infer_region import countries as country_list
from .utils.input_serializer import region_input_manager, year_input_manager
from .utils.output_serializer import serialize_queryset, serialize_pivoted_queryset
from .utils.queryset_to_structures import (
    convert_to_table,
    convert_to_dicts,
    convert_to_single_dict,
    convert_to_double_lists,
)
from .utils.create_figure import create_bar, create_pie, create_scatter
from .exceptions.custom import MissingParameterException


@app.route("/")
def home():
    if request.method == "GET":
        return render_template("index.html")
    abort("Method not allowed", 405)


@app.route("/querybuilder")
def build_query():
    if request.method == "GET":
        return render_template("query_builder.html")
    abort("Method not allowed", 405)


@app.route("/table")
def get_table_response():
    if request.method == "GET":
        if "Region" not in request.args:
            raise MissingParameterException("Region must be specified in the url")
        if "Year" not in request.args:
            raise MissingParameterException("Year must be specified in the url")
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        pivot = request.args.get("Pivot")
        if pivot not in ["Region", "Year"]:
            pivot = "Year"
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        if pivot == "Region":
            table = convert_to_table(queryset, years, cities + countries, 1)
            return render_template("table_view.html", table=table)
        table = convert_to_table(queryset, years, cities + countries)
        return render_template("table_view.html", table=table)
    abort("Method not allowed", 405)


@app.route("/json")
def get_json_response():
    if "Region" not in request.args:
        raise MissingParameterException("Region must be specified in the url")
    if "Year" not in request.args:
        raise MissingParameterException("Year must be specified in the url")
    if request.method == "GET":
        _, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        pivot = request.args.get("Pivot")
        if pivot == "Region":
            pivoted_queryset = []
            for country in countries:
                queryset = Population.query.filter(
                    Population.year.in_(years), Population.country == country
                )
                pivoted_queryset.append((country, queryset))
            json_response = serialize_pivoted_queryset(pivoted_queryset, "Year")
            return jsonify(json_response)
        if pivot == "Year":
            pivoted_queryset = []
            for year in years:
                queryset = Population.query.filter(
                    Population.country.in_(countries), Population.year == year
                )
                pivoted_queryset.append((year, queryset))
            json_response = serialize_pivoted_queryset(pivoted_queryset, "Region")
            return jsonify(json_response)
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)
        return jsonify(json_response)
    abort("Method not allowed", 405)


@app.route("/graph")
def get_graph_response():
    if request.method == "GET":
        _, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        plot = request.args.get("plot")
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        if plot == "bar":
            plot_dict = convert_to_single_dict(queryset)
            return create_bar(plot_dict)
        country_year, country_population = convert_to_dicts(queryset)
        return create_scatter(country_year, country_population)
    abort("Method not allowed", 405)


@app.route("/stats")
def get_stats_response():
    if request.method == "GET":
        num = json.loads(request.args.get("Number"))
        years = year_input_manager(json.loads(request.args.get("Year")))[:1]
        queryset = (
            Population.query.filter(
                Population.year.in_(years), Population.country.in_(country_list)
            )
            .order_by(Population.population)
            .limit(num)
            .all()
        )
        queryset += (
            Population.query.filter(
                Population.year.in_(years), Population.country.in_(country_list)
            )
            .order_by(Population.population.desc())
            .limit(num)
            .all()
        )
        array1, label1, array2, label2 = convert_to_double_lists(queryset, num)
        return create_pie(array1, label1, array2, label2, num)
    abort("Method not allowed", 405)


if __name__ == "__main__":
    app.run()
