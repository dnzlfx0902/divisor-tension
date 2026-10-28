"""Calculadora de divisor de tensión con serie E24.

Calcula tensión y corriente de salida de un divisor resistivo, propone la pareja de resistencias E24 más cercana al objetivo y rechaza valores fuera de rango con error explícito.
"""
from __future__ import annotations

import math

SERIE_E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
             3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def resolver(vin, r1, r2):
    """Tensión de salida y corriente del divisor (R1 arriba, R2 a masa)."""
    if vin <= 0 or r1 <= 0 or r2 <= 0:
        raise ValueError("vin, r1 y r2 deben ser positivos")
    total = r1 + r2
    return vin * r2 / total, vin / total


def valores_e24(r):
    """Lleva una resistencia a la serie E24 inmediatamente inferior."""
    if r <= 0:
        raise ValueError("la resistencia debe ser positiva")
    decada = 10 ** math.floor(math.log10(r) + 1e-9)
    normalizado = r / decada
    candidato = max((v for v in SERIE_E24 if v <= normalizado + 1e-9), default=SERIE_E24[-1])
    return round(candidato * decada, 6)


def proponer(vin, vobjetivo):
    """Pareja E24 (r1, r2) con la tensión de salida más cercana al objetivo."""
    if not 0 < vobjetivo < vin:
        raise ValueError("el objetivo debe estar entre 0 y vin")
    razon = (vin - vobjetivo) / vobjetivo      # r1/r2 que entrega vobjetivo
    mejor = None
    for decada in (100.0, 1000.0, 10000.0):
        for base in SERIE_E24:
            r2 = round(base * decada, 6)
            for factor in (0.85, 0.9, 1.0, 1.1, 1.2):
                r1 = valores_e24(razon * r2 * factor)
                if r1 <= 0:
                    continue
                error = abs(vin * r2 / (r1 + r2) - vobjetivo)
                if mejor is None or error < mejor[0]:
                    mejor = (error, r1, r2)
    return mejor[1], mejor[2]


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Calculadora de divisor de tensión con serie E24")
    p.add_argument("--vin", type=float, default=12.0)
    p.add_argument("--objetivo", type=float, help="tensión de salida deseada")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.objetivo:
        r1, r2 = proponer(a.vin, a.objetivo)
    elif a.demo:
        r1, r2 = proponer(12.0, 3.3)
    else:
        p.print_help()
        return 0
    vout, corriente = resolver(a.vin, r1, r2)
    print(f"vin={a.vin:g} V  r1={r1:g} Ω  r2={r2:g} Ω")
    print(f"vout={vout:.3f} V  i={corriente * 1000:.3f} mA")
    print(f"error={abs(vout - (a.objetivo or 3.3)) * 1000:.1f} mV")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
