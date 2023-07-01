from flask import jsonify, request, render_template
import json
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import *
from api.utils.queryset_to_structures import *
from api.utils.create_figure import create_figure


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
def get_image():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        country_year, country_population = convert_to_dicts(queryset)
        return create_figure(country_year, country_population)


@app.route("/stats")
def get_stats():
    if request.method == "GET":
        num = json.loads(request.args.get("Number"))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(Population.year.in_(years))
        json_response = serialize_queryset(queryset)
        res = []
        for obj in json_response:
            if obj["country"] != "World" and obj["country"] != "Less developed regions":
                res.append((obj["population"], obj["country"]))
        result = res[:num]
        values = []
        labels = []
        for item in result:
            values.append(item[0])
            labels.append(item[1])

        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "pie"}, {"type": "pie"}]],
            subplot_titles=[
                "Top {} countries".format(num),
                "Bottom {} countries".format(num),
            ],
        )

        fig.add_trace(
            go.Pie(
                values=values,
                labels=labels,
                name="Least Populated {} countries".format(num),
            ),
            row=1,
            col=1,
        )
        res.sort(reverse=True)
        result = res[:num]
        values = []
        labels = []
        for item in result:
            values.append(item[0])
            labels.append(item[1])
        fig.add_trace(
            go.Pie(
                values=values,
                labels=labels,
                name="Most Populated {} countries".format(num),
            ),
            row=1,
            col=2,
        )

        return fig.to_html(full_html=False)
