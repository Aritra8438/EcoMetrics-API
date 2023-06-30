from flask import jsonify, request, render_template
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import serialize_queryset
from flask import send_file


import matplotlib
from json import dumps
import plotly
from plotly import utils
import plotly.graph_objects as go
import matplotlib.pyplot as plt

matplotlib.use("Agg")

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


@app.route("/get_plot")
def get_image():
    # app = QtWidgets.QApplication()
    # win = QtWidgets.QWidget()
    # win.show()
    # app.exec()
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)
        country_year = {}
        country_pop = {}
        years_array = []
        pop_array = []
        for obj in json_response:
            if obj["country"] not in country_year:
                country_year[obj["country"]] = []
            if obj["country"] not in country_pop:
                country_pop[obj["country"]] = []
            country_year[obj["country"]].append(int(obj["year"]))
            country_pop[obj["country"]].append(obj["population"])

            years_array.append(obj["year"])
            pop_array.append(obj["population"])

        # fig = create_figure(years_array,pop_array)
        return create_fig(country_year, country_pop)


def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = BytesIO()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/png")


def create_figure(country_year, country_pop):
    fig = Figure()

    axis = fig.add_subplot(1, 1, 1)

    for country in country_year:
        xpoints = np.array(country_year[country])
        ypoints = np.array(country_pop[country])
        axis.plot(xpoints, ypoints)
    countries = []
    for country in country_year:
        countries.append(country)
    axis.legend(countries)

    return fig


def create_fig(country_year, country_pop):
    fig = go.Figure()
    layout = go.Layout(
        title="Population vs Year Index",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Population"),
    )
    for country in country_year:
        fig.add_trace(
            go.Scatter(
                x=country_year[country],
                y=country_pop[country],
                mode="lines",
                name=country,
            )
        )
    fig.update_layout(layout)
    return fig.to_html(full_html=False)
