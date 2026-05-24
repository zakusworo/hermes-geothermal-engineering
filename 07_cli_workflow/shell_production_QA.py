"""
Exercise 7: Shell + Python QA for geothermal production CSV.
Before running analysis, verify the CSV integrity.
"""
import csv, sys

def qa_csv(path='sample_separator.csv'):
    issues = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        required = {'well', 'date', 'separator_T_C', 'separator_P_kPa'}
        header = set(reader.fieldnames or [])
        missing = required - header
        if missing:
            issues.append(f'Missing columns: {missing}')
        rows = list(reader)
        if len(rows) == 0:
            issues.append('No data rows found')
        for i, row in enumerate(rows):
            try:
                T = float(row['separator_T_C'])
                P = float(row['separator_P_kPa'])
                if T < 0 or T > 374:
                    issues.append(f'Row {i+1}: Temperature {T} C out of physical bounds')
                if P < 0:
                    issues.append(f'Row {i+1}: Pressure {P} kPa negative')
            except (KeyError, ValueError) as e:
                issues.append(f'Row {i+1}: Parse error {e}')
    return issues

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else 'sample_separator.csv'
    issues = qa_csv(p)
    if issues:
        print('QA FAILED:')
        for iss in issues:
            print(f'  - {iss}')
        sys.exit(1)
    else:
        print('QA PASSED')
        sys.exit(0)
