# CSV to JSON Converter

This script converts a specially structured CSV file (with parent and sub-rows, and repeated headers) into a flat JSON array, merging sub-rows into their parent records.

## Requirements

- Python 3.7+
- pandas

Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

1. Open `csv_to_json.py` in your editor.
2. At the top of the file, set:
   ```python
   INPUT_CSV = "your_input.csv"      # Path to your CSV file
   OUTPUT_JSON = "your_output.json"  # Path to save JSON, or None to print to terminal
   ```
   For example:
   ```python
   INPUT_CSV = "Template_LA_Asset_group_BulkUpdateReport - Bulk_Report_Template_Encoded.csv"
   OUTPUT_JSON = "output.json"
   ```
3. Run the script:
   ```bash
   python3 csv_to_json.py
   ```
   - If `OUTPUT_JSON` is set, the JSON will be saved to that file.
   - If `OUTPUT_JSON` is `None`, the JSON will be printed to the terminal.

## What it does
- Handles CSVs with repeated headers and sub-rows.
- Merges sub-rows into their parent records.
- Outputs a flat JSON array, one object per record.

## Example
See the sample CSV and generated `output.json` for reference. 