from operator import itemgetter
from .output_serializer import serialize_queryset
from .create_figure import QUERY_LABEL_MAPPING


def transpose_table(table):
    """Function transposes the table"""
    num_rows = len(table)
    num_columns = len(table[0])
    transposed_table = [[0] * num_rows for _ in range(num_columns)]
    for i in range(num_columns):
        for j in range(num_rows):
            transposed_table[i][j] = table[j][i]
    return transposed_table


def convert_to_table(queryset, years, regions, query_type="population", pivot=0):
    """Converts queryset to table"""
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
    """Create two dictionaries to store the array corresponding to coutries. Will look like:"""
    # country_year["India"] = [2010, 2011, ...]
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
    plot_dict = {"year": [], "country": [], query_type: []}
    for element in queryset:
        plot_dict["year"].append(element.year)
        plot_dict["country"].append(element.country)
        if query_type == "population":
            plot_dict[query_type].append(element.population)
        else:
            plot_dict[query_type].append(element.gdp_per_capita)
    return plot_dict


def merge_comparable_querysets(
    queryset_population, queryset_gdp_per_capita, parameter1_type, parameter2_type
):
    sorted_population_list = sorted(
        queryset_population, key=itemgetter("year", "country")
    )
    sorted_gdp_per_capita_list = sorted(
        queryset_gdp_per_capita, key=itemgetter("year", "country")
    )
    years = []
    countries = []
    parameter1 = []
    parameter2 = []
    for idx, element in enumerate(sorted_population_list):
        years.append(element["year"])
        countries.append(element["country"])
        parameter1.append(element["value"])
        parameter2.append(sorted_gdp_per_capita_list[idx]["value"])
    merged_dict = {
        "year": years,
        "country": countries,
        QUERY_LABEL_MAPPING[parameter1_type]: parameter1,
        QUERY_LABEL_MAPPING[parameter2_type]: parameter2,
    }
    return merged_dict
