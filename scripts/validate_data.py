from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

sales = pd.read_csv(RAW_DATA_DIR / "sales.csv")
inventory = pd.read_csv(RAW_DATA_DIR / "inventory.csv")
marketing = pd.read_csv(RAW_DATA_DIR / "marketing.csv")
products = pd.read_csv(RAW_DATA_DIR / "products.csv")


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def check(condition, passed_message, failed_message):
    if condition:
        print(f"[PASS] {passed_message}")
    else:
        print(f"[FAIL] {failed_message}")


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

print("=" * 70)
print("NovaRetail Data Validation")
print("=" * 70)


# 1. Product consistency
print("\n1. Product consistency")
print("-" * 70)

sales_products = set(sales["product_id"])
inventory_products = set(inventory["product_id"])
master_products = set(products["product_id"])

check(
    sales_products == master_products,
    "All sales products exist in products.csv",
    f"Sales contains products not found in products.csv: "
    f"{sales_products - master_products}"
)

check(
    inventory_products == master_products,
    "All inventory products exist in products.csv",
    f"Inventory contains products not found in products.csv: "
    f"{inventory_products - master_products}"
)


# 2. Product name/category consistency
print("\n2. Product attribute consistency")
print("-" * 70)

product_lookup = products.set_index("product_id")

sales_name_match = (
    sales["product_name"]
    == sales["product_id"].map(product_lookup["product_name"])
).all()

sales_category_match = (
    sales["category"]
    == sales["product_id"].map(product_lookup["category"])
).all()

inventory_name_match = (
    inventory["product_name"]
    == inventory["product_id"].map(product_lookup["product_name"])
).all()

inventory_category_match = (
    inventory["category"]
    == inventory["product_id"].map(product_lookup["category"])
).all()

check(
    sales_name_match,
    "Sales product names match products.csv",
    "Sales contains inconsistent product names"
)

check(
    sales_category_match,
    "Sales categories match products.csv",
    "Sales contains inconsistent product categories"
)

check(
    inventory_name_match,
    "Inventory product names match products.csv",
    "Inventory contains inconsistent product names"
)

check(
    inventory_category_match,
    "Inventory categories match products.csv",
    "Inventory contains inconsistent product categories"
)


# 3. Revenue calculation
print("\n3. Sales revenue calculation")
print("-" * 70)

calculated_revenue = (
    sales["units_sold"] * sales["avg_selling_price"]
)

revenue_difference = (
    sales["revenue"] - calculated_revenue
).abs().max()

check(
    revenue_difference < 0.01,
    "Sales revenue = units_sold × avg_selling_price",
    f"Revenue calculation mismatch. Maximum difference: "
    f"{revenue_difference:.2f}"
)


# 4. Inventory relationship
print("\n4. Inventory metrics")
print("-" * 70)

inventory_sum = (
    inventory["inventory_availability_pct"]
    + inventory["stockout_rate_pct"]
)

max_inventory_difference = (
    inventory_sum - 100
).abs().max()

check(
    max_inventory_difference < 0.01,
    "Inventory availability + stockout rate = 100%",
    f"Inventory metric mismatch. Maximum difference: "
    f"{max_inventory_difference:.2f}"
)


# 5. Quarter coverage
print("\n5. Quarter coverage")
print("-" * 70)

expected_quarters = {"Q1", "Q2", "Q3", "Q4"}

sales_quarters = set(sales["quarter"])
inventory_quarters = set(inventory["quarter"])
marketing_quarters = set(marketing["quarter"])

check(
    sales_quarters == expected_quarters,
    "Sales contains Q1-Q4",
    f"Unexpected sales quarters: {sales_quarters}"
)

check(
    inventory_quarters == expected_quarters,
    "Inventory contains Q1-Q4",
    f"Unexpected inventory quarters: {inventory_quarters}"
)

check(
    marketing_quarters == expected_quarters,
    "Marketing contains Q1-Q4",
    f"Unexpected marketing quarters: {marketing_quarters}"
)


# 6. Calculate quarterly revenue
print("\n6. Quarterly revenue")
print("-" * 70)

quarterly_revenue = (
    sales.groupby("quarter")["revenue"]
    .sum()
    .sort_index()
)

for quarter, revenue in quarterly_revenue.items():
    print(f"{quarter}: INR {revenue:,.2f}")


# 7. Q4 regional/category performance
print("\n7. Q4 regional/category performance")
print("-" * 70)

q4_sales = sales[sales["quarter"] == "Q4"]

q4_region_category = (
    q4_sales
    .groupby(["region", "category"])["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nQ4 revenue by region and category:")
print(q4_region_category.to_string())


# 8. Q4 inventory performance
print("\n8. Q4 inventory performance")
print("-" * 70)

q4_inventory = inventory[inventory["quarter"] == "Q4"]

q4_inventory_summary = (
    q4_inventory
    .groupby(["region", "category"])
    .agg(
        inventory_availability_pct=("inventory_availability_pct", "mean"),
        stockout_rate_pct=("stockout_rate_pct", "mean")
    )
    .round(2)
)

print(q4_inventory_summary.to_string())


# 9. Q4 marketing performance
print("\n9. Q4 marketing performance")
print("-" * 70)

q4_marketing = marketing[marketing["quarter"] == "Q4"]

q4_marketing_summary = (
    q4_marketing
    .groupby(["region", "category"])
    .agg(
        campaign_spend=("campaign_spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversion_rate_pct=("conversion_rate_pct", "mean"),
        revenue_attributed=("revenue_attributed", "sum")
    )
    .round(2)
)

print(q4_marketing_summary.to_string())


# ---------------------------------------------------------
# Completion
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("Validation completed.")
print("=" * 70)