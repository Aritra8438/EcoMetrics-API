import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def create_scatter(country_year_dict, country_pop_dict):
    fig = go.Figure()
    layout = go.Layout(
        title="Population vs Year Index",
        xaxis="Year",
        yaxis="Population",
    )
    for country in country_year_dict:
        fig.add_trace(
            go.Scatter(
                x=country_year_dict[country],
                y=country_pop_dict[country],
                mode="markers+lines",
                name=country,
            )
        )
    fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_bar(plot_dict):
    fig = px.bar(
        plot_dict,
        x="country",
        y="population",
        color="country",
        animation_frame="year",
        animation_group="country",
        barmode="group",
    )
    return fig.to_html(full_html=False)


def create_pie(array1, label1, array2, label2, num):
    pie = {"type": "pie"}
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[pie, pie]],
        subplot_titles=[
            f"Top {num} countries",
            "Bottom {num} countries",
        ],
    )
    fig.add_trace(
        go.Pie(
            values=array1,
            labels=label1,
            name=f"Top {num}",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Pie(
            values=array2,
            labels=label2,
            name=f"Bottom {num}",
        ),
        row=1,
        col=2,
    )
    return fig.to_html(full_html=False)
