import os
import streamlit.components.v1 as components

# Declaramos el componente y le decimos dónde está el build de Parcel
_component_func = components.declare_component(
    "hello_component",
    path=os.path.join(os.path.dirname(__file__), "build")
)

#def hello_component(key=None):
#    return _component_func(key=key)

def hello_component(key=None, html=None):
    return _component_func(key=key, html=html)
