"""Inspect raw Olist CSV files without modifying them."""

import argparse
from pathlib import Path

import pandas as pd

KEY_CHECKS = {
    "olist_customers_dataset.csv": [
        ["customer_id"],
        ["customer_unique_id"],
    ],
    "olist_geolocation_dataset.csv": [
        ["geolocation_zip_code_prefix"],
    ],
    "olist_order_items_dataset.csv": [
        ["order_id"],
        ["order_id", "order_item_id"],
    ],
    "olist_order_payments_dataset.csv": [
        ["order_id"],
        ["order_id", "payment_sequential"],
    ],
    "olist_order_reviews_dataset.csv": [
        ["review_id"],
        ["order_id"],
        ["review_id", "order_id"],
    ],
    "olist_orders_dataset.csv": [
        ["order_id"],
        ["customer_id"],
    ],
    "olist_products_dataset.csv": [
        ["product_id"],
    ],
    "olist_sellers_dataset.csv": [
        ["seller_id"],
    ],
    "product_category_name_translation.csv": [
        ["product_category_name"],
        ["product_category_name_english"],
    ],
}


def inspect_relationships(data_dir: Path) -> None:
    relationships = [
        (
            "olist_orders_dataset.csv", "customer_id",
            "olist_customers_dataset.csv", "customer_id",
        ),
        (
            "olist_order_items_dataset.csv", "order_id",
            "olist_orders_dataset.csv", "order_id",
        ),
        (
            "olist_order_items_dataset.csv", "product_id",
            "olist_products_dataset.csv", "product_id",
        ),
        (
            "olist_order_items_dataset.csv", "seller_id",
            "olist_sellers_dataset.csv", "seller_id",
        ),
        (
            "olist_order_payments_dataset.csv", "order_id",
            "olist_orders_dataset.csv", "order_id",
        ),
        (
            "olist_order_reviews_dataset.csv", "order_id",
            "olist_orders_dataset.csv", "order_id",
        ),
        (
            "olist_products_dataset.csv", "product_category_name",
            "product_category_name_translation.csv",
            "product_category_name",
        ),
    ]

    print("\nRelationship coverage:")

    for child_file, child_key, parent_file, parent_key in relationships:
        child = pd.read_csv(
            data_dir / child_file,
            usecols=[child_key],
            dtype="string",
            keep_default_na=False,
            na_values=[""],
        )[child_key]

        parent = pd.read_csv(
            data_dir / parent_file,
            usecols=[parent_key],
            dtype="string",
            keep_default_na=False,
            na_values=[""],
        )[parent_key]

        missing = child.isna()
        unmatched = ~missing & ~child.isin(parent.dropna())

        print(
            f"\n  {child_file}.{child_key}"
            f"\n    -> {parent_file}.{parent_key}"
            f"\n    Missing references: {int(missing.sum()):,}"
            f"\n    Unmatched nonmissing rows: {int(unmatched.sum()):,}"
            f"\n    Distinct unmatched values: "
            f"{child[unmatched].nunique():,}"
        )
def inspect_files(data_dir: Path) -> None:
    if not data_dir.is_dir():
        raise NotADirectoryError(f"Data directory not found: {data_dir}")

    csv_paths = sorted(data_dir.glob("*.csv"))

    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {data_dir}")

    print(f"Directory: {data_dir.resolve()}")
    print(f"CSV files: {len(csv_paths)}")

    for path in csv_paths:
        # Preserve identifiers and ZIP-code prefixes as text.
        # Disable automatic missing-value interpretation for this inventory.
        df = pd.read_csv(
                     path,
                     dtype="string",
                     keep_default_na=False,
                     na_values=[""],
                    )

        size_mib = path.stat().st_size / (1024 ** 2)

        print(f"\nFile: {path.name}")
        print(f"Size: {size_mib:.2f} MiB")
        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")
        print(f"Column names: {', '.join(df.columns)}")
        print("Key checks:")

        for columns in KEY_CHECKS.get(path.name, []):
            key_data = df[columns]

            missing_rows = int(key_data.isna().any(axis=1).sum())
            repeated_rows = int(key_data.duplicated().sum())

            is_candidate = missing_rows == 0 and repeated_rows == 0

            print(
                f"  {', '.join(columns)}: "
                f"missing-key rows={missing_rows:,}; "
                f"repeated-key rows={repeated_rows:,}; "
                f"candidate in this file={is_candidate}"
            )

        duplicate_count = int(df.duplicated().sum())
        print(f"Fully duplicated rows: {duplicate_count:,}")

        missing_counts = df.isna().sum()
        missing_columns = missing_counts[missing_counts > 0]

        if missing_columns.empty:
            print("Missing values: none under the current parsing rule")
        else:
            missing_summary = pd.DataFrame(
                {
                    "missing_count": missing_columns,
                    "missing_pct": missing_columns / len(df) * 100,
                }
            )
            print("Missing values:")
            print(
                missing_summary.to_string(
                    float_format=lambda value: f"{value:.2f}"
                )
            )

