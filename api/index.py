"""Module produces json objects"""
import json
from flask import jsonify, request, render_template, abort
from flask import url_for  # pylint: disable=W0611

from .database import app
from .models import Population, GDPperCapita, ForestArea
from .utils.infer_region import countries as country_list
from .utils.input_serializer import (
    region_input_manager,
    year_input_manager,
    compare_input_manager,
)
from .utils.output_serializer import serialize_queryset, serialize_pivoted_queryset
from .utils.queryset_to_structures import (
    convert_to_table,
    convert_to_dicts,
    convert_to_single_dict,
    convert_to_double_lists,
    merge_comparable_querysets,
)
from .utils.create_figure import (
    create_bar,
    create_pie,
    create_scatter,
    create_3d_plot,
    create_plot_with_secondary_axis,
    QUERY_LABEL_MAPPING,
)
from .exceptions.custom import MissingParameterException, InvalidParameterException

QUERY_MODEL_MAPPING = {
    "population": Population,
    "gdp_per_capita": GDPperCapita,
    "forest_area": ForestArea,
}


@app.route("/")
def home():
    if request.method == "GET":
        return render_template("index.html")
    abort("Method not allowed", 405)


@app.route("/api-documentation")
def documentation():
    if request.method == "GET":
        return render_template("api-documentation.html")
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
        try:
            cities, countries = region_input_manager(
                json.loads(request.args.get("Region"))
            )
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Region should either be a string enclosed by quotation or an array of them"
            ) from json_decode_error
        query_type = request.args.get("Query_type", default="population")
        try:
            years = year_input_manager(json.loads(request.args.get("Year")), query_type)
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Year should either be a Number, array of number or a string of tuple"
            ) from json_decode_error
        pivot = request.args.get("Pivot")
        if pivot not in ["Region", "Year"]:
            pivot = "Year"
        queryset = QUERY_MODEL_MAPPING[query_type].query.filter(
            QUERY_MODEL_MAPPING[query_type].year.in_(years),
            QUERY_MODEL_MAPPING[query_type].country.in_(countries),
        )
        if pivot == "Region":
            table = convert_to_table(queryset, years, cities + countries, query_type, 1)
            return render_template(
                "table_view.html",
                table=table,
                table_name=QUERY_LABEL_MAPPING[query_type],
            )
        table = convert_to_table(queryset, years, cities + countries, query_type)
        return render_template(
            "table_view.html", table=table, table_name=QUERY_LABEL_MAPPING[query_type]
        )
    abort("Method not allowed", 405)


@app.route("/json")
def get_json_response():
    if request.method == "GET":
        if "Region" not in request.args:
            raise MissingParameterException("Region must be specified in the url")
        if "Year" not in request.args:
            raise MissingParameterException("Year must be specified in the url")
        query_type = request.args.get("Query_type", default="population")
        try:
            _, countries = region_input_manager(json.loads(request.args.get("Region")))
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Region should either be a string enclosed by quotation or an array of them"
            ) from json_decode_error
        try:
            years = year_input_manager(json.loads(request.args.get("Year")), query_type)
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Year should either be a Number, array of number or a string of tuple"
            ) from json_decode_error
        pivot = request.args.get("Pivot")
        if pivot == "Region":
            pivoted_queryset = []
            for country in countries:
                queryset = QUERY_MODEL_MAPPING[query_type].query.filter(
                    QUERY_MODEL_MAPPING[query_type].year.in_(years),
                    QUERY_MODEL_MAPPING[query_type].country == country,
                )
                pivoted_queryset.append((country, queryset))
            json_response = serialize_pivoted_queryset(
                pivoted_queryset, "Year", query_type
            )
            return jsonify(json_response)
        if pivot == "Year":
            pivoted_queryset = []
            for year in years:
                queryset = QUERY_MODEL_MAPPING[query_type].query.filter(
                    QUERY_MODEL_MAPPING[query_type].country.in_(countries),
                    QUERY_MODEL_MAPPING[query_type].year == year,
                )
                pivoted_queryset.append((year, queryset))
            json_response = serialize_pivoted_queryset(
                pivoted_queryset, "Region", query_type
            )
            return jsonify(json_response)
        queryset = QUERY_MODEL_MAPPING[query_type].query.filter(
            QUERY_MODEL_MAPPING[query_type].year.in_(years),
            QUERY_MODEL_MAPPING[query_type].country.in_(countries),
        )
        json_response = serialize_queryset(queryset, query_type)
        return jsonify(json_response)
    abort("Method not allowed", 405)


