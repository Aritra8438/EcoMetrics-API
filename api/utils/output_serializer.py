# serialize the queryset to create an array
def serialize_queryset(queryset, query_type="population"):
    json_response = []
    for element in queryset:
        if query_type == "gdp_per_capita":
            value = element.gdp_per_capita
        elif query_type == "population":
            value = element.population
        else:
            value = element.forest_area
        json_response.append(
            {
                "country": element.country,
                "year": element.year,
                "value": value,
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
                elif query_type == "forest_area":
                    json_array.append({obj.year: obj.forest_area})
                else:
                    json_array.append({obj.year: obj.gdp_per_capita})
            elif not_pivot == "Region":
                if query_type == "population":
                    json_array.append({obj.country: obj.population})
                elif query_type == "forest_area":
                    json_array.append({obj.country: obj.forest_area})
                else:
                    json_array.append({obj.country: obj.gdp_per_capita})
        json_response.append({pivot: json_array})
    return json_response
