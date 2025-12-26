import streamlit as st

st.title("Prueba rápida de Streamlit desde VS Code 🎯")

html_email = """
<div style='border:1px solid #ccc; padding:10px; border-radius:8px;'>
  <b>Asunto:</b> Actualiza tu contraseña<br>
  <p>Hemos detectado actividad sospechosa en tu cuenta.<br>
  Por favor, <a href="#">haz clic aquí</a> para verificar tu identidad.</p>
</div>
"""
st.markdown(html_email, unsafe_allow_html=True)

confianza = st.slider("¿Qué tan confiable te parece este correo?", 0, 100, 50)

if st.button("Enviar"):
    st.success(f"Has marcado {confianza}/100 de confianza.")
