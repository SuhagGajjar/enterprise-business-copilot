from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_csv(file_path: Path):
    """Inspect a CSV file."""
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    df = pd.read_csv(file_path)

    print(f"\nShape: {df.shape}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "  None")

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    print("\nBasic statistics:")
    print(df.describe(include="all").transpose().to_string())


def inspect_text(file_path: Path):
    """Inspect a text document."""
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    text = file_path.read_text(encoding="utf-8")

    print(f"\nCharacter count: {len(text)}")
    print(f"Word count: {len(text.split())}")

    print("\nContent:")
    print(text)


def main():
    print("=" * 70)
    print("NovaRetail Data Inspection")
    print("=" * 70)

    print(f"\nRaw data directory:")
    print(RAW_DATA_DIR)

    # Inspect CSV files
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    print(f"\nFound {len(csv_files)} CSV files.")

    for file_path in csv_files:
        inspect_csv(file_path)

    # Inspect text files
    text_files = sorted(RAW_DATA_DIR.glob("*.txt"))

    print(f"\nFound {len(text_files)} text files.")

    for file_path in text_files:
        inspect_text(file_path)

    print("\n" + "=" * 70)
    print("Inspection completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()