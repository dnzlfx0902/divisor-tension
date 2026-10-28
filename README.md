# Calculadora de divisor de tensión con serie E24

Calcula tensión y corriente de salida de un divisor resistivo, propone la pareja de resistencias E24 más cercana al objetivo y rechaza valores fuera de rango con error explícito.

`electronica` · 2026-10-28

## Instalación

```bash
python3 --version   # 3.10 o superior
# sin dependencias: sólo biblioteca estándar
```

## Uso

```bash
python3 divisor_tension.py --demo
python3 divisor_tension.py --vin 12 --objetivo 3.3
```

Salida real de una corrida de ejemplo:

```text
vin=12 V  r1=2400 Ω  r2=910 Ω
vout=3.299 V  i=3.625 mA
error=0.9 mV
```

## Cómo probar

```bash
python3 -m unittest discover -s tests -v
```

## Estructura

```text
2026-10-28-divisor-tension/
├── .github/
│   └── workflows/
│       └── ci-python.yml
├── .gitignore
├── LICENSE
├── divisor_tension.py
└── tests/
    └── test_divisor_tension.py
```

## Licencia

Distribuido bajo la licencia MIT.
