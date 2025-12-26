import streamlit as st
from clickstream import clickstream


st.header ("🧪 Test  de Clickstream")

# HTML MINIMALISTA Y CONTROLADO
email_html = """
    <div style='border:0px solid #ccc; padding:10px; border-radius:8px; margin-bottom:0;'>
        <b>Asunto:</b> Actualiza tu contraseña<br>
        <p>Hemos detectado actividad sospechosa en tu cuenta.<br><br>
        Por favor, <a href="#" data-track="cta">haz clic aquí</a> para verificar tu identidad.<br></p>
        <p> O aqui tambien puede...<a href="#" data-track="cta_secondary">Más información</a> </p>
    </div>
    """
event = clickstream(
    key="test_clickstream",
    html=email_html
)

st.subheader("Evento capturado")
st.write(event)


