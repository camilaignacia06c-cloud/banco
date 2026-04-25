"""
Aplicación Flask para cálculo de ventas en pesos chilenos.
"""
from flask import Flask, render_template, request, jsonify
from calculo_ventas import calcular_total_venta, calcular_descuento, calcular_descuento_porcentaje, calcular_impuesto
from obtener_dolar import obtener_dolar_bcentral

app = Flask(__name__)


@app.route("/")
def home():
    """Página principal con el formulario de cálculo."""
    try:
        dolar_actual = obtener_dolar_bcentral()
    except:
        dolar_actual = 950.0  # Valor de fallback
    
    return render_template("calculadora.html", dolar_actual=dolar_actual)


@app.route("/calcular", methods=["POST"])
def calcular():
    """
    Endpoint para calcular el total de una venta.
    
    Recibe:
        - monto: Monto en dólares (USD)
        - valor_dolar: (opcional) Valor del dólar en CLP
    
    Retorna:
        - JSON con todos los cálculos realizados
    """
    try:
        monto = float(request.form.get("monto", 0))
        valor_dolar = request.form.get("valor_dolar")
        
        if valor_dolar:
            valor_dolar = float(valor_dolar)
        else:
            valor_dolar = None
        
        if monto <= 0:
            return jsonify({
                "error": "El monto debe ser mayor a 0"
            }), 400
        
        resultado = calcular_total_venta(monto, valor_dolar)
        return jsonify(resultado)
        
    except ValueError:
        return jsonify({
            "error": "Por favor ingrese un monto válido"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Error al calcular: {str(e)}"
        }), 500


@app.route("/api/descuento", methods=["GET"])
def api_descuento():
    """
    API para calcular solo el descuento.
    """
    monto = request.args.get("monto", type=float)
    
    if monto is None or monto <= 0:
        return jsonify({
            "error": "Por favor ingrese un monto válido"
        }), 400
    
    descuento = calcular_descuento(monto)
    porcentaje = calcular_descuento_porcentaje(monto)
    
    return jsonify({
        "monto_venta_usd": monto,
        "descuento_total_usd": descuento,
        "porcentaje_descuento": porcentaje
    })


@app.route("/api/iva", methods=["GET"])
def api_iva():
    """
    API para calcular solo el IVA.
    """
    monto_clp = request.args.get("monto_clp", type=float)
    
    if monto_clp is None or monto_clp <= 0:
        return jsonify({
            "error": "Por favor ingrese un monto válido en CLP"
        }), 400
    
    iva = calcular_impuesto(monto_clp)
    
    return jsonify({
        "monto_neto_clp": monto_clp,
        "monto_iva_clp": iva,
        "tasa_iva": "19%"
    })


@app.route("/api/dolar")
def api_dolar():
    """
    API para obtener el valor actual del dólar.
    """
    try:
        dolar = obtener_dolar_bcentral()
        return jsonify({
            "monto_dolar": dolar,
            "fuente": "Banco Central de Chile"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)