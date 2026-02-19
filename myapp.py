from dash import Dash, Input, Output, dcc, html
import plotly.express as px


df = px.data.gapminder()
countries = df["country"].drop_duplicates()

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.H1("GDP Per Capita Growth", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": country, "value": country} for country in countries],
            value="Canada",
            clearable=False,
        ),
        dcc.Graph(id="gdp-growth"),
    ]
)


@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value"),
)
def update_graph(country_name):
    filtered_df = df[df["country"] == country_name]
    fig = px.line(
        filtered_df,
        x="year",
        y="gdpPercap",
        title=f"GDP Per Capita Growth for {country_name}",
        markers=True,
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
