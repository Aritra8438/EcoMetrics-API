import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from .theme import AquaMarine, light, dark, fluroscent, blackPink

def create_scatter(country_year_dict, country_pop_dict, user_theme ):
    fig = go.Figure()
    theme = set_theme(user_theme)
    layout = go.Layout(
        title="Population vs Year Index",
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor = theme["plot_bgcolor"],
        font_color = theme["font_color"],
        title_font_color = theme["title_font_color"]
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


def create_bar(plot_dict, user_theme):
    fig = px.bar(
        plot_dict,
        x="country",
        y="population",
        color="country",
        animation_frame="year",
        animation_group="country",
        barmode="group",
    )
    theme = set_theme(user_theme)
    layout = go.Layout(
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor = theme["plot_bgcolor"],
        font_color = theme["font_color"],
        title_font_color = theme["title_font_color"]
    )
    fig.update_layout(layout)
    return fig.to_html(full_html=False)


def create_pie(array1, label1, array2, label2, num, user_theme):
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
    layout = go.Layout(
        paper_bgcolor=theme["paper_bgcolor"],
        plot_bgcolor = theme["plot_bgcolor"],
        font_color = theme["font_color"],
        title_font_color = theme["title_font_color"]
    )
    fig.update_layout(layout)
    return fig.to_html(full_html=False)

def set_theme(user_theme):
    if user_theme is None or user_theme=="light" :
        theme = light
    if user_theme=="AquaMarine":
        theme = AquaMarine
    if user_theme=="dark":
        theme = dark
    if user_theme=="fluroscent":
        theme = fluroscent
    if user_theme=="blackPink":
        theme = blackPink
    return theme
  