import streamlit as st
import pandas as pd
from io import BytesIO

# Función para formatear como moneda


def formato_moneda(valor):
    """Convierte un número en formato moneda: $10.000.000,00."""
    try:
        return f"${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor > 0 else "$"
    except:
        return "$"

# Función principal


def calcular_din():
    # CSS personalizado para diseño
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        h1, h2, label {
            color: black;
            font-family: Arial, sans-serif;
        }
        .tabla {
            background: white;
            color: black;
            border: 1px solid black;
            font-family: Arial;
        }
        thead th {
            text-align: center;
            font-weight: bold;
            border: 1px solid black;
        }
        tbody td {
            border: 1px solid black;
        }
        </style>
    """, unsafe_allow_html=True)

    # Imagen inicial y título
    st.image(
        "https://www.comercioyaduanas.com.mx/storage/2015/04/porque-empezar-un-negocio-importando-o-exportando.jpg",
        caption="Bienvenido a la calculadora para la Provisión de Fondo",
        use_container_width=True
    )
    st.markdown("<h1>Calculadora DinProV</h1>", unsafe_allow_html=True)

    # Inicialización de sesión
    if "calculos" not in st.session_state:
        st.session_state.calculos = []
    if "resumen" not in st.session_state:
        st.session_state.resumen = []

    # Entrada de datos
    unidad_negocio = st.selectbox("Seleccione la unidad de negocio:", [
        "A000 - Compañía Cervecerías Unidas S.A.",
        "A023 - Cervecera CCU Chile LTDA",
        "A050 - Viña San Pedro Tarapacá S.A."
    ])
    numero_despacho = st.text_input(
        "Ingrese el número de despacho:", value="I-")

    valor_mercancia = st.text_input("Valor de la Mercancía (USD):", value="$")
    costo_flete = st.text_input("Costo del Flete (USD):", value="$")
    monto_seguro = st.text_input("Monto del Seguro (USD):", value="$")

    # Conversión segura
    def convertir_a_float(valor):
        try:
            return float(valor.strip("$").replace(".", "").replace(",", "."))
        except:
            return 0.0

    valor_mercancia = convertir_a_float(valor_mercancia)
    costo_flete = convertir_a_float(costo_flete)
    monto_seguro = convertir_a_float(monto_seguro)

    # Cálculos
    cif = valor_mercancia + costo_flete + monto_seguro
    st.write(f"Valor CIF: {formato_moneda(cif)}")

    ad_valorem = cif * 0.06
    st.write(f"Ad Valorem: {formato_moneda(ad_valorem)}")

    iva = (cif + ad_valorem) * 0.19
    st.write(f"IVA: {formato_moneda(iva)}")

    total_general = cif + ad_valorem + iva
    st.write(f"Total General: {formato_moneda(total_general)}")

    # Botón para agregar provisión
    if st.button("Agregar Provisión"):
        st.session_state.calculos.append({
            "Unidad de Negocio": unidad_negocio,
            "Despacho": numero_despacho,
            "Monto DIN": formato_moneda(total_general)
        })

    # Botón para restablecer
    if st.button("Restablecer"):
        st.session_state.calculos = []
        st.session_state.resumen = []

    # Tabla de provisión de fondos
    if st.session_state.calculos:
        df = pd.DataFrame(st.session_state.calculos)
        st.write("### Tabla Provisión de Fondos")
        st.dataframe(df.style.set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border-color': 'black'
        }))

    # Tabla resumen
    if st.session_state.calculos:
        resumen_df = pd.DataFrame(st.session_state.calculos)
        resumen_df["Monto DIN"] = resumen_df["Monto DIN"].apply(
            lambda x: convertir_a_float(x) if isinstance(x, str) else x
        )
        resumen = resumen_df.groupby("Unidad de Negocio", as_index=False)[
            "Monto DIN"].sum()
        resumen.loc[len(resumen)] = ["TOTAL", resumen["Monto DIN"].sum()]
        resumen["Monto DIN"] = resumen["Monto DIN"].apply(formato_moneda)

        st.write("### Tabla Resumen")
        st.dataframe(resumen.style.set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border-color': 'black'
        }))

        # Exportar ambas tablas a Excel
        if st.button("Exportar a Excel"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(
                    writer, sheet_name="Provisión de Fondos", index=False)
                resumen.to_excel(writer, sheet_name="Resumen", index=False)
            output.seek(0)
            st.download_button(
                label="Descargar Excel",
                data=output,
                file_name="provision_fondos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# Ejecutar aplicación
if __name__ == "__main__":
    calcular_din()
