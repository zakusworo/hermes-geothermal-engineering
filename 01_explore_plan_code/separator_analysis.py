import csv, os

# Fictional geothermal well data: separator measurements
DATA = """well,date,separator_T_C,separator_P_kPa,mass_flow_total_kg_s,steam_mass_flow_kg_s,liquid_mass_flow_kg_s
A-01,2023-01-01,145,250,10.0,1.5,8.5
A-01,2023-02-01,143,248,10.2,1.6,8.6
A-01,2023-03-01,142,247,10.3,1.7,8.6
A-01,2023-04-01,141,245,10.5,1.9,8.6
B-02,2023-01-01,152,255,8.0,2.0,6.0
B-02,2023-02-01,150,252,8.1,2.1,6.0
B-02,2023-03-01,148,250,8.2,2.3,5.9
B-02,2023-04-01,147,248,8.4,2.5,5.9
C-03,2023-01-01,138,240,12.0,1.2,10.8
C-03,2023-02-01,137,238,12.2,1.3,10.9
C-03,2023-03-01,136,237,12.3,1.4,10.9
C-03,2023-04-01,135,235,12.5,1.5,11.0
"""


def write_sample_data(path='sample_separator.csv'):
    with open(path, 'w', newline='') as f:
        f.write(DATA)


def read_production_data(path='sample_separator.csv'):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def add_enthalpy_trends(data):
    """
    Compute total enthalpy per kg from separator T and P using linear approximation.
    In real work, use CoolProp / IAPWS.
    """
    for row in data:
        T = float(row['separator_T_C'])
        P = float(row['separator_P_kPa'])
        # Simple placeholder enthalpy: h = 4.18*T + P/100 (kJ/kg) -- not physically accurate, just for demo
        row['enthalpy_kJ_kg'] = round(4.18 * T + P / 100.0, 2)
        row['steam_fraction'] = round(float(row['steam_mass_flow_kg_s']) / float(row['mass_flow_total_kg_s']), 4)
    return data


def summarize_by_well(data):
    wells = {}
    for row in data:
        w = row['well']
        if w not in wells:
            wells[w] = []
        wells[w].append(row)
    summary = {}
    for w, rows in wells.items():
        summary[w] = {
            'avg_enthalpy': sum(float(r['enthalpy_kJ_kg']) for r in rows) / len(rows),
            'max_steam_fraction': max(float(r['steam_fraction']) for r in rows),
            'temperature_decline_C': float(rows[0]['separator_T_C']) - float(rows[-1]['separator_T_C']),
        }
    return summary


if __name__ == '__main__':
    write_sample_data()
    data = read_production_data()
    data = add_enthalpy_trends(data)
    summary = summarize_by_well(data)
    for well, stats in summary.items():
        print(f"Well {well}: avg enthalpy={stats['avg_enthalpy']:.1f} kJ/kg, "
              f"max steam fraction={stats['max_steam_fraction']:.2%}, "
              f"T decline={stats['temperature_decline_C']:.1f} C")
