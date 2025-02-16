# qfx-to-csv

A Python utility to convert OFX/QFX financial files to CSV, TSV, or formatted table output.

## Features

- Supports multiple output formats: human-readable tables, CSV, and TSV
- Select specific columns to include in output
- Handles multiple input files in one command
- Shows available transaction fields automatically when invalid columns are specified

## Installation

1. Ensure Python 3.6+ is installed
2. Install required dependencies:
```bash
pip install ofxparse tabulate
```

## Usage

```bash
python main.py [OPTIONS] OFX_FILE(S)...
```

### Options:
- `--format FORMAT`: Output format (`table`, `csv`, or `tsv`), default: `table`
- `--columns COL1,COL2,...`: Comma-separated list of columns to include

### Examples:
1. Basic table view of transactions:
```bash
python main.py transactions.ofx
```

#### Output
```bash
┌──────────┬────────────┬────────────┬───────────┬───────┬────────┬───────────────────────┬───────┬─────────┬─────────────┐
│   amount │ checknum   │ date       │        id │ mcc   │ memo   │ payee                 │ sic   │ type    │ user_date   │
├──────────┼────────────┼────────────┼───────────┼───────┼────────┼───────────────────────┼───────┼─────────┼─────────────┤
│   -58.73 │            │ 2014-09-20 │ 201409206 │       │        │ TRADER JOE'S #541 QPS │ None  │ payment │ None        │
└──────────┴────────────┴────────────┴───────────┴───────┴────────┴───────────────────────┴───────┴─────────┴─────────────┘
```

2. Basic table view with specific columns:
```bash
python main.py transactions.ofx --columns date,amount,payee
```

#### Output
```bash
┌────────────┬──────────┬───────────────────────┐
│ date       │   amount │ payee                 │
├────────────┼──────────┼───────────────────────┤
│ 2014-09-20 │   -58.73 │ TRADER JOE'S #541 QPS │
└────────────┴──────────┴───────────────────────┘
```

3. Process multiple files with TSV format:
```bash
python main.py apostrophe.ofx checking.ofx --format CSV
```

#### Output
```bash
date,amount,payee
2014-09-20,-58.73,TRADER JOE'S #541 QPS
date,amount,payee
2011-03-31,0.01,DIVIDEND EARNED FOR PERIOD OF 03
2011-04-05,-34.51,"AUTOMATIC WITHDRAWAL, ELECTRIC BILL"
2011-04-07,-25.00,"RETURNED CHECK FEE, CHECK # 319"
```

## Available Columns

Common transaction fields include:
- `date`
- `amount`
- `payee`
- `memo`
- `id`
- `type`
- `checknum`
- `sic`
- `mcc`

To see all available fields for your file:
1. Run the script with an invalid column name:
```bash
python main.py your_file.qfx --columns invalid_column
```
2. The error message will display all valid columns for your transactions

## License

This project is [MIT licensed](LICENSE).
