import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


QUERY_LABEL_MAPPING = {
    "population": "Population",
    "gdp_per_capita": "GDP per capita",
    "forest_area": "Forest Area Percentage",
}


def create_scatter(
    country_year_dict, country_val_dict, user_theme, query_type="population"
):
    """
    Create a scatter plot for comparing a query type against years.

    This function generates a scatter plot using Plotly for comparing a specified query type
    (e.g., 'population', 'gdp_per_capita', 'forest_area') against years for multiple countries.

    :param country_year_dict: A dictionary mapping countries to arrays of years.
    :param country_val_dict: A dictionary mapping countries to arrays of corresponding values.
    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                        "aquamarine", "dark", "fluorescent", "blackpink").
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: HTML code representing the scatter plot.
    """

    fig = go.Figure()
    theme = set_theme(user_theme)
    layout = go.Layout(
        title=f"{QUERY_LABEL_MAPPING[query_type]} vs Year graph",
        xaxis={"title": "Year"},
        yaxis={"title": QUERY_LABEL_MAPPING[query_type]},
    )
    for country in country_year_dict:
        fig.add_trace(
            go.Scatter(
                x=country_year_dict[country],
                y=country_val_dict[country],
                mode="markers+lines",
                name=country,
            )
        )
    fig.update_layout(layout)
    if theme is not None:
        layout = go.Layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font_color=theme["font_color"],
            title_font_color=theme["title_font_color"],
        )
        fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_bar(plot_dict, user_theme, query_type="population"):
    """
    Create an animated bar plot for comparing a query type against years.

    This function generates an animated bar plot using Plotly Express for comparing a specified
    query type (e.g., 'population', 'gdp_per_capita', 'forest_area') against years for multiple
    countries. The animation is based on the year, and each bar represents a country.

    :param plot_dict: A dictionary containing data points for plotting, typically generated
                        by the 'convert_to_single_dict' function.
    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                        "aquamarine", "dark", "fluorescent", "blackpink").
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: HTML code representing the animated bar plot.
    """
    fig = px.bar(
        plot_dict,
        x="country",
        y=query_type,
        color="country",
        animation_frame="year",
        animation_group="country",
        barmode="group",
        title=f"{QUERY_LABEL_MAPPING[query_type]} vs Year bar plot",
        labels={"country": "Country", query_type: QUERY_LABEL_MAPPING[query_type]},
    )
    theme = set_theme(user_theme)
    if theme is not None:
        layout = go.Layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font_color=theme["font_color"],
            title_font_color=theme["title_font_color"],
        )
        fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_pie(array_labels1, array_labels2, num, user_theme, query_type="population"):
    """
    Create two pie charts for displaying data on the top and bottom countries.

    This function generates two pie charts side by side using Plotly, each representing data
    for either the top or bottom 'num' countries based on the specified query type (e.g.,
    'population', 'gdp_per_capita', 'forest_area').

    :param array_labels1: A tuple containing two lists - values and labels for the top countries.
    :param array_labels2: A tuple containing two lists - values and labels for the bottom countries.
    :param num: The number of top and bottom countries to display.
    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                        "aquamarine", "dark", "fluorescent", "blackpink").
    :param query_type: The type of query used to retrieve data (default is "population").
    :return: HTML code representing the two pie charts.
    """
    theme = set_theme(user_theme)
    pie = {"type": "pie"}
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[pie, pie]],
        subplot_titles=[
            f"Top {num} countries",
            f"Bottom {num} countries",
        ],
    )
    fig.add_trace(
        go.Pie(
            values=array_labels1[0],
            labels=array_labels1[1],
            name=f"Top {num}",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Pie(
            values=array_labels2[0],
            labels=array_labels2[1],
            name=f"Bottom {num}",
        ),
        row=1,
        col=2,
    )
    layout = go.Layout(title=f"Stats pie charts for {QUERY_LABEL_MAPPING[query_type]}")
    fig.update_layout(layout)
    if theme is not None:
        layout = go.Layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font_color=theme["font_color"],
            title_font_color=theme["title_font_color"],
        )
        fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_3d_plot(merged_dict, user_theme, parameter1_type, parameter2_type):
    """
    Create a 3D scatter plot.

    This function generates a 3D scatter plot using Plotly Express.

    :param merged_dict: A dictionary containing data to be plotted, including 'year',
                       'parameter1_type', 'parameter2_type', 'country', and other information.
    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                      "aquamarine", "dark", "fluorescent", "blackpink").
    :param parameter1_type: The type of the first parameter (e.g., "population",
                            "gdp_per_capita", "forest_area").
    :param parameter2_type: The type of the second parameter (e.g., "population",
                            "gdp_per_capita", "forest_area").
    :return: HTML code representing the 3D scatter plot.
    """
    theme = set_theme(user_theme)
    fig = px.scatter_3d(
        merged_dict,
        x="year",
        y=QUERY_LABEL_MAPPING[parameter1_type],
        z=QUERY_LABEL_MAPPING[parameter2_type],
        color="country",
        hover_data=["country"],
        title=f"3d plot for country, {QUERY_LABEL_MAPPING[parameter1_type]} and "
        + f"{QUERY_LABEL_MAPPING[parameter2_type]}",
    )
    if theme is not None:
        layout = go.Layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font_color=theme["font_color"],
            title_font_color=theme["title_font_color"],
        )
        fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_plot_with_secondary_axis(
    merged_dict, user_theme, parameter1_type, parameter2_type
):
    """
    Create a plot with a secondary y-axis to visualize two parameters over time.

    This function generates a plot with a secondary y-axis using Plotly Express,
    allowing the user to visualize and compare two parameters over time.

    :param merged_dict: A dictionary containing data to be plotted, including 'year',
                       'parameter1_type', 'parameter2_type', and other information.
    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                      "aquamarine", "dark", "fluorescent", "blackpink").
    :param parameter1_type: The type of the first parameter (e.g., "population",
                            "gdp_per_capita", "forest_area").
    :param parameter2_type: The type of the second parameter (e.g., "population",
                            "gdp_per_capita", "forest_area").
    :return: HTML code representing the plot with two y-axes.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    theme = set_theme(user_theme)
    fig.add_trace(
        go.Scatter(
            x=merged_dict["year"],
            y=merged_dict[QUERY_LABEL_MAPPING[parameter1_type]],
            name=QUERY_LABEL_MAPPING[parameter1_type],
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=merged_dict["year"],
            y=merged_dict[QUERY_LABEL_MAPPING[parameter2_type]],
            name=QUERY_LABEL_MAPPING[parameter2_type],
        ),
        secondary_y=True,
    )
    if theme is not None:
        layout = go.Layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font_color=theme["font_color"],
            title_font_color=theme["title_font_color"],
        )
        fig.update_layout(layout)
    fig.update_layout(
        title_text=f"{QUERY_LABEL_MAPPING[parameter1_type]} vs "
        + f"{QUERY_LABEL_MAPPING[parameter2_type]} visualization"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="year")

    # Set y-axes titles
    fig.update_yaxes(title_text="Population", secondary_y=False)
    fig.update_yaxes(title_text="GDP per capita", secondary_y=True)
    return fig.to_html(full_html=False)


def set_theme(user_theme):
    """
    Set plot theme based on a user-defined theme name.

    This function takes a user-defined theme name and returns a dictionary containing
    theme-related settings for a plot, including background colors, font colors, and title
    font colors.

    :param user_theme: A string specifying the user's desired theme (e.g., "light",
                        "aquamarine", "dark", "fluorescent", "blackpink").
    :return: A dictionary with theme settings, or None if the theme name is not recognized.
    """
    themes = {
        "black_pink": {
            "paper_bgcolor": "black",
            "plot_bgcolor": "pink",
            "font_color": "#E6A29E",
            "title_font_color": "#D3382D",
        },
        "fluorescent": {
            "paper_bgcolor": "#B2FF00",
            "plot_bgcolor": "#D0FC77",
            "font_color": "black",
            "title_font_color": "black",
        },
        "aqua_marine": {
            "paper_bgcolor": "#1E4967",
            "plot_bgcolor": "#ADD3EC",
            "font_color": "white",
            "title_font_color": "white",
        },
        "light": {
            "paper_bgcolor": "#A6BEBE",
            "plot_bgcolor": "#BDD0D0",
            "font_color": "black",
            "title_font_color": "black",
        },
        "dark": {
            "paper_bgcolor": "black",
            "plot_bgcolor": "#383C3C",
            "font_color": "#A5F207",
            "title_font_color": "#A5F207",
        },
    }
    if user_theme == "light":
        return themes["light"]
    if user_theme == "aquamarine":
        return themes["aqua_marine"]
    if user_theme == "dark":
        return themes["dark"]
    if user_theme == "fluorescent":
        return themes["fluorescent"]
    if user_theme == "blackpink":
        return themes["black_pink"]
    return None
