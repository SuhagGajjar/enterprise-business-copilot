from pathlib import Path

import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_sales():
    """Load the NovaRetail sales dataset."""
    return pd.read_csv(RAW_DATA_DIR / "sales.csv")


def load_inventory():
    """Load the NovaRetail inventory dataset."""
    return pd.read_csv(RAW_DATA_DIR / "inventory.csv")


def load_marketing():
    """Load the NovaRetail marketing dataset."""
    return pd.read_csv(RAW_DATA_DIR / "marketing.csv")


def load_products():
    """Load the NovaRetail product master dataset."""
    return pd.read_csv(RAW_DATA_DIR / "products.csv")


def load_customer_segments():
    """Load the NovaRetail customer segment dataset."""
    return pd.read_csv(RAW_DATA_DIR / "customer_segments.csv")