
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------------------
# 1. PROJECT FOLDER AND DATASET
# -----------------------------------------

folder = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(folder, "sales_data.csv")

data = pd.read_csv(file_path)

print("\n======================================")
print("   E-COMMERCE SALES DATA ANALYSIS")
print("======================================")

# -----------------------------------------
# 2. DATA CLEANING
# -----------------------------------------

print("\n1. DATA CLEANING")

print("\nMissing Values:")
print(data.isnull().sum())

data = data.drop_duplicates()

required_columns = [
    "Order_ID", "Date", "Product", "Category",
    "Quantity", "Unit_Price", "City"
]

data = data.dropna(subset=required_columns)

data["Quantity"] = pd.to_numeric(
    data["Quantity"], errors="coerce"
)

data["Unit_Price"] = pd.to_numeric(
    data["Unit_Price"], errors="coerce"
)

data = data.dropna(
    subset=["Quantity", "Unit_Price"]
)

data = data[
    (data["Quantity"] > 0) &
    (data["Unit_Price"] >= 0)
]

data["Total_Sales"] = (
    data["Quantity"] * data["Unit_Price"]
)

if "Profit" not in data.columns:
    data["Profit"] = 0

data["Profit"] = pd.to_numeric(
    data["Profit"], errors="coerce"
).fillna(0)

data["Date"] = pd.to_datetime(
    data["Date"], errors="coerce"
)

data = data.dropna(subset=["Date"])

data["Month"] = data["Date"].dt.strftime("%B")

data.to_csv(
    os.path.join(folder, "cleaned_sales_data.csv"),
    index=False
)

print("\nData cleaning completed successfully!")

# -----------------------------------------
# 3. OVERALL SALES ANALYSIS
# -----------------------------------------

print("\n2. OVERALL SALES ANALYSIS")

total_sales = data["Total_Sales"].sum()

total_profit = data["Profit"].sum()

total_quantity = data["Quantity"].sum()

total_orders = data["Order_ID"].nunique()

average_order_value = total_sales / total_orders

print("\nTotal Sales       :", total_sales)
print("Total Profit      :", total_profit)
print("Total Quantity    :", total_quantity)
print("Total Orders      :", total_orders)
print("Average Order Value:", round(average_order_value, 2))

# -----------------------------------------
# 4. CATEGORY-WISE ANALYSIS
# -----------------------------------------

print("\n3. CATEGORY-WISE SALES ANALYSIS")

category_sales = data.groupby(
    "Category"
)["Total_Sales"].sum().sort_values(ascending=False)

category_profit = data.groupby(
    "Category"
)["Profit"].sum().sort_values(ascending=False)

print("\nCategory-wise Sales:")
print(category_sales)

print("\nCategory-wise Profit:")
print(category_profit)

# -----------------------------------------
# 5. BEST-SELLING PRODUCTS
# -----------------------------------------

print("\n4. BEST-SELLING PRODUCTS")

product_sales = data.groupby(
    "Product"
)["Quantity"].sum().sort_values(ascending=False)

top_products = product_sales.head(5)

print("\nTop 5 Best-Selling Products:")
print(top_products)

best_product = product_sales.idxmax()

print("\nBest-Selling Product:", best_product)

# -----------------------------------------
# 6. CITY-WISE SALES ANALYSIS
# -----------------------------------------

print("\n5. CITY-WISE SALES ANALYSIS")

city_sales = data.groupby(
    "City"
)["Total_Sales"].sum().sort_values(ascending=False)

print("\nCity-wise Sales:")
print(city_sales)

best_city = city_sales.idxmax()

print("\nHighest Sales City:", best_city)

# -----------------------------------------
# 7. PROFIT MARGIN ANALYSIS
# -----------------------------------------

print("\n6. PROFIT MARGIN ANALYSIS")

if total_sales > 0:
    profit_margin = (
        total_profit / total_sales
    ) * 100
else:
    profit_margin = 0

print(
    "Overall Profit Margin:",
    round(profit_margin, 2), "%"
)

# -----------------------------------------
# 8. MONTHLY SALES ANALYSIS
# -----------------------------------------

print("\n7. MONTHLY SALES ANALYSIS")

