"""
Módulo de cálculo para ventas con descuentos e impuestos.
"""
from obtener_dolar import obtener_dolar_bcentral


# Constantes
TASA_IMPUESTO = 0.19  # 19% IVA en Chile


def calcular_descuento(monto_usd: float) -> float:
    """
    Calcula el monto de descuento aplicable según las reglas de negocio.
    
    Reglas de descuento:
    - Monto menor a 100 USD: Sin descuento (0%)
    - Monto mayor o igual a 1.000 USD: 10% de descuento
    - Monto mayor a 10.000 USD: 13% de descuento
    
    Args:
        monto_usd: Monto de la venta en dólares (USD)
    
    Returns:
        float: Monto del descuento en USD
    """
    if monto_usd > 10000:
        return monto_usd * 0.13  # 13% de descuento
    elif monto_usd >= 1000:
        return monto_usd * 0.10  # 10% de descuento
    else:
        return 0.0  # Sin descuento


def calcular_impuesto(monto_clp: float) -> float:
    """
    Calcula el monto del impuesto (IVA) sobre el monto en CLP.
    
    IMPORTANTE: El IVA se calcula sobre el monto en pesos chilenos (CLP),
    no sobre el monto en dólares.
    
    Args:
        monto_clp: Monto de la venta en pesos chilenos (CLP) después de descuento
    
    Returns:
        float: Monto del impuesto en CLP
    """
    return monto_clp * TASA_IMPUESTO


def calcular_total_venta(monto_usd: float, valor_dolar: float = None) -> dict:
    """
    Calcula el monto total de una venta en CLP.
    
    Proceso:
    1. Obtiene el valor del dólar (si no se proporciona)
    2. Aplica el descuento según las reglas
    3. Convierte a pesos chilenos
    4. Calcula el IVA (19%) sobre el monto en CLP
    5. Calcula el total final (neto + IVA)
    
    Args:
        monto_usd: Monto de la venta en dólares (USD)
        valor_dolar: Valor del dólar en CLP. Si es None, lo obtiene automáticamente.
    
    Returns:
        dict: Diccionario con todos los valores calculados
    """
    # Obtener valor del dólar si no se proporciona
    if valor_dolar is None:
        valor_dolar = obtener_dolar_bcentral()
    
    # Paso 1: Calcular monto total en USD
    monto_original_usd = monto_usd
    
    # Paso 2: Aplicar descuento según tramo
    monto_descuento = calcular_descuento(monto_usd)
    monto_neto_usd = monto_usd - monto_descuento
    
    # Paso 3: Convertir a CLP (monto neto sin IVA)
    monto_neto_clp = monto_neto_usd * valor_dolar
    
    # Paso 4: Calcular IVA sobre el monto en CLP
    monto_iva_clp = calcular_impuesto(monto_neto_clp)
    
    # Paso 5: Calcular total final en CLP
    monto_total_clp = monto_neto_clp + monto_iva_clp
    
    # Calcular porcentaje de descuento aplicado
    if monto_usd > 0:
        porcentaje_descuento = (monto_descuento / monto_usd) * 100
    else:
        porcentaje_descuento = 0
    
    return {
        "monto_dolar": valor_dolar,
        "monto_venta_usd": monto_original_usd,
        "descuento_total_usd": monto_descuento,
        "porcentaje_descuento": porcentaje_descuento,
        "monto_neto_clp": monto_neto_clp,
        "monto_iva_clp": monto_iva_clp,
        "monto_total_clp": monto_total_clp
    }


def calcular_descuento_porcentaje(monto_usd: float) -> float:
    """
    Retorna el porcentaje de descuento aplicable.
    
    Args:
        monto_usd: Monto de la venta en dólares (USD)
    
    Returns:
        float: Porcentaje de descuento (0, 10 o 13)
    """
    if monto_usd > 10000:
        return 13.0
    elif monto_usd >= 1000:
        return 10.0
    else:
        return 0.0


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 60)
    print("PRUEBAS DE CÁLCULO DE VENTAS")
    print("=" * 60)
    
    # Casos de prueba
    casos_prueba = [
        50,      # < 100 USD - sin descuento
        500,     # < 1000 USD - sin descuento
        1000,    # = 1000 USD - 10% descuento
        5000,    # >= 1000 y < 10000 - 10% descuento
        10000,   # = 10000 USD - 10% descuento
        15000,   # > 10000 USD - 13% descuento
    ]
    
    valor_dolar = 950.0  # Valor de prueba
    
    for monto in casos_prueba:
        resultado = calcular_total_venta(monto, valor_dolar)
        print(f"\nMonto: ${monto} USD")
        print(f"  Descuento: ${resultado['monto_descuento_usd']:.2f} USD ({resultado['porcentaje_descuento']:.0f}%)")
        print(f"  Impuesto: ${resultado['monto_impuesto_usd']:.2f} USD")
        print(f"  Total: ${resultado['subtotal_usd']:.2f} USD = ${resultado['total_clp']:,.0f} CLP")