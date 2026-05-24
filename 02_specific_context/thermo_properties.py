import csv
import io

# Sample geothermal well separator data
DATA = """well,date,separator_T_C,separator_P_kPa
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


class DummyPropsSI:
    """Placeholder "buggy" water property calculator.
    This version ignores pressure and returns enthalpy = 4.18 * T + 50.
    The correct formula should also account for pressure contribution.
    The test `test_known_value` will fail because of this.
    """
    @staticmethod
    def PropsSI(what, Tsym, Tval, Psym, Pval, fluid):
        if what == 'H':
            T_C = Tval - 273.15 if Tval > 200 else Tval
            return (4.18 * T_C + 50) * 1000  # J/kg
        if what == 'D':
            T_C = Tval - 273.15 if Tval > 200 else Tval
            return 1000 - 0.5 * T_C  # Very rough placeholder
        raise ValueError(f"Unknown property {what}")


PropsSI = DummyPropsSI.PropsSI

def enthalpy_from_TP(T_C, P_kPa):
    """Compute enthalpy (J/kg) from T (C) and P (kPa)."""
    return PropsSI('H', 'T', T_C, 'P', P_kPa * 1000, 'Water')


def density_from_TP(T_C, P_kPa):
    """Compute density (kg/m³) from T (C) and P (kPa)."""
    return PropsSI('D', 'T', T_C, 'P', P_kPa * 1000, 'Water')


if __name__ == '__main__':
    # Round-trip: the test will catch that this does NOT match known IAPWS values
    h = enthalpy_from_TP(200, 2000)
    rho = density_from_TP(200, 2000)
    print(f"T=200 C, P=2000 kPa --> h={h/1000:.1f} kJ/kg, rho={rho:.1f} kg/m³")
