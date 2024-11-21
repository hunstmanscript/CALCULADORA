import streamlit as st
import pandas as pd
import io

# 1. Función para formatear números como moneda


def formato_moneda(valor):
    """Formatea un número como moneda con separador de miles (.) y decimales (,)."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 2. Función principal para manejar la lógica de la calculadora


def calcular_din():
    # Código CSS para agregar imagen de fondo y personalizar botones
    st.markdown("""
        <style>
        .reportview-container {
            background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeRE3pQeUDVVveJJYPJuMpfV_HDmGgb3VKKw&s");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .sidebar .sidebar-content {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .stButton>button {
            background-color: #0044cc;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #0066ff;
        }
        .header {
            text-align: center;
            font-size: 36px;
            font-family: 'Arial', sans-serif;
            color: #ffffff;
            background-color: rgba(0, 68, 204, 0.8);
            padding: 15px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header">Calculadora DinProV</div>',
                unsafe_allow_html=True)

    # 3. Inicialización de sesión
    if "calculos" not in st.session_state:
        st.session_state.calculos = []

    # 4. Entrada inicial
    st.image(
        "https://www.comercioyaduanas.com.mx/storage/2015/04/porque-empezar-un-negocio-importando-o-exportando.jpg",
        caption="Bienvenido a la calculadora para la Provisión de Fondo",
        use_container_width=True
    )

    # 5. Selección de Unidad de Negocio
    unidad_negocio = st.selectbox("Seleccione la unidad de negocio:", [
        "A000 - Compañía Cervecerías Unidas S.A.",
        "A023 - Cervecera CCU Chile LTDA",
        "A050 - Viña San Pedro Tarapacá S.A.",
        "A071 - Compañía Pisquera de Chile S.A.",
        "A060 - Cervecería Austral S.A.",
        "A063 - Cervecería Kunstmann S.A.",
        "A096 - Comercial CCU S.A.",
        "A081 - Manantial S.A.",
        "A090 - Embotelladoras Chilenas Unidas S.A.",
        "A031 - Fábrica de Envases Plásticos S.A.",
        "A080 - Aguas CCU-Nestlé Chile S.A.",
        "A082 - Bebidas CCU Pepsico",
        "A083 - Bebidas Ecusa SPA",
        "A061 - Comercial Patagona LTDA"
    ])

    # 6. Ingreso de número de despacho
    numero_despacho = st.text_input(
        "Ingrese el número de despacho:", value="I-")

    # 7. Tasa de impuesto adicional
    tasas_mercancia = {"15%": 0.15, "50%": 0.50, "13%": 0.13, "0%": 0.0}
    tasa_impuesto = st.selectbox(
        "Seleccione la Tasa de Impuesto Adicional:", list(tasas_mercancia.keys()))
    tasa_impuesto_valor = tasas_mercancia[tasa_impuesto]

    # 8. Entradas de cálculos: valor de la mercancía, flete y seguro
    valor_mercancia = st.text_input("Valor de la Mercancía (USD):", value="$")
    costo_flete = st.text_input("Costo del Flete (USD):", value="$")
    monto_seguro = st.text_input("Monto del Seguro (USD):", value="$")

    # Validación y conversión de valores
    valor_mercancia = float(valor_mercancia.strip(
        "$").replace(",", "")) if valor_mercancia != "$" else 0
    costo_flete = float(costo_flete.strip("$").replace(
        ",", "")) if costo_flete != "$" else 0
    monto_seguro = float(monto_seguro.strip("$").replace(
        ",", "")) if monto_seguro != "$" else 0

    # 9. Cálculo de CIF
    cif = valor_mercancia + costo_flete + monto_seguro
    st.write(f"Valor CIF: {formato_moneda(cif)}")

    # 10. Cálculo de Ad Valorem
    opcion_ad_valorem = st.radio("¿Aplica Ad Valorem?", ("Sí", "No"))
    ad_valorem = cif * 0.06 if opcion_ad_valorem == "Sí" else 0.0
    st.write(f"Ad Valorem: {formato_moneda(ad_valorem)}")

    # 11. Cálculo del IVA
    iva = (cif + ad_valorem) * 0.19
    st.write(f"IVA: {formato_moneda(iva)}")

    # 12. Impuesto adicional
    impuesto_adicional = (cif + ad_valorem) * tasa_impuesto_valor
    st.write(f"Impuesto Adicional: {formato_moneda(impuesto_adicional)}")

    # 13. Totales
    total_impuestos = ad_valorem + iva + impuesto_adicional
    total_general = cif + total_impuestos
    st.write(f"Total Impuestos: {formato_moneda(total_impuestos)}")
    st.write(f"Total General: {formato_moneda(total_general)}")

    # 14. Observaciones y provisiones
    observaciones = st.text_area(
        "¿Hay documentos pendientes? Agregue observaciones:")
    if st.button("Agregar Provisión"):
        st.session_state.calculos.append({
            "Unidad de Negocio": unidad_negocio,
            "Despacho": numero_despacho,
            "Monto DIN": total_general,
            "Observaciones": observaciones
        })

    # 15. Mostrar historial de cálculos
    if st.session_state.calculos:
        df = pd.DataFrame(st.session_state.calculos)
        st.write("### PROVISIÓN DE FONDOS")
        st.table(df)


# 16. Ejecutar aplicación
if __name__ == "__main__":
    calcular_din()
