from flask import jsonify, request
import json

import database as database
from models import *
from utils.input_serializer import *
from utils.output_serializer import serialize_queryset

app = database.app


@app.route("/")
def serve():
    if request.method == "GET":
        cities, countries = region_input_manager(json.loads(request.args.get("Region")))
        years = year_input_manager(json.loads(request.args.get("Year")))
        queryset = Population.query.filter(
            Population.year.in_(years), Population.country.in_(countries)
        )
        json_response = serialize_queryset(queryset)
        return jsonify(json_response)
