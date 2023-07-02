# serialize the queryset to create an array
def serialize_queryset(queryset):
    json_response = []
    for element in queryset:
        json_response.append(
            {
                "country": element.country,
                "year": element.year,
                "population": element.population,
            }
        )
    return json_response


def serialize_pivoted_queryset(pivoted_queryset, not_pivot):
    json_response = []
    for query in pivoted_queryset:
        pivot = query[0]
        queryset = query[1]
        json_array = []
        for obj in queryset:
            if not_pivot == "Year":
                json_array.append({obj.year: obj.population})
            elif not_pivot == "Region":
                json_array.append({obj.country: obj.population})
        json_response.append({pivot: json_array})
    return json_response
