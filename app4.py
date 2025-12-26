import streamlit as st
import pandas as pd
import time
from hello_component import hello_component  # 👈 nuestro componente

# --- Inicializar estado ---
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Variables de control del hover
if "hover_total" not in st.session_state:
    st.session_state.hover_total = 0.0
if "hover_active" not in st.session_state:
    st.session_state.hover_active = False
if "hover_start_time" not in st.session_state:
    st.session_state.hover_start_time = None

# --- Función para cambiar de página ---
def go_to(page_name: str):
    st.session_state.page = page_name
    st.rerun()

# --- PÁGINA 1: Introducción ---
if st.session_state.page == "intro":
    st.title("🧠 Estudio sobre percepción de correos electrónicos")
    st.markdown("""
    Gracias por participar en este estudio.  
    En este test verás un correo electrónico y después algunas preguntas.
    """)

    if st.button("Comenzar"):
        go_to("pl_item")

# --- PÁGINA 2: Ítem P/L ---
elif st.session_state.page == "pl_item":
    st.header("Correo recibido 📩")
    
    #Reseteamos el hovert_total
    st.session_state.hover_total = 0.0
    st.session_state.link_clicked = False


    email_html = """
    <div style='border:1px solid #ccc; padding:10px; border-radius:8px; margin-bottom:0;'>
        <b>Asunto:</b> Actualiza tu contraseña<br>
        <p>Hemos detectado actividad sospechosa en tu cuenta.<br>
    Por favor, <a href="#" data-track="cta">haz clic aquí</a> para verificar tu identidad.</p>
    </div>
    """


    # --- Mostrar el correo con el componente (detecta hover/click) ---
    event = hello_component(key="correo1", html=email_html)

    # --- Registrar eventos de hover ---
    if event:
        if event.get("event") == "hover_start":
            st.session_state.hover_active = True
            st.session_state.hover_start_time = event.get("timestamp")

        elif event.get("event") == "hover_end":
            dur = event.get("duration", 0)
            st.session_state.hover_total += dur
            st.session_state.hover_active = False

        elif event.get("event") == "click":
            st.session_state.link_clicked = True

    # --- Mostrar feedback al investigador ---
    # st.info(f"Hover acumulado: {round(st.session_state.hover_total/1000, 2)} segundos")
    # st.write("Último evento:", event)
    # --- (Opcional) Solo mostrar si modo debug --- 
    if st.session_state.get("debug", False):
        st.info(f"Hover acumulado: {round(st.session_state.hover_total/1000, 2)} segundos")
        st.write("Último evento:", event)


    # --- Guardar hora de inicio del ítem (RT) ---
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # --- Pregunta P/L ---
    st.write("¿Crees que este correo es legítimo o phishing?")
    respuesta = st.radio("Selecciona una opción:", ["Legítimo", "Phishing"], index=None)

    if st.button("Siguiente") and respuesta:
        end_time = time.time()
        st.session_state.respuesta_pl = respuesta
        st.session_state.rt = round(end_time - st.session_state.start_time, 3)
        go_to("likert")

# --- PÁGINA 3: Ítem Likert ---
elif st.session_state.page == "likert":
    st.header("Valoración del correo")

    confianza = st.slider(
        "¿Qué tan seguro estás de tu respuesta anterior?",
        0, 100, 50
    )

    if st.button("Continuar"):
        st.session_state.confianza = confianza
        go_to("final")

# --- PÁGINA 4: Despedida ---
elif st.session_state.page == "final":
    st.title("🎉 ¡Gracias por participar!")
    st.markdown("#### 🧾 Resumen de tus respuestas")

    resumen = {
        "Variable": [
            "Evaluación del correo",
            "Nivel de confianza",
            "Tiempo de respuesta (s)",
            "Tiempo total de hover (s)",
            "Ha hecho clic?"
        ],
        "Valor": [
            st.session_state.get("respuesta_pl", "—"),
            str(st.session_state.get("confianza", "—")),
            str(st.session_state.get("rt", "—")),
            str(round(st.session_state.get("hover_total", 0) / 1000, 2)),
            str(st.session_state.get("link_clicked","-")),
        ],
    }

    df = pd.DataFrame(resumen)
    st.table(df)

    st.markdown("---")
    st.write("Tus respuestas se han registrado correctamente.")
    st.write("Puedes cerrar esta ventana.")
