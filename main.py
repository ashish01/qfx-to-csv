#!/usr/bin/env python3
"""
QFX to CSV converter - Converts OFX/QFX financial files to various formats.
"""
import csv
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ofxparse import OfxParser
from tabulate import tabulate


def get_transaction_fields(transaction: Any) -> List[str]:
    """Extract available fields from a transaction object."""
    return [attr for attr in dir(transaction) if not attr.startswith("_")]


def format_value(value: Any) -> str:
    """Format a value for display, handling date objects."""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)


def convert_ofx(
    ofx_file: Union[str, Path],
    output_format: str,
    columns: Optional[List[str]] = None,
    no_headers: bool = False,
) -> None:
    """
    Convert OFX file to specified format and output to stdout.
    
    Args:
        ofx_file: Path to the OFX/QFX file
        output_format: Format to convert to (csv, tsv, or table)
        columns: List of columns to include in output
        no_headers: Whether to suppress headers in output
    """
    # Parse OFX file
    with open(ofx_file) as fileobj:
        ofx = OfxParser.parse(fileobj)

    # Get account transactions
    account = ofx.account
    transactions = account.statement.transactions

    if not transactions:
        print(f"No transactions found in {ofx_file}", file=sys.stderr)
        return

    # Get transaction fields
    first_trans = transactions[0]
    all_fields = get_transaction_fields(first_trans)
    
    # Use specified columns if provided, otherwise use all fields
    if columns:
        # Validate specified columns exist
        invalid_cols = [col for col in columns if col not in all_fields]
        if invalid_cols:
            print(f"Error: Invalid columns specified: {invalid_cols}", file=sys.stderr)
            print(f"Available columns: {all_fields}", file=sys.stderr)
            sys.exit(1)
        header = columns
    else:
        header = all_fields

    # Prepare data rows
    rows = []
    for trans in transactions:
        row = {field: format_value(getattr(trans, field)) for field in header}
        rows.append(row)

    # Output based on format
    if output_format in ("csv", "tsv"):
        delimiter = "," if output_format == "csv" else "\t"
        writer = csv.DictWriter(sys.stdout, fieldnames=header, delimiter=delimiter)
        if not no_headers:
            writer.writeheader()
        writer.writerows(rows)
    elif output_format == "table":
        # Convert rows to list format for tabulate
        table_data = [[row[h] for h in header] for row in rows]
        headers = header if not no_headers else []
        print(tabulate(table_data, headers=headers, tablefmt="simple_grid"))


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Convert OFX/QFX files to various formats"
    )
    parser.add_argument(
        "ofx_files", 
        nargs="+", 
        help="Input OFX/QFX file(s)"
    )
    parser.add_argument(
        "--format",
        choices=["tsv", "csv", "table"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--columns",
        help="Comma-separated list of columns to display (display all if not provided)",
    )
    parser.add_argument(
        "--no-headers",
        action="store_true",
        help="Do not print headers in output",
    )
    args = parser.parse_args()

    columns = args.columns.split(",") if args.columns else None
    
    for ofx_file in args.ofx_files:
        convert_ofx(ofx_file, args.format, columns, args.no_headers)


if __name__ == "__main__":
    main()