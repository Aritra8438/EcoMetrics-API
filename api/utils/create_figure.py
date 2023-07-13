import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


QUERY_LABEL_MAPPING = {
    "population": "Population",
    "gdp_per_capita": "GDP per capita",
    "forest_area": "Forest Area Percentage"
}


def create_scatter(
    country_year_dict, country_val_dict, user_theme, query_type="population"
):
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


def create_3d_plot(merged_dict, user_theme):
    theme = set_theme(user_theme)
    fig = px.scatter_3d(
        merged_dict,
        x="year",
        y="gdp_per_capita",
        z="population",
        color="country",
        hover_data=["country"],
        title="3d plot for country, population and GDP per capita",
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


def create_plot_with_secondary_axis(merged_dict, user_theme):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    theme = set_theme(user_theme)
    fig.add_trace(
        go.Scatter(
            x=merged_dict["year"],
            y=merged_dict["population"],
            name="Population",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=merged_dict["year"],
            y=merged_dict["gdp_per_capita"],
            name="GDP per capita",
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
    fig.update_layout(title_text="Population vs GDP per capita visualization")

    # Set x-axis title
    fig.update_xaxes(title_text="year")

    # Set y-axes titles
    fig.update_yaxes(title_text="Population", secondary_y=False)
    fig.update_yaxes(title_text="GDP per capita", secondary_y=True)
    return fig.to_html(full_html=False)


def set_theme(user_theme):
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
