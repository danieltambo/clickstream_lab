import streamlit as st
from hello_component import hello_component

email_html = """
  <p>Estimado usuario,</p>
  <p>Hemos detectado actividad sospechosa en su cuenta.</p>
  <a href="#" data-track="cta" style="color:#0056b3;text-decoration:none;">Verificar cuenta</a>
"""

st.title("📧 Test de hover + click sobre enlace")
event = hello_component(key="correo1", html=email_html)
st.write(event)

# st.title("🧩 Test de componente")
# event = hello_component(key="correo1")
# st.write("Evento recibido:", event)
