import React, { useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

import { Renderer } from "./renderer";
import { attachClickstreamLogger } from "./logger";

interface Props {
  args: {
    html?: string;
  };
}

const App = ({ args }: Props) => {
  const { html = "" } = args;
  const containerRef = useRef<HTMLDivElement>(null);

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

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight();
  });

  // Para enviar tiempo inicial (t0) al cliente
  useEffect(() => {
    const t0 = Date.now();

    Streamlit.setComponentValue({
      event: "render",
      timestamp: t0,
    });
  }, [html]);

  return <Renderer html={html} containerRef={containerRef} />;
};

const Connected = withStreamlitConnection(App);

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<Connected />);
}
