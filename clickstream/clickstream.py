
# Wrapper Python del componente frontend (JS/HTML) que permite integrar
# el tracking de interacciones del usuario (clickstream) en Streamlit

import os
import streamlit.components.v1 as components

# Declaramos el componente y especificamos la ruta al build generado con Parcel
#
_component_func = components.declare_component(
    "clickstream",
    path=os.path.join(os.path.dirname(__file__), "build")
)

# Expone el componente clickstream para su uso desde la app Streamlit
#
# Renderiza el componente y devuelve los eventos generados en el frontend
#
def clickstream (key=None, html=None):
    return _component_func(key=key, html=html)
