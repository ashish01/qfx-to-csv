import csv
import argparse
from typing import Dict, List
from ofxparse import OfxParser
import sys
from tabulate import tabulate


def convert_ofx(
    ofx_file: str, output_format: str, columns: List[str] | None = None
) -> None:
    """Convert OFX file to specified format and output to stdout"""

    # Parse OFX file
    with open(ofx_file) as fileobj:
        ofx = OfxParser.parse(fileobj)

    # Get account transactions
    account = ofx.account
    transactions = account.statement.transactions

    # Get first transaction to inspect available fields
    if transactions:
        first_trans = transactions[0]
        all_fields = [attr for attr in dir(first_trans) if not attr.startswith("_")]
        # Use specified columns if provided, otherwise use all fields
        header = columns if columns else all_fields
        # Validate specified columns exist
        if columns:
            invalid_cols = [col for col in columns if col not in all_fields]
            if invalid_cols:
                print(
                    f"Warning: Invalid columns specified: {invalid_cols}",
                    file=sys.stderr,
                )
                print(f"Available columns: {all_fields}", file=sys.stderr)
                sys.exit(1)
    else:
        header = []

    # Prepare data rows
    rows: List[Dict[str, str]] = []

    for trans in transactions:
        row = {}
        for field in header:
            value = getattr(trans, field)
            if hasattr(value, "strftime"):
                row[field] = value.strftime("%Y-%m-%d")
            else:
                row[field] = str(value)
        rows.append(row)

    # Output based on format
    if output_format == "tsv":
        writer = csv.DictWriter(sys.stdout, fieldnames=header, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    elif output_format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    elif output_format == "table":
        # Convert rows to list format for tabulate
        table_data = [[row[h] for h in header] for row in rows]
        print(tabulate(table_data, headers=header, tablefmt="simple_grid"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert OFX file to various formats")
    parser.add_argument("ofx_files", nargs="+", help="Input OFX file(s)")
    parser.add_argument(
        "--format",
        choices=["tsv", "csv", "table"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--columns",
        type=str,
        help="Comma-separated list of columns to display (display all if not provided)",
    )
    args = parser.parse_args()

    columns = args.columns.split(",") if args.columns else None
    for ofx_file in args.ofx_files:
        convert_ofx(ofx_file, args.format, columns)
