"""
NovaRetail Synthetic Enterprise Data Generator
================================================

Purpose
-------
Generate a small but realistic synthetic enterprise business dataset
for the Enterprise Business Knowledge & Analytics Copilot project.

The generator creates:
    1. Master/reference data
    2. Sales data
    3. Inventory data
    4. Marketing data
    5. Customer Insights document
    6. Business Strategy document
    7. Quarterly Business Review PDF

Important design principle
--------------------------
The data is NOT generated as completely independent random values.

Instead, we first define a simple business model and then apply
controlled business rules.

This allows different datasets to tell a consistent business story.

Example:
    Fashion & Lifestyle
    + East region
    + Q4
        ↓
    weaker inventory availability
        ↓
    weaker marketing performance
        ↓
    weaker customer demand
        ↓
    lower sales

This controlled relationship will later help us test RAG retrieval
and grounded answer generation.

The dataset is fictional and does not represent a real company.
"""


# ============================================================
# 1. IMPORTS
# ============================================================

import random
from pathlib import Path

import pandas as pd


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

# A random seed makes the generated data reproducible.
#
# Without a seed:
#     Running the script today and tomorrow could produce
#     different numbers.
#
# With a seed:
#     The same code produces the same random values.
#
# This is important for experimentation and debugging.

RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ============================================================
# 3. PROJECT DIRECTORIES
# ============================================================

# Path(__file__) gives the location of this Python file.
#
# If this file is:
#
#     project/
#         scripts/
#             generate_data.py
#
# then:
#
#     Path(__file__).resolve().parent
#
# points to:
#
#     project/scripts
#
# The parent of that directory is our project root.

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 4. MASTER BUSINESS DATA
# ============================================================

# These are the controlled dimensions of our fictional company.

REGIONS = [
    "North",
    "South",
    "East",
    "West",
]

CHANNELS = [
    "Physical Store",
    "E-commerce",
]

QUARTERS = [
    "Q1",
    "Q2",
    "Q3",
    "Q4",
]


# ------------------------------------------------------------
# Product catalog
# ------------------------------------------------------------

PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "Smartphone",
        "category": "Electronics",
        "base_price": 30000,
    },
    {
        "product_id": "P002",
        "product_name": "Laptop",
        "category": "Electronics",
        "base_price": 60000,
    },
    {
        "product_id": "P003",
        "product_name": "Wireless Earbuds",
        "category": "Electronics",
        "base_price": 5000,
    },
    {
        "product_id": "P004",
        "product_name": "Smartwatch",
        "category": "Electronics",
        "base_price": 12000,
    },
    {
        "product_id": "P005",
        "product_name": "Air Fryer",
        "category": "Home & Kitchen",
        "base_price": 7000,
    },
    {
        "product_id": "P006",
        "product_name": "Vacuum Cleaner",
        "category": "Home & Kitchen",
        "base_price": 10000,
    },
    {
        "product_id": "P007",
        "product_name": "Cookware Set",
        "category": "Home & Kitchen",
        "base_price": 6000,
    },
    {
        "product_id": "P008",
        "product_name": "Skincare Kit",
        "category": "Beauty & Personal Care",
        "base_price": 3500,
    },
    {
        "product_id": "P009",
        "product_name": "Hair Dryer",
        "category": "Beauty & Personal Care",
        "base_price": 3000,
    },
    {
        "product_id": "P010",
        "product_name": "Grooming Kit",
        "category": "Beauty & Personal Care",
        "base_price": 4000,
    },
    {
        "product_id": "P011",
        "product_name": "Sneakers",
        "category": "Fashion & Lifestyle",
        "base_price": 4500,
    },
    {
        "product_id": "P012",
        "product_name": "Backpack",
        "category": "Fashion & Lifestyle",
        "base_price": 2500,
    },
    {
        "product_id": "P013",
        "product_name": "Casual Jacket",
        "category": "Fashion & Lifestyle",
        "base_price": 5000,
    },
    {
        "product_id": "P014",
        "product_name": "Yoga Mat",
        "category": "Sports & Fitness",
        "base_price": 1500,
    },
    {
        "product_id": "P015",
        "product_name": "Running Shoes",
        "category": "Sports & Fitness",
        "base_price": 4000,
    },
    {
        "product_id": "P016",
        "product_name": "Fitness Band",
        "category": "Sports & Fitness",
        "base_price": 3500,
    },
]


# ------------------------------------------------------------
# Customer segments
# ------------------------------------------------------------

