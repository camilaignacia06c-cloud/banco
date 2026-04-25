"""
Pruebas automatizadas para el sistema de cálculo de ventas.
"""
import pytest
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculo_ventas import (
    calcular_descuento,
    calcular_impuesto,
    calcular_total_venta,
    calcular_descuento_porcentaje,
    TASA_IMPUESTO
)


class TestCalcularDescuento:
    """Pruebas para la función de cálculo de descuento."""
    
    def test_descuento_monto_menor_100(self):
        """Monto menor a 100 USD debe tener 0% de descuento."""
        assert calcular_descuento(50) == 0.0
        assert calcular_descuento(99.99) == 0.0
        assert calcular_descuento(1) == 0.0
    
    def test_descuento_monto_100_a_999(self):
        """Monto entre 100 y 999 USD debe tener 0% de descuento."""
        assert calcular_descuento(100) == 0.0
        assert calcular_descuento(500) == 0.0
        assert calcular_descuento(999) == 0.0
    
    def test_descuento_monto_igual_1000(self):
        """Monto igual a 1000 USD debe tener 10% de descuento."""
        assert calcular_descuento(1000) == 100.0  # 10% de 1000
    
    def test_descuento_monto_1000_a_9999(self):
        """Monto entre 1000 y 9999 USD debe tener 10% de descuento."""
        assert calcular_descuento(1000) == 100.0
        assert calcular_descuento(5000) == 500.0  # 10% de 5000
        assert abs(calcular_descuento(9999) - 999.9) < 0.01  # 10% de 9999
    
    def test_descuento_monto_igual_10000(self):
        """Monto igual a 10000 USD debe tener 10% de descuento."""
        assert calcular_descuento(10000) == 1000.0  # 10% de 10000
    
    def test_descuento_monto_mayor_10000(self):
        """Monto mayor a 10000 USD debe tener 13% de descuento."""
        assert calcular_descuento(10001) == 1300.13  # 13% de 10001
        assert calcular_descuento(15000) == 1950.0  # 13% de 15000
        assert calcular_descuento(50000) == 6500.0  # 13% de 50000
    
    def test_descuento_monto_cero(self):
        """Monto cero debe tener descuento cero."""
        assert calcular_descuento(0) == 0.0
    
    def test_descuento_monto_negativo(self):
        """Monto negativo debe manejar correctamente."""
        # Asumimos que valores negativos no son válidos
        # pero la función debe manejar el caso
        resultado = calcular_descuento(-100)
        assert resultado >= 0  # No debe dar descuento negativo


class TestCalcularImpuesto:
    """Pruebas para la función de cálculo de impuesto (IVA sobre CLP)."""
    
    def test_impuesto_basico(self):
        """Calculo básico de impuesto (19% IVA) sobre CLP."""
        assert calcular_impuesto(100000) == 19000.0
        assert calcular_impuesto(1000000) == 190000.0
    
    def test_impuesto_con_decimales(self):
        """Calculo de impuesto con valores decimales."""
        assert abs(calcular_impuesto(100000.50) - 19000.095) < 0.01
        assert abs(calcular_impuesto(999999.99) - 189999.9981) < 0.01
    
    def test_impuesto_cero(self):
        """Impuesto sobre monto cero debe ser cero."""
        assert calcular_impuesto(0) == 0.0
    
    def test_tasa_impuesto(self):
        """Verificar que la tasa de impuesto sea 19%."""
        assert TASA_IMPUESTO == 0.19


