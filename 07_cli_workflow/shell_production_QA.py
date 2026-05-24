"""
Exercise 7: Shell + Python QA for geothermal production CSV.
Before running analysis, verify the CSV integrity.
"""
import csv
import sys
import os

REQUIRED_COLS = {'well', 'date', 'separator_T_C', 'separator_P_kPa'}

def qa_csv(path='sample_separator.csv'):
    """QA geothermal separator CSV for missing columns, NaN, out-of-range T/P, and duplicates."""
    issues = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        header = set(reader.fieldnames or [])
        missing = REQUIRED_COLS - header
        if missing:
            issues.append(f'Missing columns: {missing}')
        rows = list(reader)
        if len(rows) == 0:
            issues.append('No data rows found')
        seen = set()
        for i, row in enumerate(rows):
            well_date = (row.get('well'), row.get('date'))
            if well_date in seen:
                issues.append(f'Row {i+1}: Duplicate well-date {well_date}')
            seen.add(well_date)
            try:
                T = float(row['separator_T_C'])
                P = float(row['separator_P_kPa'])
                if T < 0 or T > 374:
                    issues.append(f'Row {i+1}: Temperature {T} C out of bounds (0-374)')
                if P < 0 or P > 22100:
                    issues.append(f'Row {i+1}: Pressure {P} kPa out of bounds (0-22100)')
            except (KeyError, ValueError) as e:
                issues.append(f'Row {i+1}: Parse error {e}')
    return issues


def write_sample_data(path='sample_separator.csv'):
    """Create fictional separator data if none exists."""
    print(f'Generating sample separator data at {path} ...')
    data = """well,date,separator_T_C,separator_P_kPa
A-01,2023-01-01,145,250
A-01,2023-02-01,143,248
A-01,2023-03-01,142,247
A-01,2023-04-01,141,245
B-02,2023-01-01,152,255
B-02,2023-02-01,150,252
B-02,2023-03-01,148,250
B-02,2023-04-01,147,248
C-03,2023-01-01,138,240
C-03,2023-02-01,137,238
C-03,2023-03-01,136,237
C-03,2023-04-01,135,235
"""
    with open(path, 'w', newline='') as f:
        f.write(data)


if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'sample_separator.csv'
    if not os.path.exists(p):
        write_sample_data(p)
    issues = qa_csv(p)
    if issues:
        print('QA FAILED:')
        for iss in issues:
            print(f'  - {iss}')
        sys.exit(1)
    else:
        print(f'QA PASSED for {p}')
        sys.exit(0)
