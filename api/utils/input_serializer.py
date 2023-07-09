from api.exceptions.custom import InvalidParameterException
from . import infer_region


# Takes an array or a region, output will be two different arrays of city and country
# Input "India" => output cities = [], countries = ["India"]
# Input "Kolkata" => output cities = ["Kolkata"], countries = []
# Input ["India", "Kolkata"] => output cities = ["Kolkata"], countries = ["India"]
def region_input_manager(region_or_array):
    cities = []
    countries = []
    if isinstance(region_or_array, list):
        for region in region_or_array:
            spec, region = infer_region.infer_region(region)
            if spec == "city":
                cities.append(region)
            else:
                countries.append(region)
        return cities, countries
    return region_input_manager([region_or_array])


# Takes year or tuple or array, outputs an array
# Input 2021 => output [2021]
# Input [2021,2022] => output [2021,2022]
# Input "(2001,2011,5)" => output [2001, 2006, 2011]
def year_input_manager(year_or_tuple_or_array, query_type="population"):
    years = []
    if isinstance(year_or_tuple_or_array, list):
        years = year_or_tuple_or_array
    elif isinstance(year_or_tuple_or_array, str):
        start, stop, step = tuple(
            int(element)
            for element in tuple(year_or_tuple_or_array.split(",", maxsplit=2))
        )
        years = list(range(start, stop + 1, step))
    else:
        years = [year_or_tuple_or_array]
    if query_type == "gdp_per_capita" and str(max(years)) > str(2018):
        raise InvalidParameterException("We have GDP per capita data upto 2018")
    if query_type == "population" and str(max(years)) > str(2021):
        raise InvalidParameterException("We have population data upto 2021")
    return years
