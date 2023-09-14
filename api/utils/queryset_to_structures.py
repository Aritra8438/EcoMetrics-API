from operator import itemgetter
from .output_serializer import serialize_queryset
from .create_figure import QUERY_LABEL_MAPPING


def transpose_table(table):
    """
    Transpose a table.

    This function takes a table represented as a list of lists and returns the transpose
    of the table.

    :param table: A list of lists representing the input table.
    :return: The transposed table as a list of lists.
    """
    num_rows = len(table)
    num_columns = len(table[0])
    transposed_table = [[0] * num_rows for _ in range(num_columns)]
    for i in range(num_columns):
        for j in range(num_rows):
            transposed_table[i][j] = table[j][i]
    return transposed_table


def convert_to_table(queryset, years, regions, query_type="population", pivot=0):
    """
    Convert a queryset into a table.

    This function takes a queryset, representing data points for specific years, regions,
    and query types, and converts it into a table format. The table can be customized
    to pivot data if needed. Serves "/table" endpoint

    :param queryset: A queryset containing data points with fields like 'country',
                    'year', and the specified 'query_type' (e.g., 'population',
                    'gdp_per_capita', 'forest_area').
    :param years: A list of years to include in the table.
    :param regions: A list of regions (e.g., countries) to include in the table.
    :param query_type: The type of query used to retrieve data (default is "population").
    :param pivot: If set to 1, the table will be transposed (pivoted). Default is 0.
    :return: A table represented as a list of lists.
    """
    years.sort()
    regions.sort()
    country_dict = {}
    year_dict = {}
    for index, country in enumerate(regions, start=1):
        country_dict[country] = index
    for index, year in enumerate(years, start=1):
        year_dict[year] = index
    num_years = len(years) + 1
    num_regions = len(regions) + 1
    table = [[0] * num_regions for _ in range(num_years)]
    table[0][0] = "↘"
    for i, _ in enumerate(regions):
        table[0][i + 1] = regions[i]
    for i, _ in enumerate(years):
        table[i + 1][0] = years[i]
    for element in queryset:
        country = element.country
        year = element.year
        if query_type == "gdp_per_capita":
            table[year_dict[year]][country_dict[country]] = element.gdp_per_capita
        elif query_type == "forest_area":
            table[year_dict[year]][country_dict[country]] = element.forest_area
        else:
            table[year_dict[year]][country_dict[country]] = element.population
    if pivot == 1:
        return transpose_table(table)
    return table


def convert_to_dicts(queryset, query_type="population"):
    """
    Convert a queryset into two dictionaries for country-year and country-value pairs.

    This function takes a queryset containing data points for specific countries and years,
    along with a specified 'query_type' (e.g., 'population', 'gdp_per_capita', 'forest_area').
    It converts the queryset into two dictionaries, one for storing arrays of years per country,
    and another for storing corresponding values per country. Serves "/graph" endpoint to create
    scatter plots.

    Example usage:
    - Input queryset may contain data like:
        [{"country": "India", "year": 2010, "value": 1350000000},
        {"country": "India", "year": 2011, "value": 1370000000},
        ...]

    - The resulting dictionaries would look like:
        country_year = {"India": [2010, 2011, ...]}
        country_value = {"India": [1350000000, 1370000000, ...]}

    :param queryset: A queryset containing data points with fields 'country', 'year',
                    and the specified 'query_type'.
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: Two dictionaries:
            - 'country_year': A dictionary mapping countries to arrays of years.
            - 'country_value': A dictionary mapping countries to arrays of corresponding values.
    """
    json_response = serialize_queryset(queryset, query_type)
    country_year = {}
    country_value = {}
    for obj in json_response:
        if obj["country"] not in country_year:
            country_year[obj["country"]] = []
        if obj["country"] not in country_value:
            country_value[obj["country"]] = []
        country_year[obj["country"]].append(int(obj["year"]))
        country_value[obj["country"]].append(obj["value"])
    return country_year, country_value


