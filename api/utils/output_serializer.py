# serialize the queryset to create an array
def serialize_queryset(queryset, many=True):
    json_response = []
    for element in queryset:
        json_response.append({
            "country": element.country,
            "year": element.year,
            "population": element.population
        })
    return json_response
