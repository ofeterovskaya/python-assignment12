import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


query = """
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""


with sqlite3.connect("../db/lesson.db") as connection:
	employee_results = pd.read_sql_query(query, connection)


print(employee_results)
# sort the results by revenue in DESC order for better visualization
employee_results = employee_results.sort_values(
    by="revenue",
    ascending=False
)

revenue_chart = employee_results.plot(
	kind="bar",
	x="last_name",
	y="revenue",
	color="teal",
	legend=False,
	figsize=(10, 6),
)
revenue_chart.set_title("Employee Revenue", fontweight="bold", color="teal", pad=20)
revenue_chart.set_xlabel("Employee Last Name", fontweight="bold", labelpad=12)
revenue_chart.set_ylabel("Revenue", fontweight="bold", labelpad=12)

revenue_chart.grid(axis="y", linestyle="--", alpha=0.4)  # y-lines

for label in revenue_chart.get_xticklabels():
	label.set_rotation(45)
	label.set_ha("right")
plt.tight_layout()

plt.show()