CUSTOMER_SEGMENTS = [
    "Value Seekers",
    "Young Professionals",
    "Families",
    "Fitness & Lifestyle Enthusiasts",
]


# ============================================================
# 5. BUSINESS RULES
# ============================================================

# These values represent synthetic assumptions about how
# different categories behave.
#
# They are NOT real-world statistics.

CATEGORY_MULTIPLIERS = {
    "Electronics": 1.20,
    "Home & Kitchen": 1.00,
    "Beauty & Personal Care": 0.90,
    "Fashion & Lifestyle": 0.95,
    "Sports & Fitness": 0.85,
}


# Channel behavior.
CHANNEL_MULTIPLIERS = {
    "Physical Store": 1.00,
    "E-commerce": 1.10,
}


# Regional demand differences.
REGION_MULTIPLIERS = {
    "North": 1.00,
    "South": 1.10,
    "East": 0.90,
    "West": 1.05,
}


# Quarterly demand pattern.
QUARTER_MULTIPLIERS = {
    "Q1": 0.95,
    "Q2": 1.00,
    "Q3": 1.05,
    "Q4": 1.15,
}


# ============================================================
# 6. CONTROLLED BUSINESS SCENARIOS
# ============================================================

# Scenario 1:
# Fashion & Lifestyle sales decline in the East region during Q4.
#
# We don't simply force sales to be low.
#
# Instead, several business factors are weakened:
#
#     Inventory availability ↓
#     Marketing performance ↓
#     Customer demand ↓
#     Sales ↓
#
# This creates a more believable relationship.

SCENARIO_1 = {
    "region": "East",
    "category": "Fashion & Lifestyle",
    "quarter": "Q4",
    "sales_multiplier": 0.72,
    "inventory_multiplier": 0.72,
    "marketing_multiplier": 0.70,
    "customer_demand_multiplier": 0.75,
}


# Scenario 2:
# Electronics performs strongly in the South region.

SCENARIO_2 = {
    "region": "South",
    "category": "Electronics",
    "quarter": "Q4",
    "sales_multiplier": 1.30,
    "inventory_multiplier": 1.10,
    "marketing_multiplier": 1.25,
    "customer_demand_multiplier": 1.20,
}


# ============================================================
# 7. HELPER FUNCTIONS
# ============================================================

def get_product_by_id(product_id):
    """
    Find a product dictionary using its product ID.

    Example:
        P001 -> Smartphone

    This function makes the code easier to read than repeatedly
    searching the PRODUCTS list manually.
    """

    for product in PRODUCTS:
        if product["product_id"] == product_id:
            return product

    return None


def get_scenario(region, category, quarter):
    """
    Return the controlled scenario that applies to a specific
    region/category/quarter combination.

    If no special scenario applies, return None.
    """

    if (
        region == SCENARIO_1["region"]
        and category == SCENARIO_1["category"]
        and quarter == SCENARIO_1["quarter"]
    ):
        return SCENARIO_1

    if (
        region == SCENARIO_2["region"]
        and category == SCENARIO_2["category"]
        and quarter == SCENARIO_2["quarter"]
    ):
        return SCENARIO_2

    return None


# ============================================================
# 8. GENERATE SALES DATA
# ============================================================

def generate_sales_data():
    """
    Generate synthetic sales records.

    Grain of the dataset:
        Region + Channel + Quarter + Product

    Each row represents the sales performance of one product
    for one region, channel, and quarter.
    """

    rows = []

    for region in REGIONS:

        for channel in CHANNELS:

            for quarter in QUARTERS:

                for product in PRODUCTS:

                    category = product["category"]

                    # ------------------------------------------------
                    # Start with a simple baseline.
                    # ------------------------------------------------

                    base_units = random.randint(80, 180)

                    # Apply our business assumptions.
                    units = (
                        base_units
                        * REGION_MULTIPLIERS[region]
                        * CHANNEL_MULTIPLIERS[channel]
                        * QUARTER_MULTIPLIERS[quarter]
                        * CATEGORY_MULTIPLIERS[category]
                    )

                    # ------------------------------------------------
                    # Apply controlled scenario if relevant.
                    # ------------------------------------------------

                    scenario = get_scenario(
                        region,
                        category,
                        quarter,
                    )

                    if scenario:
                        units *= scenario["sales_multiplier"]

                    # Add a small amount of natural variation.
                    units *= random.uniform(0.90, 1.10)

                    units = max(1, int(round(units)))

                    # Discount is a percentage.
                    discount_pct = round(
                        random.uniform(5, 20),
                        1,
                    )

                    # Actual selling price after discount.
                    avg_selling_price = (
                        product["base_price"]
                        * (1 - discount_pct / 100)
                    )

                    revenue = units * avg_selling_price

                    rows.append(
                        {
                            "region": region,
                            "channel": channel,
                            "quarter": quarter,
                            "product_id": product["product_id"],
                            "product_name": product["product_name"],
                            "category": category,
                            "customer_segment": random.choice(
                                CUSTOMER_SEGMENTS
                            ),
                            "units_sold": units,
                            "discount_pct": discount_pct,
                            "avg_selling_price": round(
                                avg_selling_price,
                                2,
                            ),
                            "revenue": round(revenue, 2),
                        }
                    )

    return pd.DataFrame(rows)


