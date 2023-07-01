from api.utils.output_serializer import serialize_queryset
from api.utils.infer_region import infer_region


def transpose_table(table):
    n = len(table)
    m = len(table[0])
    transposed_table = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            transposed_table[i][j] = table[j][i]
    return transposed_table


def convert_to_table(queryset, years, regions, pivot=0):
    years.sort()
    regions.sort()
    country_dict = {}
    year_dict = {}
    for index, country in enumerate(regions, start=1):
        country_dict[country] = index
    for index, year in enumerate(years, start=1):
        year_dict[year] = index
    n = len(years) + 1
    m = len(regions) + 1
    table = [[0] * m for _ in range(n)]
    table[0][0] = "↘"
    for i in range(len(regions)):
        table[0][i + 1] = regions[i]
    for i in range(len(years)):
        table[i + 1][0] = years[i]
    for element in queryset:
        country = element.country
        year = element.year
        population = element.population
        table[year_dict[year]][country_dict[country]] = population
    if pivot == 1:
        return transpose_table(table)
    return table


def convert_to_dicts(queryset):
    # Create two dictionaries to store the array corresponding to coutries. Will look like:
    # country_year["India"] = [2010, 2011, ...]
    json_response = serialize_queryset(queryset)
    country_year = {}
    country_population = {}
    for obj in json_response:
        if obj["country"] not in country_year:
            country_year[obj["country"]] = []
        if obj["country"] not in country_population:
            country_population[obj["country"]] = []
        country_year[obj["country"]].append(int(obj["year"]))
        country_population[obj["country"]].append(obj["population"])
    return country_year, country_population


def convert_to_double_lists(queryset, num):
    json_response = serialize_queryset(queryset)
    population_country_list = []
    for obj in json_response:
        population_country_list.append((obj["population"], obj["country"]))
    population_country_list.sort(reverse=True)
    top_num_countries = population_country_list[:num]
    bottom_num_countries = population_country_list[-num:]
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


def convert_to_single_dict(queryset):
    years = []
    countries = []
    populations = []
    plot_dict = {}
    for element in queryset:
        years.append(element.year)
        countries.append(element.country)
        populations.append(element.population)
    plot_dict["year"] = years
    plot_dict["country"] = countries
    plot_dict["population"] = populations
    return plot_dict
