from api.exceptions.custom import InvalidParameterException
from . import infer_region


def region_input_manager(region_or_array):
    """
    Split input into cities and countries.

    Given an input that can be either a string representing a city or country, or a list
    containing a mix of city and country names, this function categorizes and separates
    the input into two lists: one for cities and another for countries.

    Example usage:
    - Input "India" => cities = [], countries = ["India"]
    - Input "Kolkata" => cities = ["Kolkata"], countries = []
    - Input ["India", "Kolkata"] => cities = ["Kolkata"], countries = ["India"]

    :param region_or_array: A string or list of strings representing regions, which can
                            be cities or countries.
    :return: A tuple containing two lists - cities and countries.
    """
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


def compare_input_manager(comparison_params):
    """
    Parse input and validate requested comparisons.

    This function takes either a string or a list of strings representing comparison parameters
    and ensures that the requested comparisons are valid and properly formatted.

    Example usage:
    - Input "population,forest_area" => Output ["population", "forest_area"]
    - Input ["population", "forest_area"] => Output ["population", "forest_area"]

    :param comparison_params: A string or list of strings representing requested comparison parameters.
    :return: A list of requested comparison parameters as strings.
    :raises InvalidParameterException: If the input is invalid or contains unsupported comparisons.
    """
    comparisons_available = ["gdp_per_capita", "population", "forest_area"]
    comparisons_requested = []
    if isinstance(comparison_params, list):
        if len(comparison_params) <= 1:
            raise InvalidParameterException(
                "Two comparables must be defined in the url"
            )
        comparisons_requested = [comparison_params[0], comparison_params[1]]
    else:
        comparisons_requested = comparison_params.split(",")
    for comparison in comparisons_requested:
        if comparison not in comparisons_available:
            raise InvalidParameterException(
                'Comparable should be one of "gdp_per_capita", "population", "forest_area"'
            )
    if len(comparisons_requested) == 1:
        raise InvalidParameterException("Two comparables must be defined in the url")
    return comparisons_requested


def year_input_manager(year_or_tuple_or_array, query_type="population"):
    """
    Parse and validate input representing years or year ranges.

    This function takes input that can be either a single year, a tuple representing a
    year range (start, stop, step), or a list of years. It validates the input and
    returns a list of years.

    Example usage:
    - Input 2021 => Output [2021]
    - Input [2021, 2022] => Output [2021, 2022]
    - Input "2001,2011,5" => Output [2001, 2006, 2011]

    :param year_or_tuple_or_array: Input representing years or year ranges.
    :param query_type: The type of query for which the years are intended.
                        Default is "population."
    :return: A list of years.
    :raises InvalidParameterException: If the input is invalid or contains unsupported years.
    """
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
    if isinstance(query_type, str):
        query_type = [query_type]
    if "forest_area" in query_type and str(max(years)) > str(2020):
        raise InvalidParameterException("We have Forest area percentage data upto 2020")
    if "gdp_per_capita" in query_type and str(max(years)) > str(2018):
        raise InvalidParameterException("We have GDP per capita data upto 2018")
    if "population" in query_type and str(max(years)) > str(2021):
        raise InvalidParameterException("We have population data upto 2021")
    return years