# ============================================================
# 9. GENERATE INVENTORY DATA
# ============================================================

def generate_inventory_data(sales_df):
    """
    Generate inventory information.

    Inventory is partially influenced by sales demand.

    This is important because we want inventory and sales to have
    a meaningful business relationship.
    """

    rows = []

    for _, sale in sales_df.iterrows():

        product = get_product_by_id(sale["product_id"])

        units_sold = sale["units_sold"]

        # Opening inventory is generally larger than expected
        # quarterly demand.
        opening_inventory = int(
            units_sold * random.uniform(1.4, 2.0)
        )

        category = sale["category"]

        scenario = get_scenario(
            sale["region"],
            category,
            sale["quarter"],
        )

        if scenario:
            availability_pct = (
                random.uniform(65, 75)
                * scenario["inventory_multiplier"]
            )
        else:
            availability_pct = random.uniform(88, 98)

        # Keep the percentage within a sensible range.
        availability_pct = max(
            50,
            min(99, availability_pct),
        )

        stockout_rate = 100 - availability_pct

        # Closing inventory is estimated from opening inventory
        # and sales.
        closing_inventory = max(
            0,
            opening_inventory - units_sold,
        )

        rows.append(
            {
                "region": sale["region"],
                "channel": sale["channel"],
                "quarter": sale["quarter"],
                "product_id": sale["product_id"],
                "product_name": product["product_name"],
                "category": category,
                "opening_inventory": opening_inventory,
                "closing_inventory": closing_inventory,
                "inventory_availability_pct": round(
                    availability_pct,
                    1,
                ),
                "stockout_rate_pct": round(
                    stockout_rate,
                    1,
                ),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# 10. GENERATE MARKETING DATA
# ============================================================

def generate_marketing_data():
    """
    Generate synthetic marketing performance data.

    Grain:
        Region + Channel + Quarter + Category

    Marketing is generated at category level rather than
    individual-product level to keep the dataset manageable.
    """

    rows = []

    categories = list(
        CATEGORY_MULTIPLIERS.keys()
    )

    for region in REGIONS:

        for channel in CHANNELS:

            for quarter in QUARTERS:

                for category in categories:

                    scenario = get_scenario(
                        region,
                        category,
                        quarter,
                    )

                    campaign_spend = random.randint(
                        50000,
                        150000,
                    )

                    impressions = random.randint(
                        500000,
                        1500000,
                    )

                    clicks = int(
                        impressions
                        * random.uniform(0.02, 0.06)
                    )

                    conversion_rate = random.uniform(
                        1.5,
                        5.0,
                    )

                    revenue_attributed = (
                        campaign_spend
                        * random.uniform(2.0, 5.0)
                    )

                    # Apply controlled scenario.
                    if scenario:
                        marketing_multiplier = (
                            scenario["marketing_multiplier"]
                        )

                        campaign_spend *= (
                            marketing_multiplier
                        )

                        impressions *= (
                            marketing_multiplier
                        )

                        clicks *= (
                            marketing_multiplier
                        )

                        conversion_rate *= (
                            scenario[
                                "customer_demand_multiplier"
                            ]
                        )

                        revenue_attributed *= (
                            marketing_multiplier
                        )

                    rows.append(
                        {
                            "region": region,
                            "channel": channel,
                            "quarter": quarter,
                            "category": category,
                            "campaign_spend": round(
                                campaign_spend,
                                2,
                            ),
                            "impressions": int(impressions),
                            "clicks": int(clicks),
                            "conversion_rate_pct": round(
                                conversion_rate,
                                2,
                            ),
                            "revenue_attributed": round(
                                revenue_attributed,
                                2,
                            ),
                        }
                    )

    return pd.DataFrame(rows)


# ============================================================
# 11. GENERATE CUSTOMER SEGMENT DATA
# ============================================================

def generate_customer_segment_data():
    """
    Create a small reference dataset describing the relationship
    between customer segments and product categories.

    This is intentionally simple and will later help the RAG system
    retrieve customer-related business context.
    """

    rows = [
        {
            "customer_segment": "Value Seekers",
            "primary_interest": "Promotion-sensitive products",
            "strong_categories": "Home & Kitchen, Fashion & Lifestyle",
        },
        {
            "customer_segment": "Young Professionals",
            "primary_interest": "Technology and lifestyle products",
            "strong_categories": "Electronics, Fashion & Lifestyle",
        },
        {
            "customer_segment": "Families",
            "primary_interest": "Household and practical products",
            "strong_categories": "Home & Kitchen, Electronics",
        },
        {
            "customer_segment": "Fitness & Lifestyle Enthusiasts",
            "primary_interest": "Fitness and wellness products",
            "strong_categories": "Sports & Fitness",
        },
    ]

    return pd.DataFrame(rows)


# ============================================================
# 12. GENERATE PRODUCT MASTER DATA
# ============================================================

def generate_product_data():
    """
    Convert our Python product catalog into a DataFrame.
    """

    return pd.DataFrame(PRODUCTS)


# ============================================================
# 13. GENERATE CUSTOMER INSIGHTS DOCUMENT CONTENT
# ============================================================

def generate_customer_insights():
    """
    Generate narrative business knowledge for the Customer
    Insights document.

    The content intentionally describes relationships that also
    exist in the structured data.
    """

    return """
NovaRetail Customer Insights
============================

Overview
--------
NovaRetail serves four primary customer segments:

1. Value Seekers
2. Young Professionals
3. Families
4. Fitness & Lifestyle Enthusiasts


Segment Insights
----------------

Value Seekers are relatively sensitive to promotions and discounts.
They demonstrate stronger interest in products where promotional
offers provide clear value.

Young Professionals show stronger interest in Electronics and
Fashion & Lifestyle products. Convenience and digital shopping
experience are important factors for this segment.

Families demonstrate relatively higher demand for Home & Kitchen
products and practical household products.

Fitness & Lifestyle Enthusiasts demonstrate stronger engagement
with Sports & Fitness products such as running shoes, yoga mats,
and fitness bands.


Regional Observation
-------------------

During Q4, customer interest in Fashion & Lifestyle products in the
East region weakened compared with other regions.

The decline was particularly noticeable for products such as
Sneakers, Backpacks, and Casual Jackets.

The decline appears to be associated with changing customer
preferences and weaker promotional engagement.


Electronics Observation
-----------------------

Electronics demonstrated strong demand in the South region during
Q4.

Young Professionals were an important customer segment contributing
to this performance.

The combination of strong digital engagement, healthy product
availability, and customer interest supported the category's strong
performance.
""".strip()


# ============================================================
# 14. GENERATE BUSINESS STRATEGY DOCUMENT CONTENT
# ============================================================

def generate_business_strategy():
    """
    Generate management-level business recommendations.

    These recommendations connect the observations from the
    structured datasets and customer insights.
    """

    return """
NovaRetail Business Strategy
============================

Q4 Management Review
--------------------

NovaRetail's Q4 performance shows different trends across regions
and product categories.


Fashion & Lifestyle — East Region
----------------------------------

Fashion & Lifestyle performance weakened in the East region during
Q4.

Management observations indicate that the decline was associated
with:

- Lower inventory availability
- Higher stockout pressure
- Weaker marketing campaign performance
- Changing customer preferences

Recommended actions include:

1. Improve inventory availability for high-demand products.
2. Review regional marketing campaigns.
3. Reassess product assortment for the East region.
4. Monitor customer preference changes.
5. Improve coordination between marketing and inventory planning.


Electronics — South Region
--------------------------

Electronics delivered strong performance in the South region during
Q4.

Key contributing factors included:

- Healthy inventory availability
- Strong e-commerce engagement
- Successful marketing activity
- Strong demand from Young Professionals

Recommended actions include:

1. Maintain healthy inventory levels.
2. Continue targeted digital marketing.
3. Monitor demand from Young Professionals.
4. Evaluate opportunities to expand successful Electronics products.


Management Priorities
---------------------

The key management priorities for the next planning cycle are:

- Improve inventory availability.
- Strengthen regional marketing effectiveness.
- Monitor customer preferences.
- Improve coordination between Sales, Marketing, Inventory,
  and Supply Chain teams.
- Expand successful category and regional strategies where evidence
  supports continued investment.
""".strip()


# ============================================================
# 15. GENERATE QUARTERLY BUSINESS REVIEW CONTENT
# ============================================================

def generate_qbr_content(sales_df):
    """
    Create a simple quarterly business review.

    This document is derived from the generated sales data so that
    the narrative and structured data remain consistent.
    """

    quarterly_sales = (
        sales_df
        .groupby("quarter")["revenue"]
        .sum()
        .sort_index()
    )

    lines = [
        "NovaRetail Quarterly Business Review",
        "====================================",
        "",
        "Revenue Summary",
        "---------------",
    ]

    for quarter, revenue in quarterly_sales.items():
        lines.append(
            f"{quarter}: Revenue of INR {revenue:,.0f}"
        )

    lines.extend(
        [
            "",
            "Business Highlights",
            "-------------------",
            "",
            "Q4 was an important quarter for NovaRetail.",
            "",
            "Electronics performed strongly in the South region.",
            "Fashion & Lifestyle experienced weaker performance",
            "in the East region.",
            "",
            "Management should focus on inventory availability,",
            "regional marketing effectiveness, and changing",
            "customer preferences.",
        ]
    )

    return "\n".join(lines)


# ============================================================
# 16. SAVE TEXT/DOCUMENT CONTENT
# ============================================================

def save_text_file(content, filename):
    """
    Save text content into the raw data directory.

    We initially save narrative content as TXT.

    DOCX/PDF conversion can be added as a separate step once
    the core data generation is verified.
    """

    output_path = RAW_DATA_DIR / filename

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(content)

    return output_path


# ============================================================
# 17. MAIN FUNCTION
# ============================================================

def main():
    """
    Main execution function.

    Keeping the program entry point inside main() is a common
    Python practice because it makes the script easier to reuse
    later.
    """

    print("=" * 60)
    print("NovaRetail Synthetic Data Generator")
    print("=" * 60)

    # --------------------------------------------------------
    # Generate structured datasets
    # --------------------------------------------------------

    print("\nGenerating sales data...")
    sales_df = generate_sales_data()

    print("Generating inventory data...")
    inventory_df = generate_inventory_data(
        sales_df
    )

    print("Generating marketing data...")
    marketing_df = generate_marketing_data()

    print("Generating product master...")
    products_df = generate_product_data()

    print("Generating customer segment data...")
    customer_segments_df = (
        generate_customer_segment_data()
    )

    # --------------------------------------------------------
    # Save structured datasets
    # --------------------------------------------------------

    sales_path = RAW_DATA_DIR / "sales.csv"
    inventory_path = RAW_DATA_DIR / "inventory.csv"
    marketing_path = RAW_DATA_DIR / "marketing.csv"
    products_path = RAW_DATA_DIR / "products.csv"
    segments_path = (
        RAW_DATA_DIR / "customer_segments.csv"
    )

    sales_df.to_csv(
        sales_path,
        index=False,
    )

    inventory_df.to_csv(
        inventory_path,
        index=False,
    )

    marketing_df.to_csv(
        marketing_path,
        index=False,
    )

    products_df.to_csv(
        products_path,
        index=False,
    )

    customer_segments_df.to_csv(
        segments_path,
        index=False,
    )

    # --------------------------------------------------------
    # Generate narrative documents
    # --------------------------------------------------------

    customer_insights = (
        generate_customer_insights()
    )

    business_strategy = (
        generate_business_strategy()
    )

    qbr_content = generate_qbr_content(
        sales_df
    )

    save_text_file(
        customer_insights,
        "customer_insights.txt",
    )

    save_text_file(
        business_strategy,
        "business_strategy.txt",
    )

    save_text_file(
        qbr_content,
        "quarterly_business_review.txt",
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\nData generation completed.")
    print("\nGenerated files:")

    for path in sorted(RAW_DATA_DIR.iterdir()):
        if path.is_file():
            print(f"  - {path.name}")

    print("\nDataset sizes:")
    print(f"  Sales records: {len(sales_df)}")
    print(f"  Inventory records: {len(inventory_df)}")
    print(f"  Marketing records: {len(marketing_df)}")

    print("\nOutput directory:")
    print(f"  {RAW_DATA_DIR}")


# ============================================================
# 18. SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()