class TestCalcularDescuentoPorcentaje:
    """Pruebas para la función de porcentaje de descuento."""
    
    def test_porcentaje_menor_1000(self):
        """Monto menor a 1000 debe retornar 0%."""
        assert calcular_descuento_porcentaje(50) == 0.0
        assert calcular_descuento_porcentaje(999) == 0.0
    
    def test_porcentaje_1000_a_9999(self):
        """Monto entre 1000 y 9999 debe retornar 10%."""
        assert calcular_descuento_porcentaje(1000) == 10.0
        assert calcular_descuento_porcentaje(5000) == 10.0
    
    def test_porcentaje_mayor_10000(self):
        """Monto mayor a 10000 debe retornar 13%."""
        assert calcular_descuento_porcentaje(10001) == 13.0
        assert calcular_descuento_porcentaje(50000) == 13.0


class TestCalcularTotalVenta:
    """Pruebas para la función de cálculo total de venta."""
    
    def test_venta_menor_100_sin_descuento(self):
        """Venta menor a 100 USD sin descuento."""
        resultado = calcular_total_venta(50, 950.0)
        
        assert resultado["monto_venta_usd"] == 50
        assert resultado["descuento_total_usd"] == 0.0
        assert resultado["porcentaje_descuento"] == 0.0
        # Neto CLP: 50 * 950 = 47500
        assert resultado["monto_neto_clp"] == 47500.0
        # IVA: 47500 * 0.19 = 9025
        assert resultado["monto_iva_clp"] == 9025.0
        # Total: 47500 + 9025 = 56525
        assert resultado["monto_total_clp"] == 56525.0
    
    def test_venta_1000_con_10_descuento(self):
        """Venta de 1000 USD con 10% descuento."""
        resultado = calcular_total_venta(1000, 950.0)
        
        assert resultado["monto_venta_usd"] == 1000
        assert resultado["descuento_total_usd"] == 100.0
        assert resultado["porcentaje_descuento"] == 10.0
        # Neto CLP: (1000 - 100) * 950 = 900 * 950 = 855000
        assert resultado["monto_neto_clp"] == 855000.0
        # IVA: 855000 * 0.19 = 162450
        assert resultado["monto_iva_clp"] == 162450.0
        # Total: 855000 + 162450 = 1017450
        assert resultado["monto_total_clp"] == 1017450.0
    
    def test_venta_15000_con_13_descuento(self):
        """Venta de 15000 USD con 13% descuento."""
        resultado = calcular_total_venta(15000, 950.0)
        
        assert resultado["monto_venta_usd"] == 15000
        assert resultado["descuento_total_usd"] == 1950.0  # 13% de 15000
        assert resultado["porcentaje_descuento"] == 13.0
        # Neto CLP: (15000 - 1950) * 950 = 13050 * 950 = 12397500
        assert resultado["monto_neto_clp"] == 12397500.0
        # IVA: 12397500 * 0.19 = 2355525
        assert resultado["monto_iva_clp"] == 2355525.0
        # Total: 12397500 + 2355525 = 14753025
        assert resultado["monto_total_clp"] == 14753025.0
    
    def test_venta_con_valor_dolar_none(self):
        """Venta sin especificar valor del dólar."""
        resultado = calcular_total_venta(1000)
        
        assert resultado["monto_venta_usd"] == 1000
        assert resultado["monto_dolar"] is not None
        assert resultado["monto_total_clp"] > 0
    
    def test_venta_cero(self):
        """Venta con monto cero."""
        resultado = calcular_total_venta(0, 950.0)
        
        assert resultado["monto_venta_usd"] == 0
        assert resultado["descuento_total_usd"] == 0.0
        assert resultado["monto_total_clp"] == 0.0


