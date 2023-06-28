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
