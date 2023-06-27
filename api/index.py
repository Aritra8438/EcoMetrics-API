from flask import jsonify, request
import json

from api.database import app
from api.models import *
from api.utils.input_serializer import *
from api.utils.output_serializer import serialize_queryset


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
        return jsonify(json_response)