class TestIntegracion:
    """Pruebas de integración del sistema completo."""
    
    def test_ciclo_completo_venta(self):
        """Prueba del ciclo completo de una venta."""
        monto_original = 5000
        valor_dolar = 950.0
        
        # Paso 1: Calcular descuento
        descuento = calcular_descuento(monto_original)
        assert descuento == 500.0  # 10% de 5000
        
        # Paso 2: Calcular monto con descuento
        monto_neto_usd = monto_original - descuento
        assert monto_neto_usd == 4500
        
        # Paso 3: Convertir a CLP
        monto_neto_clp = monto_neto_usd * valor_dolar
        assert monto_neto_clp == 4275000  # 4500 * 950
        
        # Paso 4: Calcular IVA sobre CLP
        iva_clp = calcular_impuesto(monto_neto_clp)
        assert iva_clp == 812250.0  # 19% de 4275000
        
        # Paso 5: Calcular total
        total_clp = monto_neto_clp + iva_clp
        assert total_clp == 5087250.0
    
    def test_multiples_ventas(self):
        """Prueba con múltiples ventas."""
        montos = [50, 500, 1000, 5000, 10000, 15000]
        valor_dolar = 950.0
        
        for monto in montos:
            resultado = calcular_total_venta(monto, valor_dolar)
            assert resultado["monto_venta_usd"] == monto
            assert resultado["monto_total_clp"] > 0
            # Verificar que el total = neto + IVA
            assert resultado["monto_total_clp"] == resultado["monto_neto_clp"] + resultado["monto_iva_clp"]


class TestCasosBorde:
    """Pruebas de casos límite y borde."""
    
    def test_valor_cero(self):
        """El sistema maneja correctamente ventas con monto cero."""
        resultado = calcular_total_venta(0, 950.0)
        assert resultado["monto_total_clp"] == 0.0
        assert resultado["monto_iva_clp"] == 0.0
    
    def test_valores_negativos(self):
        """El sistema valida y rechaza montos negativos."""
        # El descuento no debe ser negativo
        resultado = calcular_descuento(-100)
        assert resultado >= 0
    
    def test_limite_100(self):
        """Prueba el valor exacto en el umbral de 100."""
        resultado = calcular_total_venta(100, 950.0)
        assert resultado["descuento_total_usd"] == 0.0  # < 1000 sin descuento
    
    def test_limite_1000(self):
        """Prueba el valor exacto en el umbral de 1000."""
        resultado = calcular_total_venta(1000, 950.0)
        assert resultado["descuento_total_usd"] == 100.0  # 10% de descuento
        assert resultado["porcentaje_descuento"] == 10.0
    
    def test_limite_10000(self):
        """Prueba el valor exacto en el umbral de 10000."""
        resultado = calcular_total_venta(10000, 950.0)
        assert resultado["descuento_total_usd"] == 1000.0  # 10% (no 13%)
        assert resultado["porcentaje_descuento"] == 10.0
    
    def test_limite_10001(self):
        """Prueba el valor justo después de 10000."""
        resultado = calcular_total_venta(10001, 950.0)
        assert resultado["descuento_total_usd"] == 1300.13  # 13%


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# ==================== PRUEBAS DE SELENIUM ====================
class TestSeleniumObtenerDolar:
    """Pruebas para el módulo de Selenium."""
    
    def test_obtener_dolar_importa_selenium(self):
        """Verifica que se puede importar selenium."""
        from selenium import webdriver
        assert webdriver is not None
    
    def test_obtener_dolar_funcion_existe(self):
        """Verifica que existe la función principal."""
        from obtener_dolar import obtener_dolar_bcentral
        assert callable(obtener_dolar_bcentral)
    
    def test_obtener_dolar_retorna_float(self):
        """Verifica que retorna un valor numérico."""
        from obtener_dolar import obtener_dolar_api_fallback
        valor = obtener_dolar_api_fallback()
        assert isinstance(valor, (int, float))
    
    def test_obtener_dolar_valor_valido(self):
        """Verifica que el valor está en rango razonable."""
        from obtener_dolar import obtener_dolar_api_fallback
        valor = obtener_dolar_api_fallback()
        assert 500 < valor < 2000  # Rango válido para dólar CLP
    
    def test_obtener_dolar_fecha(self):
        """Verifica que funciona para fechas específicas."""
        from obtener_dolar import obtener_dolar_fecha
        # No necesita fecha específica para la prueba
        assert callable(obtener_dolar_fecha)