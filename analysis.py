import csv
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "retail_sales_dataset.csv"


def load_data(file_path):
    with open(file_path, newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    for row in rows:
        for field in [
            "unit_price",
            "quantity",
            "discount_pct",
            "sales_amount",
            "cost_amount",
            "profit",
        ]:
            row[field] = float(row[field])
    return rows


def summarize(rows):
    category_sales = defaultdict(float)
    region_sales = defaultdict(float)
    segment_sales = defaultdict(float)

    total_sales = 0.0
    total_profit = 0.0

    for row in rows:
        total_sales += row["sales_amount"]
        total_profit += row["profit"]
        category_sales[row["category"]] += row["sales_amount"]
        region_sales[row["region"]] += row["sales_amount"]
        segment_sales[row["customer_segment"]] += row["sales_amount"]

    orders = len(rows)
    avg_order_value = total_sales / orders if orders else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    return {
        "orders": orders,
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_order_value": avg_order_value,
        "profit_margin": profit_margin,
        "top_category": max(category_sales, key=category_sales.get),
        "top_region": max(region_sales, key=region_sales.get),
        "top_segment": max(segment_sales, key=segment_sales.get),
    }


def main():
    rows = load_data(DATA_FILE)
    summary = summarize(rows)

    print("Retail Sales Project Summary")
    print("-" * 30)
    print(f"Orders: {summary['orders']}")
    print(f"Total Sales: Rs. {summary['total_sales']:,.2f}")
    print(f"Total Profit: Rs. {summary['total_profit']:,.2f}")
    print(f"Average Order Value: Rs. {summary['avg_order_value']:,.2f}")
    print(f"Profit Margin: {summary['profit_margin']:.2f}%")
    print(f"Top Category: {summary['top_category']}")
    print(f"Top Region: {summary['top_region']}")
    print(f"Top Customer Segment: {summary['top_segment']}")


if __name__ == "__main__":
    main()
