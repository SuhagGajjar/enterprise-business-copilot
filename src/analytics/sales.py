from src.data.loader import load_sales, load_inventory, load_marketing


def get_q4_revenue_by_region():
    """Calculate Q4 revenue by region."""
    sales = load_sales()

    q4_sales = sales[sales["quarter"] == "Q4"]

    revenue_by_region = (
        q4_sales
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    return revenue_by_region
    
def get_business_summary(quarter, region, category):
    """Return key business metrics for a quarter, region, and category."""

    sales = load_sales()
    inventory = load_inventory()
    marketing = load_marketing()

    # Validate input values
    valid_quarters = sales["quarter"].unique()
    valid_regions = sales["region"].unique()
    valid_categories = sales["category"].unique()

    if quarter not in valid_quarters:
        raise ValueError(
            f"Invalid quarter '{quarter}'. "
            f"Valid values are: {list(valid_quarters)}"
        )

    if region not in valid_regions:
        raise ValueError(
            f"Invalid region '{region}'. "
            f"Valid values are: {list(valid_regions)}"
        )

    if category not in valid_categories:
        raise ValueError(
            f"Invalid category '{category}'. "
            f"Valid values are: {list(valid_categories)}"
        )

    # Filter the requested business scenario
    sales_filtered = sales[
        (sales["quarter"] == quarter) &
        (sales["region"] == region) &
        (sales["category"] == category)
    ]

    inventory_filtered = inventory[
        (inventory["quarter"] == quarter) &
        (inventory["region"] == region) &
        (inventory["category"] == category)
    ]

    marketing_filtered = marketing[
        (marketing["quarter"] == quarter) &
        (marketing["region"] == region) &
        (marketing["category"] == category)
    ]

    # Validate that the requested combination exists
    if sales_filtered.empty:
        raise ValueError(
            f"No sales data found for "
            f"{quarter}, {region}, {category}."
        )

    if inventory_filtered.empty:
        raise ValueError(
            f"No inventory data found for "
            f"{quarter}, {region}, {category}."
        )

    if marketing_filtered.empty:
        raise ValueError(
            f"No marketing data found for "
            f"{quarter}, {region}, {category}."
        )

    summary = {
        "quarter": quarter,
        "region": region,
        "category": category,
        "revenue": float(sales_filtered["revenue"].sum()),
        "inventory_availability_pct": float(
            inventory_filtered["inventory_availability_pct"].mean()
        ),
        "stockout_rate_pct": float(
            inventory_filtered["stockout_rate_pct"].mean()
        ),
        "campaign_spend": float(
            marketing_filtered["campaign_spend"].sum()
        ),
        "conversion_rate_pct": float(
            marketing_filtered["conversion_rate_pct"].mean()
        ),
        "revenue_attributed": float(
            marketing_filtered["revenue_attributed"].sum()
        ),
    }
    return summary