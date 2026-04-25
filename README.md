# Calculadora de Ventas CLP

Aplicación web para cálculo de ventas en pesos chilenos (CLP) con conversión de dólares, descuentos e impuestos.

## Características

- ✅ **Flask**: Formulario web funcional
- ✅ **Selenium**: Web scraping desde bcentral.cl
- ✅ **Descuentos**: 0%, 10%, 13% según monto
- ✅ **IVA**: 19% calculado sobre monto en CLP
- ✅ **Pruebas**: 33 tests con pytest

## Estructura

```
banco/
├── app_ventas.py          # Aplicación Flask
├── calculo_ventas.py      # Lógica de cálculo
├── obtener_dolar.py       # Selenium para bcentral.cl
├── test_calculo_ventas.py # Pruebas automatizadas
├── templates/
│   └── calculadora.html   # Interfaz web
├── README.md
└── requirements.txt
```

## Instalación

```powershell
pip install -r requirements.txt
```

## Ejecución

```powershell
python app_ventas.py
```

Luego abre: http://localhost:5000

## Pruebas

```powershell
python -m pytest test_calculo_ventas.py -v
```

## Reglas de Descuento

| Monto USD | Descuento |
|-----------|-----------|
| < 1.000   | 0%        |
| 1.000 - 9.999 | 10%   |
| ≥ 10.000  | 13%       |

## Flujo de Cálculo

1. Monto total en USD
2. → Aplicar descuento según tramo
3. → Convertir a CLP usando valor del dólar
4. → Calcular IVA (19%) sobre monto en CLP
5. → Total final = Neto CLP + IVA