def inspect_order_multiplicity(data_dir: Path) -> None:
    orders = pd.read_csv(
        data_dir / "olist_orders_dataset.csv",
        usecols=["order_id"],
        dtype="string",
        keep_default_na=False,
        na_values=[""],
    )

    print("\nChild records per order:")

    child_files = [
        "olist_order_items_dataset.csv",
        "olist_order_payments_dataset.csv",
        "olist_order_reviews_dataset.csv",
    ]

    for filename in child_files:
        child = pd.read_csv(
            data_dir / filename,
            usecols=["order_id"],
            dtype="string",
            keep_default_na=False,
            na_values=[""],
        )

        counts = child["order_id"].value_counts()

        per_order = (
            orders["order_id"]
            .map(counts)
            .fillna(0)
            .astype("int64")
        )

        print(f"\n  {filename}")
        print(f"    Orders with no records: {int((per_order == 0).sum()):,}")
        print(f"    Orders with one record: {int((per_order == 1).sum()):,}")
        print(f"    Orders with multiple records: {int((per_order > 1).sum()):,}")
        print(f"    Maximum records per order: {int(per_order.max()):,}")
        print(f"    Total child records counted: {int(per_order.sum()):,}")
def inspect_order_dates(data_dir: Path) -> None:
    orders = pd.read_csv(
        data_dir / "olist_orders_dataset.csv",
        dtype="string",
        keep_default_na=False,
        na_values=[""],
    )

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    print("\nTimestamp checks:")

    for column in date_columns:
        raw = orders[column]

        parsed = pd.to_datetime(
            raw,
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce",
        )

        invalid = raw.notna() & parsed.isna()
        orders[column] = parsed

        print(
            f"\n  {column}"
            f"\n    Missing source values: {int(raw.isna().sum()):,}"
            f"\n    Invalid nonmissing values: {int(invalid.sum()):,}"
            f"\n    Earliest parsed value: {parsed.min()}"
            f"\n    Latest parsed value: {parsed.max()}"
        )

    orders["delivery_timestamp_missing"] = (
        orders["order_delivered_customer_date"].isna()
    )

    status_summary = (
        orders.groupby("order_status", dropna=False)
        .agg(
            orders=("order_id", "size"),
            missing_delivery_timestamp=(
                "delivery_timestamp_missing", "sum"
            ),
        )
        .sort_values("orders", ascending=False)
    )

    print("\nOrder statuses and missing delivery timestamps:")
    print(status_summary.to_string())

    purchase = orders["order_purchase_timestamp"]
    delivered = orders["order_delivered_customer_date"]
    estimated = orders["order_estimated_delivery_date"]

    print("\nChronology checks:")
    print(
        "  Delivered before purchase:",
        int((delivered.notna() & purchase.notna()
             & (delivered < purchase)).sum()),
    )
    print(
        "  Estimated delivery before purchase:",
        int((estimated.notna() & purchase.notna()
             & (estimated < purchase)).sum()),
    )

