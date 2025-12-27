/**
 * Punto de entrada del componente clickstream.
 *
 * Coordina el ciclo completo del componente:
 * - renderizado del estímulo HTML
 * - captura e instrumentación de eventos de interacción
 * - envío de eventos al backend de Streamlit
 *
 * Actúa como frontera explícita entre:
 * frontend (medición conductual y timestamps)
 * backend (recogida y análisis de datos)
 */
import React, { useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

import { Renderer } from "./renderer";
import { attachClickstreamLogger } from "./logger";

// Define los argumentos de entrada enviados desde Python (Streamlit)
interface Props {
  args: {
    html?: string;
  };
}

// Componente principal que renderiza el estímulo y gestiona la captura de eventos
const App = ({ args }: Props) => {
  const { html = "" } = args;
  const containerRef = useRef<HTMLDivElement>(null);

  // Inicializa la captura de interacciones dentro del contenedor y envía cada evento registrado a Streamlit
  useEffect(() => {
    if (!containerRef.current) return;

    const detach = attachClickstreamLogger(
      containerRef.current,
      (event) => {
        Streamlit.setComponentValue(event);
      }
    );

    return detach;
  }, [html]);


  // Señala a Streamlit que el componente está listo y ajusta el alto del iframe
  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight();
  });

  // Envia tiempo inicial (t0) al cliente
  useEffect(() => {
    const t0 = Date.now();

    Streamlit.setComponentValue({
      event: "render",
      timestamp: t0,
    });
  }, [html]);

  return <Renderer html={html} containerRef={containerRef} />;
};

// Conecta el componente al ciclo de vida de Streamlit
const Connected = withStreamlitConnection(App);

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<Connected />);
}
