import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

# CONFIGURACIÓN DE CONEXIÓN A BASE DE DATOS

DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "parametros_alberca"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(page_title="Bitácora de Albercas", page_icon="🏊", layout="centered")

st.header("🏊 Bitácora de Parámetros de Albercas y cuerpos de agua Casa club")
st.markdown("Toma de lecturas de agua de albercas")


with st.form("parametros_form"):
    area = st.selectbox("Selecciona la alberca:", 
                        ["Alberca Interior", "Alberca Exterior", "Chapoteadero", "Jacuzzi adultos", "Jacuzzi niños", "Canal de Nado"])


    cloro = st.number_input("Cloro (ppm)", min_value=0.0, max_value=10.0, step=0.1)
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
    temperatura = st.number_input("Temperatura (°C)", min_value=0.0, max_value=50.0, step=0.5)
    claridad = st.selectbox("Claridad del agua:", ["Clara", "Turbia"])
    quimico = st.selectbox("¿Se agregó químico?", ["No", "Si"])
    quimico_agregado = st.text_input("¿Cual?")
    operador = st.text_input("Operador de turno")

    submit = st.form_submit_button("💾 Guardar registro")

if submit:
    try:
        # Crear DataFrame con los datos (sin fecha ni hora explícita)
        nuevo_registro = pd.DataFrame([{
            "area": area,
            "cloro": cloro,
            "ph": ph,
            "temperatura": temperatura,
            "claridad": claridad,
            "quimico": quimico,
            "quimico_agregado": quimico_agregado,
            "operador": operador
        }])

        nuevo_registro.to_sql("bitacora_albercas", engine, if_exists="append", index=False)
        st.success("✅ Registro guardado exitosamente.")
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")