def inspect_numeric_fields(data_dir: Path) -> None:
    numeric_fields = {
        "olist_order_items_dataset.csv": [
            "order_item_id", "price", "freight_value",
        ],
        "olist_order_payments_dataset.csv": [
            "payment_sequential", "payment_installments",
            "payment_value",
        ],
        "olist_order_reviews_dataset.csv": [
            "review_score",
        ],
        "olist_products_dataset.csv": [
            "product_name_lenght", "product_description_lenght",
            "product_photos_qty", "product_weight_g",
            "product_length_cm", "product_height_cm",
            "product_width_cm",
        ],
        "olist_geolocation_dataset.csv": [
            "geolocation_lat", "geolocation_lng",
        ],
    }

    print("\nNumeric field checks:")

    for filename, columns in numeric_fields.items():
        df = pd.read_csv(
            data_dir / filename,
            usecols=columns,
            dtype="string",
            keep_default_na=False,
            na_values=[""],
        )

        results = []

        for column in columns:
            raw = df[column]
            numeric = pd.to_numeric(raw, errors="coerce")
            invalid = raw.notna() & numeric.isna()

            results.append(
                {
                    "column": column,
                    "missing": int(raw.isna().sum()),
                    "invalid": int(invalid.sum()),
                    "negative": int((numeric < 0).sum()),
                    "zero": int((numeric == 0).sum()),
                    "min": numeric.min(),
                    "max": numeric.max(),
                }
            )

        print(f"\n  {filename}")
        print(pd.DataFrame(results).set_index("column").to_string())
def inspect_category_translation(data_dir: Path) -> None:
    products = pd.read_csv(
        data_dir / "olist_products_dataset.csv",
        usecols=["product_id", "product_category_name"],
        dtype="string",
        keep_default_na=False,
        na_values=[""],
    )

    translation = pd.read_csv(
        data_dir / "product_category_name_translation.csv",
        dtype="string",
        keep_default_na=False,
        na_values=[""],
    )

    category = products["product_category_name"]
    known_categories = translation["product_category_name"]

    missing = category.isna()
    untranslated = category.notna() & ~category.isin(known_categories)

    print("\nCategory translation checks:")
    print(f"  Products without a category: {int(missing.sum()):,}")
    print(
        "  Products with an untranslated category:",
        f"{int(untranslated.sum()):,}",
    )

    print("\nUntranslated categories and product counts:")
    print(
        category[untranslated]
        .value_counts()
        .rename_axis("product_category_name")
        .rename("product_count")
        .to_string()
    )

    unused = ~known_categories.isin(category.dropna())

    print(
        "\n  Translation entries absent from products:",
        f"{int(unused.sum()):,}",
    )
def inspect_geolocation_grain(data_dir: Path) -> None:
    geo = pd.read_csv(
        data_dir / "olist_geolocation_dataset.csv",
        dtype="string",
        keep_default_na=False,
        na_values=[""],
    )

    prefix = "geolocation_zip_code_prefix"

    # Temporary analysis copy; the source CSV remains unchanged.
    distinct_rows = geo.drop_duplicates()

    rows_per_prefix = distinct_rows.groupby(prefix).size()

    coordinates = geo[
        [prefix, "geolocation_lat", "geolocation_lng"]
    ].drop_duplicates()

    coordinates_per_prefix = coordinates.groupby(prefix).size()

    print("\nGeolocation grain checks:")
    print(f"  Original rows: {len(geo):,}")
    print(f"  Distinct full rows: {len(distinct_rows):,}")
    print(f"  Distinct ZIP-code prefixes: {geo[prefix].nunique():,}")
    print(
        "  Prefixes with multiple distinct full rows:",
        f"{int((rows_per_prefix > 1).sum()):,}",
    )
    print(
        "  Prefixes with multiple distinct coordinate pairs:",
        f"{int((coordinates_per_prefix > 1).sum()):,}",
    )
    print(
        "  Maximum distinct full rows per prefix:",
        f"{int(rows_per_prefix.max()):,}",
    )
    print(
        "  Maximum distinct coordinate pairs per prefix:",
        f"{int(coordinates_per_prefix.max()):,}",
    )
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing the extracted Olist CSV files.",
    )
    args = parser.parse_args()
    inspect_files(args.data_dir)
    inspect_relationships(args.data_dir)
    inspect_order_multiplicity(args.data_dir)
    inspect_order_dates(args.data_dir)
    inspect_numeric_fields(args.data_dir)
    inspect_category_translation(args.data_dir)
    inspect_geolocation_grain(args.data_dir)

if __name__ == "__main__":
    main()
