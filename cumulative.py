import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


query = """
SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""


with sqlite3.connect("../db/lesson.db") as connection:
    df = pd.read_sql_query(query, connection)


def cumulative(row):
    totals_above = df["total_price"][0 : row.name + 1]
    return totals_above.sum()


df["cumulative"] = df.apply(cumulative, axis=1)

print(df)

ax = df.plot(
    kind="line",
    x="order_id",
    y="cumulative",
    color="teal",
    marker="o",
    figsize=(10, 6),
    legend=False,
)
# add a shaded area under the line for better visualization
ax.fill_between(
    df["order_id"],
    df["cumulative"],
    color="teal",
    alpha=0.10
)


ax.grid(axis="y", linestyle="--", alpha=0.4)  # y-lines
ax.set_title("Cumulative Revenue by Order", fontweight="bold", color="teal", pad=20)
ax.set_xlabel("Order ID", fontweight="bold", labelpad=12)
ax.set_ylabel("Cumulative Revenue", fontweight="bold", labelpad=12)

plt.tight_layout()
plt.show()
