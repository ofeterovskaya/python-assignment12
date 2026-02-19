import plotly.express as px
import plotly.data as pldata


output_file = "wind.html"

df = pldata.wind(return_type="pandas")

print("First 10 rows:")
print(df.head(10))
print("\nLast 10 rows:")
print(df.tail(10))

strength_as_text = df["strength"].astype(str).str.replace(r"\s", "", regex=True)
strength_ranges = strength_as_text.str.split("-", n=1, expand=True)
start_values = strength_ranges[0].str.replace(r"[^\d.]", "", regex=True)
end_values = strength_ranges[1].str.replace(r"[^\d.]", "", regex=True)

start_numeric = start_values.astype(float)
end_numeric = end_values.astype(float)
df["strength"] = ((start_numeric + end_numeric) / 2).astype(float)

fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs Frequency by Direction",
    labels={"strength": "Strength", "frequency": "Frequency", "direction": "Direction"},
)

fig.update_layout(
    template="plotly_white",
    title=dict(
        text="Wind Strength vs Frequency by Direction",
        font=dict(size=20, color="coral", family="Arial Black"),
        y=0.96,
    ),
    xaxis_title=dict(text="<b>Strength (Beaufort Scale – Midpoint)</b>"),
    yaxis_title=dict(text="<b>Relative Frequency (%)</b>"),
    margin=dict(t=170),
)

fig.add_annotation(
    text="Strength is shown as the midpoint of Beaufort wind strength ranges.<br>"
    "Frequency represents how often each wind condition occurs.",
    xref="paper",
    yref="paper",
    x=0,
    y=1.14,
    showarrow=False,
    align="left",
    font=dict(size=12, color="gray"),
)


fig.update_traces(marker=dict(size=15))  # increase dot size for better visibility


fig.write_html(output_file, include_plotlyjs="cdn")

with open(output_file, "r", encoding="utf-8") as html_file:
    html_content = html_file.read()
    print(f"\n{output_file} loaded successfully ({len(html_content)} characters).")

fig.show()
