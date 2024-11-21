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

    # 3. Inicialización de sesión y cálculo de provisiones
    if "calculos" not in st.session_state:
        st.session_state.calculos = []

    # 4. Entrada inicial con imagen
    st.image(
        "https://www.comercioyaduanas.com.mx/storage/2015/04/porque-empezar-un-negocio-importando-o-exportando.jpg",
        caption="Bienvenido a la calculadora para la Provisión de Fondo",
        use_container_width=True
    )

    # 5. Selección de Unidad de Negocio desde lista desplegable
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

    # 6. Ingreso de número de despacho con valor predeterminado
    numero_despacho = st.text_input(
        "Ingrese el número de despacho:", value="I-")

    # 7. Tasa para cada mercancía (directamente en el cálculo)
    tasas_mercancia = {
        "15%": 0.15,
        "50%": 0.50,
        "13%": 0.13,
        "15%": 0.15,
        "27%": 0.27,
        "0%": 0.0
    }

    tasa_impuesto = st.selectbox(
        "Seleccione la Tasa de Impuesto Adicional:", list(tasas_mercancia.keys()))
    tasa_impuesto_valor = tasas_mercancia[tasa_impuesto]

    # Mostrar el porcentaje de impuesto adicional
    st.write(f"Tasa de Impuesto Adicional Seleccionada: {tasa_impuesto}.")

    # 8. Entradas para cálculos: valor de la mercancía y costo de flete
    valor_mercancia = st.text_input("Valor de la Mercancía (USD):", value="$")
    costo_flete = st.text_input("Costo del Flete (USD):", value="$")

    # Asegurarse de que se ingresen valores válidos
    valor_mercancia = float(valor_mercancia.strip(
        "$").replace(",", "")) if valor_mercancia != "$" else 0
    costo_flete = float(costo_flete.strip("$").replace(
        ",", "")) if costo_flete != "$" else 0

    # 9. Cálculo de seguro, CIF y demás valores
    seguro = 0.1 * (valor_mercancia + costo_flete)
    cif = valor_mercancia + costo_flete + seguro

    st.write(f"Valor CIF: {formato_moneda(cif)}")
    st.write(f"Costo Seguro (10% del total de Mercancía y Flete): {
             formato_moneda(seguro)}")

    # 10. Cálculo de Ad Valorem
    opcion_ad_valorem = st.radio("¿Aplica Ad Valorem?", ("Sí", "No"))
    ad_valorem = cif * 0.06 if opcion_ad_valorem == "Sí" else 0.0
    st.write(f"Ad Valorem: {formato_moneda(ad_valorem)}")

    # 11. Cálculo del IVA
    iva = (cif + ad_valorem) * 0.19
    st.write(f"IVA: {formato_moneda(iva)}")

    # 12. Cálculo de Impuesto Adicional
    impuesto_adicional = (cif + ad_valorem) * tasa_impuesto_valor
    st.write(f"Impuesto Adicional: {formato_moneda(impuesto_adicional)}")

    # 13. Cálculos de Totales
    total_impuestos = ad_valorem + iva + impuesto_adicional
    total_general = cif + total_impuestos
    st.write(f"Total Impuestos: {formato_moneda(total_impuestos)}")
    st.write(f"Total General: {formato_moneda(total_general)}")

    # 14. Campo para observaciones
    observaciones = st.text_area(
        "¿Hay documentos pendientes? Agregue observaciones:")

    # 15. Agregar cálculo al historial
    if st.button("Agregar Provisión"):
        st.session_state.calculos.append({
            "Unidad de Negocio": unidad_negocio,
            "Despacho": numero_despacho,
            "Monto DIN": total_general,
            "Observaciones": observaciones
        })

    # 16. Mostrar historial de cálculos
    if st.session_state.calculos:
        st.write("### PROVISIÓN DE FONDOS")
        df = pd.DataFrame(st.session_state.calculos)
        st.table(df)

        # 17. Crear tabla resumen agrupando por unidad de negocio (sin observaciones)
        df_resumen = df.groupby("Unidad de Negocio", as_index=False)[
            "Monto DIN"].sum()
        st.write("### Provision por Unidad de Negocio")
        st.table(df_resumen)

        # 18. Exportar ambas tablas a Excel
        if st.button("Exportar a Excel"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Escribir la tabla completa
                df.to_excel(writer, index=False, sheet_name="Provisiones")
                start_row = len(df) + 4  # Dejar espacio entre tablas
                # Escribir el resumen a continuación
                df_resumen.to_excel(writer, startrow=start_row,
                                    index=False, sheet_name="Provisiones")
            buffer.seek(0)
            st.download_button("Descargar Excel", buffer,
                               "provision_fondos.xlsx")


# 19. Ejecutar la aplicación
if __name__ == "__main__":
    calcular_din()
