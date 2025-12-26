import streamlit as st

# --- Inicializar el estado de la página ---
if "page" not in st.session_state:
    st.session_state.page = "intro"

# --- Función para cambiar de página ---
def go_to(page_name: str):
    st.session_state["page"] = page_name
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

    html_email = """
    <div style='border:1px solid #ccc; padding:10px; border-radius:8px;'>
      <b>Asunto:</b> Actualiza tu contraseña<br>
      <p>Hemos detectado actividad sospechosa en tu cuenta.<br>
      Por favor, <a href="#">haz clic aquí</a> para verificar tu identidad.</p>
    </div>
    """
    st.markdown(html_email, unsafe_allow_html=True)

    st.write("¿Crees que este correo es legítimo o phishing?")
    respuesta = st.radio("Selecciona una opción:", ["Legítimo", "Phishing"], index=None)

    if st.button("Siguiente") and respuesta:
        st.session_state.respuesta_pl = respuesta
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
    st.write("Tus respuestas se han registrado correctamente.")
    st.write("Puedes cerrar esta ventana.")