def convert_to_double_lists(queryset, num, query_type):
    """
    Convert a queryset into two sets of lists for top and bottom countries based on values.

    This function takes a queryset containing data points for specific countries and values,
    along with a specified 'query_type' (e.g., 'population', 'gdp_per_capita', 'forest_area').
    It converts the queryset into two sets of lists: one for the top 'num' countries with the
    highest values, and another for the bottom 'num' countries with the lowest values. Serves
    "/stats" endpoint

    :param queryset: A queryset containing data points with fields 'country', 'value',
                    and the specified 'query_type'.
    :param num: The number of top and bottom countries to retrieve.
    :param query_type: The type of query used to retrieve data.
    :return: Four lists:
                - 'array1': Values of the top 'num' countries.
                - 'label1': Country labels of the top 'num' countries.
                - 'array2': Values of the bottom 'num' countries.
                - 'label2': Country labels of the bottom 'num' countries.
    """
    json_response = serialize_queryset(queryset, query_type)
    value_country_list = []
    for obj in json_response:
        value_country_list.append((obj["value"], obj["country"]))
    value_country_list.sort(reverse=True)
    top_num_countries = value_country_list[:num]
    bottom_num_countries = value_country_list[-num:]
    array1 = []
    array2 = []
    label1 = []
    label2 = []
    for country in top_num_countries:
        array1.append(country[0])
        label1.append(country[1])
    for country in bottom_num_countries:
        array2.append(country[0])
        label2.append(country[1])
    return array1, label1, array2, label2


def convert_to_single_dict(queryset, query_type="population"):
    """
    Convert a queryset into a dictionary for plotting data.

    This function takes a queryset containing data points for specific years, countries, and a
    specified 'query_type' (e.g., 'population', 'gdp_per_capita', 'forest_area'). It converts
    the queryset into a dictionary suitable for plotting, where each key represents a data
    category, and the corresponding values are lists of data points. Serves "/graph" endpoints
    to create bar plots.

    Example usage:
    - Input queryset may contain data like:
        [{"country": "India", "year": 2010, "population": 1350000000},
        {"country": "India", "year": 2011, "population": 1370000000},
        ...]

    - The resulting dictionary would look like:
        {
            "year": [2010, 2011, ...],
            "country": ["India", "India", ...],
            "population": [1350000000, 1370000000, ...]
        }

    :param queryset: A queryset containing data points with fields 'country', 'year', and
                    the specified 'query_type'.
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: A dictionary suitable for plotting data, where keys represent data categories
            and values are lists of data points.
    """
    plot_dict = {"year": [], "country": [], query_type: []}
    for element in queryset:
        plot_dict["year"].append(element.year)
        plot_dict["country"].append(element.country)
        if query_type == "population":
            plot_dict[query_type].append(element.population)
        elif query_type == "gdp_per_capita":
            plot_dict[query_type].append(element.gdp_per_capita)
        else:
            plot_dict[query_type].append(element.forest_area)
    return plot_dict


def merge_comparable_querysets(
    queryset_param1, queryset_param2, parameter1_type, parameter2_type
):
    """
    Merge two comparable querysets into a single dictionary.

    This function takes two querysets containing data points for specific years, countries,
    and different comparable parameters (e.g., 'population' and 'gdp_per_capita'). It merges
    these querysets into a single dictionary for comparative analysis.

    :param queryset_population: A queryset containing data points for query_param1.
    :param queryset_gdp_per_capita: A queryset containing data points for query_param2.
    :param parameter1_type: The type of the first parameter (e.g., 'population').
    :param parameter2_type: The type of the second parameter (e.g., 'gdp_per_capita').
    :return: A dictionary with the following keys:
            - "year": A list of years.
            - "country": A list of countries.
            - The keys for parameter1_type and parameter2_type, mapped to lists of values.
    """
    sorted_param1 = sorted(queryset_param1, key=itemgetter("year", "country"))
    sorted_param2 = sorted(queryset_param2, key=itemgetter("year", "country"))
    years = []
    countries = []
    parameter1 = []
    parameter2 = []
    for id, element in enumerate(sorted_param1):
        years.append(element["year"])
        countries.append(element["country"])
        parameter1.append(element["value"])
        parameter2.append(sorted_param2[id]["value"])
    merged_dict = {
        "year": years,
        "country": countries,
        QUERY_LABEL_MAPPING[parameter1_type]: parameter1,
        QUERY_LABEL_MAPPING[parameter2_type]: parameter2,
    }
    return merged_dict
