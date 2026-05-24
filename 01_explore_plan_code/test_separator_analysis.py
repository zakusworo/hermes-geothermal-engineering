"""Tests for Exercise 1: separator enthalpy trends."""
import csv, os, tempfile

from separator_analysis import write_sample_data, read_production_data, add_enthalpy_trends, summarize_by_well

def test_sample_data_exists():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        path = f.name
    try:
        write_sample_data(path)
        rows = list(csv.DictReader(open(path)))
        assert len(rows) == 12, f"Expected 12 rows, got {len(rows)}"
        assert rows[0]['well'] == 'A-01'
        assert float(rows[0]['separator_T_C']) == 145.0
    finally:
        os.unlink(path)

def test_enthalpy_computed():
    data = read_production_data()
    data = add_enthalpy_trends(data)
    assert 'enthalpy_kJ_kg' in data[0]
    assert float(data[0]['enthalpy_kJ_kg']) > 0

def test_steam_fraction_range():
    data = read_production_data()
    data = add_enthalpy_trends(data)
    for row in data:
        x = float(row['steam_fraction'])
        assert 0 <= x <= 1, f"Steam fraction {x} out of bounds"

def test_temperature_decline_detected():
    summary = summarize_by_well(add_enthalpy_trends(read_production_data()))
    assert summary['A-01']['temperature_decline_C'] > 0, "Expected temperature decline"
    assert summary['B-02']['temperature_decline_C'] > 0
    assert summary['C-03']['temperature_decline_C'] > 0

def test_monotonic_enthalpy_increases_with_T_placeholder():
    """
    For the simple placeholder formula h = 4.18*T + P/100, at fixed pressure,
    higher T should yield higher h.  This test is a sanity check that the formula
    is being applied monotonically at the pressure levels in the data.
    """
    data = read_production_data()
    data = add_enthalpy_trends(data)
    well_data = [d for d in data if d['well'] == 'A-01']
    hs = [float(d['enthalpy_kJ_kg']) for d in well_data]
    # Temperatures are monotonically decreasing in CSV, so enthalpy should decrease too.
    for i in range(len(hs)-1):
        T1 = float(well_data[i]['separator_T_C'])
        T2 = float(well_data[i+1]['separator_T_C'])
        if T1 > T2:
            assert hs[i] > hs[i+1], "Placeholder enthalpy did not decrease with lower T"
