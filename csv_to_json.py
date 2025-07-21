import pandas as pd
import json

INPUT_CSV = "Template_LA_Asset_group_BulkUpdateReport - Bulk_Report_Template_Encoded.csv"
OUTPUT_JSON = "output.json"

def parse_nested_csv(df):
    """
    Parse CSV with specific structure:
    - Multiple sections with "Blitz ID" headers
    - Each section may have the same Blitz ID but different data
    - Rows with empty Blitz ID should be merged with parent data to create individual records
    """
    df = df.dropna(how='all')
    header_rows = []
    for idx, row in df.iterrows():
        if len(row) > 0 and pd.notna(row.iloc[0]) and str(row.iloc[0]).strip() == "Blitz ID":
            header_rows.append(idx)
    if not header_rows:
        raise ValueError("No header row with 'Blitz ID' found in the CSV")
    headers = df.iloc[header_rows[0]].tolist()
    result = []
    for i, header_idx in enumerate(header_rows):
        if i + 1 < len(header_rows):
            section_end = header_rows[i + 1]
        else:
            section_end = len(df)
        section_data = df.iloc[header_idx + 1:section_end].reset_index(drop=True)
        section_data = section_data.dropna(how='all')
        current_parent = None
        for idx, row in section_data.iterrows():
            first_col_value = row.iloc[0] if len(row) > 0 else None
            if first_col_value is not None and pd.notna(first_col_value) and str(first_col_value).strip() == "Blitz ID":
                continue
            is_new_parent_row = False
            if first_col_value is not None and pd.notna(first_col_value):
                first_col_str = str(first_col_value).strip()
                if first_col_str != "" and first_col_str != "Blitz ID":
                    is_new_parent_row = True
            if is_new_parent_row:
                parent_dict = {}
                for j, header in enumerate(headers):
                    if j < len(row):
                        value = row.iloc[j]
                        if pd.isna(value):
                            parent_dict[header] = None
                        else:
                            parent_dict[header] = str(value).strip()
                    else:
                        parent_dict[header] = None
                parent_dict['section'] = i + 1
                current_parent = parent_dict
                result.append(current_parent.copy())
            else:
                if current_parent is not None:
                    merged_record = current_parent.copy()
                    for j, header in enumerate(headers):
                        if j < len(row):
                            value = row.iloc[j]
                            if pd.notna(value) and str(value).strip() != "":
                                merged_record[header] = str(value).strip()
                    has_additional_data = False
                    for j, header in enumerate(headers):
                        if j < len(row):
                            value = row.iloc[j]
                            if pd.notna(value) and str(value).strip() != "":
                                parent_value = current_parent.get(header)
                                if parent_value != str(value).strip():
                                    has_additional_data = True
                                    break
                    if has_additional_data:
                        result.append(merged_record)
    return result

def main():
    df = pd.read_csv(INPUT_CSV, keep_default_na=False)
    nested_data = parse_nested_csv(df)
    json_string = json.dumps(nested_data, indent=2, ensure_ascii=False)
    if OUTPUT_JSON:
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            f.write(json_string)
        print(f"JSON written to {OUTPUT_JSON}")
    else:
        print(json_string)

if __name__ == '__main__':
    main()
