from flask import jsonify, request, render_template
import json

from .database import app
from .models import *
from .utils.input_serializer import *
from .utils.output_serializer import *
from .utils.queryset_to_structures import *
from .utils.create_figure import *


@app.route("/")
def home():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/querybuilder")
def build_query():
    if request.method == "GET":
        return render_template("query_builder.html")


@app.route("/table")
def get_table_response():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        pivot = request.args.get("Pivot")
        if pivot != "Region" and pivot != "Year":
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


@app.route("/json")
def get_json_response():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
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


@app.route("/graph")
def get_graph_response():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
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


@app.route("/stats")
def get_stats_response():
    if request.method == "GET":
        from api.utils.infer_region import countries

        num = json.loads(request.args.get("Number"))
        num = min(num, 10)
        years = year_input_manager(json.loads(request.args.get("Year")))[:1]
        queryset = (
            Population.query.filter(
                Population.year.in_(years), Population.country.in_(countries)
            )
            .order_by(Population.population)
            .limit(num)
            .all()
        )
        queryset += (
            Population.query.filter(
                Population.year.in_(years), Population.country.in_(countries)
            )
            .order_by(Population.population.desc())
            .limit(num)
            .all()
        )
        array1, label1, array2, label2 = convert_to_double_lists(queryset, num)
        return create_pie(array1, label1, array2, label2, num)


if __name__ == "__main__":
    app.run()
