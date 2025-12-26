import streamlit as st
import pandas as pd
import time
from hello_component import hello_component
import os

# --- Inicializar variables de sesión ---
if "page" not in st.session_state:
    st.session_state.page = "intro"

if "data" not in st.session_state:
    st.session_state.data = []  # lista donde guardaremos cada registro

# --- Función para pasar de página ---
def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- Ruta donde guardar el CSV ---
CSV_PATH = "resultados.csv"

# --- PÁGINA 1: Introducción ---
if st.session_state.page == "intro":
    st.title("🧠 Estudio sobre percepción de correos electrónicos")
    st.markdown("""
    Gracias por participar en este estudio.  
    Verás un correo y luego algunas preguntas.
    """)

    if st.button("Comenzar"):
        go_to("pl_item")

# --- PÁGINA 2: Ítem (correo) ---
elif st.session_state.page == "pl_item":
    st.header("Correo recibido 📩")

    email_html = """
    <div style='border:1px solid #ccc; padding:10px; border-radius:8px; margin-bottom:0;'>
        <b>Asunto:</b> Actualiza tu contraseña<br>
        <p>Hemos detectado actividad sospechosa en tu cuenta.<br>
        Por favor, <a href="#" data-track="cta">haz clic aquí</a> para verificar tu identidad.</p>
    </div>
    """

    event = hello_component(key="correo1", html=email_html)

    # Variables simuladas (en tu versión real vendrán del componente)
    metrics = {
        "correo_id": "C01",
        "hover_total": st.session_state.get("hover_total", 850),
        "hover_count": st.session_state.get("hover_count", 2),
        "click_link": st.session_state.get("link_clicked", False),
        "latencia_hover1": st.session_state.get("first_hover_latency", 1300),
        "rt": st.session_state.get("rt", 9.4),
    }

    st.session_state.current_metrics = metrics

    st.write("¿Crees que este correo es legítimo o phishing?")
    respuesta = st.radio("Selecciona una opción:", ["Legítimo", "Phishing"], index=None)

    if st.button("Siguiente") and respuesta:
        st.session_state.current_metrics["respuesta_pl"] = respuesta
        st.session_state.current_metrics["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.data.append(st.session_state.current_metrics)
        go_to("final")

# --- PÁGINA FINAL ---
elif st.session_state.page == "final":
    st.title("🎉 ¡Gracias por participar!")
    st.write("Tus respuestas se han registrado correctamente.")

    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)

    # Guardar el CSV en el servidor
    if not os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, index=False)
    else:
        df_existing = pd.read_csv(CSV_PATH)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_csv(CSV_PATH, index=False)

    st.success(f"✅ Datos guardados en {CSV_PATH}")
    st.download_button("Descargar CSV", df.to_csv(index=False), "resultados.csv", "text/csv")

    if st.button("Nuevo ensayo"):
        st.session_state.page = "intro"
        st.session_state.current_metrics = {}
        st.rerun()
