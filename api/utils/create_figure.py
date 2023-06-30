import plotly.graph_objects as go


def create_figure(country_year, country_pop):
    fig = go.Figure()
    layout = go.Layout(
        title="Population vs Year Index",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Population"),
    )
    for country in country_year:
        fig.add_trace(
            go.Scatter(
                x=country_year[country],
                y=country_pop[country],
                mode="markers+lines",
                name=country,
            )
        )
    fig.update_layout(layout)
    return fig.to_html(full_html=False)
