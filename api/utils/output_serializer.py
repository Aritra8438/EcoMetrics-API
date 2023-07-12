# serialize the queryset to create an array
def serialize_queryset(queryset, query_type="population"):
    json_response = []
    for element in queryset:
        json_response.append(
            {
                "country": element.country,
                "year": element.year,
                "value": element.gdp_per_capita
                if query_type == "gdp_per_capita"
                else element.population,
            }
        )
    return json_response


def serialize_pivoted_queryset(pivoted_queryset, not_pivot, query_type="population"):
    json_response = []
    for query in pivoted_queryset:
        pivot = query[0]
        queryset = query[1]
        json_array = []
        for obj in queryset:
            if not_pivot == "Year":
                if query_type == "population":
                    json_array.append({obj.year: obj.population})
                else:
                    json_array.append({obj.year: obj.gdp_per_capita})
            elif not_pivot == "Region":
                if query_type == "population":
                    json_array.append({obj.country: obj.population})
                else:
                    json_array.append({obj.country: obj.gdp_per_capita})
        json_response.append({pivot: json_array})
    return json_response