@app.route("/graph")
def get_graph_response():
    if request.method == "GET":
        if "Region" not in request.args:
            raise MissingParameterException("Region must be specified in the url")
        if "Year" not in request.args:
            raise MissingParameterException("Year must be specified in the url")
        query_type = request.args.get("Query_type", default="population")
        try:
            _, countries = region_input_manager(json.loads(request.args.get("Region")))
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Region should either be a string enclosed by quotation or an array of them"
            ) from json_decode_error
        try:
            years = year_input_manager(json.loads(request.args.get("Year")), query_type)
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Year should either be a Number, array of number or a string of tuple"
            ) from json_decode_error
        plot = request.args.get("Plot")
        user_theme = request.args.get("Theme")
        queryset = QUERY_MODEL_MAPPING[query_type].query.filter(
            QUERY_MODEL_MAPPING[query_type].year.in_(years),
            QUERY_MODEL_MAPPING[query_type].country.in_(countries),
        )
        if plot == "bar":
            plot_dict = convert_to_single_dict(queryset, query_type)
            return create_bar(plot_dict, user_theme, query_type)
        country_year, country_value = convert_to_dicts(queryset, query_type)
        return create_scatter(country_year, country_value, user_theme, query_type)
    abort("Method not allowed", 405)


@app.route("/stats")
def get_stats_response():
    if request.method == "GET":
        if "Number" not in request.args:
            raise MissingParameterException(
                "Number of comparables must be specified in the url"
            )
        if "Year" not in request.args:
            raise MissingParameterException("Year must be specified in the url")
        query_type = request.args.get("Query_type", default="population")
        num = json.loads(request.args.get("Number"))
        user_theme = request.args.get("Theme")
        try:
            years = year_input_manager(
                json.loads(request.args.get("Year")), query_type
            )[:1]
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Year should either be a Number, array of number or a string of tuple"
            ) from json_decode_error
        order_entity = Population.population
        if query_type == "gdp_per_capita":
            order_entity = GDPperCapita.gdp_per_capita
        elif query_type == "forest_area":
            order_entity = ForestArea.forest_area
        queryset = (
            QUERY_MODEL_MAPPING[query_type]
            .query.filter(
                QUERY_MODEL_MAPPING[query_type].year.in_(years),
                QUERY_MODEL_MAPPING[query_type].country.in_(country_list),
            )
            .order_by(order_entity)
            .limit(num)
            .all()
        )
        queryset += (
            QUERY_MODEL_MAPPING[query_type]
            .query.filter(
                QUERY_MODEL_MAPPING[query_type].year.in_(years),
                QUERY_MODEL_MAPPING[query_type].country.in_(country_list),
            )
            .order_by(order_entity.desc())
            .limit(num)
            .all()
        )
        array1, label1, array2, label2 = convert_to_double_lists(
            queryset, num, query_type
        )
        return create_pie(
            [array1, label1],
            [array2, label2],
            num=num,
            user_theme=user_theme,
            query_type=query_type,
        )
    abort("Method not allowed", 405)


@app.route("/compare")
def compare():
    if request.method == "GET":
        if "Region" not in request.args:
            raise MissingParameterException("Region must be specified in the url")
        if "Year" not in request.args:
            raise MissingParameterException("Year must be specified in the url")
        if "Compare" not in request.args:
            raise MissingParameterException("Comparables must be specified in the url")
        try:
            [first_parameter, second_parameter] = compare_input_manager(
                json.loads(request.args.get("Compare"))
            )
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Comparison parameters should either be an array or a string of tuple"
            ) from json_decode_error
        try:
            years = year_input_manager(
                json.loads(request.args.get("Year")),
                [first_parameter, second_parameter],
            )
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Year should either be a Number, array of number or a string of tuple"
            ) from json_decode_error
        try:
            _, countries = region_input_manager(json.loads(request.args.get("Region")))
        except json.decoder.JSONDecodeError as json_decode_error:
            raise InvalidParameterException(
                "The Region should either be a string enclosed by quotation or an array of them"
            ) from json_decode_error
        plot_type = request.args.get("Type")
        user_theme = request.args.get("Theme")
        queryset_param1 = QUERY_MODEL_MAPPING[first_parameter].query.filter(
            QUERY_MODEL_MAPPING[first_parameter].year.in_(years),
            QUERY_MODEL_MAPPING[first_parameter].country.in_(countries),
        )
        queryset_param2 = QUERY_MODEL_MAPPING[second_parameter].query.filter(
            QUERY_MODEL_MAPPING[second_parameter].year.in_(years),
            QUERY_MODEL_MAPPING[second_parameter].country.in_(countries),
        )
        json_response_parameter1 = serialize_queryset(queryset_param1, first_parameter)
        json_response_parameter2 = serialize_queryset(queryset_param2, second_parameter)
        merged_dict = merge_comparable_querysets(
            json_response_parameter1,
            json_response_parameter2,
            first_parameter,
            second_parameter,
        )
        if plot_type == "2d":
            return create_plot_with_secondary_axis(
                merged_dict, user_theme, first_parameter, second_parameter
            )
        return create_3d_plot(
            merged_dict, user_theme, first_parameter, second_parameter
        )
    abort("Method not allowed", 405)


if __name__ == "__main__":
    app.run()