monthly_sales = data.groupby(
    data["Date"].dt.to_period("M")
)["Total_Sales"].sum()

print("\nMonthly Sales:")
print(monthly_sales)

# -----------------------------------------
# 9. EXCEL REPORT GENERATION
# -----------------------------------------

print("\n8. GENERATING EXCEL REPORT")

summary = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Total Quantity",
        "Total Orders",
        "Average Order Value",
        "Profit Margin (%)",
        "Best-Selling Product",
        "Highest Sales City"
    ],
    "Value": [
        total_sales,
        total_profit,
        total_quantity,
        total_orders,
        average_order_value,
        profit_margin,
        best_product,
        best_city
    ]
})

excel_path = os.path.join(
    folder, "sales_report.xlsx"
)

with pd.ExcelWriter(
    excel_path, engine="openpyxl"
) as writer:

    data.to_excel(
        writer,
        sheet_name="Cleaned Data",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Sales Summary",
        index=False
    )

    category_sales.to_frame(
        "Total Sales"
    ).to_excel(
        writer,
        sheet_name="Category Sales"
    )

    category_profit.to_frame(
        "Total Profit"
    ).to_excel(
        writer,
        sheet_name="Category Profit"
    )

    city_sales.to_frame(
        "Total Sales"
    ).to_excel(
        writer,
        sheet_name="City Analysis"
    )

    top_products.to_frame(
        "Quantity Sold"
    ).to_excel(
        writer,
        sheet_name="Top Products"
    )

    monthly_sales.to_frame(
        "Total Sales"
    ).to_excel(
        writer,
        sheet_name="Monthly Analysis"
    )

print("Excel report generated successfully!")

# -----------------------------------------
# 10. PROFESSIONAL SALES DASHBOARD
# -----------------------------------------

print("\n9. CREATING SALES DASHBOARD")

fig, axes = plt.subplots(
    2, 2, figsize=(12, 7)
)

fig.suptitle(
    "E-COMMERCE SALES ANALYSIS DASHBOARD",
    fontsize=18,
    fontweight="bold"
)

# Category-wise Sales
category_sales.plot(
    kind="bar",
    ax=axes[0, 0],
    title="Category-wise Sales",
    color="skyblue"
)

axes[0, 0].set_ylabel("Sales Amount")
axes[0, 0].tick_params(
    axis="x", rotation=30
)

# City-wise Sales
city_sales.plot(
    kind="bar",
    ax=axes[0, 1],
    title="City-wise Sales",
    color="orange"
)

axes[0, 1].set_ylabel("Sales Amount")
axes[0, 1].tick_params(
    axis="x", rotation=30
)

# Top 5 Products
top_products.plot(
    kind="bar",
    ax=axes[1, 0],
    title="Top 5 Best-Selling Products",
    color="green"
)

axes[1, 0].set_ylabel("Quantity Sold")
axes[1, 0].tick_params(
    axis="x", rotation=30
)

# Category-wise Profit
category_profit.plot(
    kind="pie",
    ax=axes[1, 1],
    autopct="%1.1f%%",
    title="Category-wise Profit",
    ylabel=""
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

dashboard_path = os.path.join(
    folder, "dashboard.png"
)

plt.savefig(
    dashboard_path,
    dpi=300,
    bbox_inches="tight"
)

print("Dashboard created successfully!")

plt.show()

# -----------------------------------------
# 11. BUSINESS INSIGHTS
# -----------------------------------------

print("\n10. BUSINESS INSIGHTS")

print("\nTotal Revenue:", total_sales)

print("Total Profit:", total_profit)

print("Best-Selling Product:", best_product)

print("Best Performing City:", best_city)

print(
    "Most Profitable Category:",
    category_profit.idxmax()
)

print(
    "Highest Sales Category:",
    category_sales.idxmax()
)

# -----------------------------------------
# 12. PROJECT COMPLETION
# -----------------------------------------

print("\n======================================")
print("       PROJECT COMPLETED")
print("======================================")

print("\nGenerated Files:")

print("1. cleaned_sales_data.csv")
print("2. sales_report.xlsx")
print("3. dashboard.png")

print("\nAll project outputs saved in:")
print(folder)

print("\nThank You!")
