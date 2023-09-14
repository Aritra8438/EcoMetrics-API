def serialize_queryset(queryset, query_type="population"):
    """
    Serialize a queryset into an array of dictionaries.

    This function takes a queryset containing data points for specific countries, years,
    and a specified 'query_type' (e.g., 'population', 'gdp_per_capita', 'forest_area').
    It serializes the queryset by converting it into an array of dictionaries, where each
    dictionary represents a data point with fields 'country', 'year', and 'value'.

    Example usage:
    - Input queryset may contain data like:
        [{"country": "India", "year": 2010, "population": 1350000000},
        {"country": "India", "year": 2011, "population": 1370000000},
        ...]

    - The resulting array of dictionaries would look like:
        [
            {"country": "India", "year": 2010, "value": 1350000000},
            {"country": "India", "year": 2011, "value": 1370000000},
            ...
        ]

    :param queryset: A queryset containing data points with fields 'country', 'year',
                    and the specified 'query_type'.
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: An array of dictionaries, where each dictionary represents a data point.
    """
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
    """
    Serialize a pivoted queryset into an array of dictionaries.

    This function takes a pivoted queryset containing data points for specific years or regions,
    and a specified 'query_type' (e.g., 'population', 'gdp_per_capita', 'forest_area'). It serializes
    the pivoted queryset by converting it into an array of dictionaries, where each dictionary represents
    a data point with fields based on the pivot and 'query_type'.

    :param pivoted_queryset: A pivoted queryset containing data points based on the pivot (e.g., 'Year'
                            or 'Region').
    :param not_pivot: The field that is not part of the pivot ('Year' or 'Region').
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: An array of dictionaries, where each dictionary represents a data point.
            The structure of the dictionaries depends on the pivot and query_type.
    """
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
