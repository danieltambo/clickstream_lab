import React, { useEffect, useRef } from "react";
import ReactDOM from "react-dom/client";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

interface Props {
  args: {
    html?: string;
  };
}

const EmailComponent = ({ args }: Props) => {
  const { html = "" } = args;
  const hoverStartRef = useRef<number | null>(null);

  useEffect(() => {
    // Seleccionamos solo los elementos marcados con data-track
    const elements = document.querySelectorAll("[data-track]");

    const handleEnter = (e: Event) => {
      const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
      hoverStartRef.current = Date.now();
      Streamlit.setComponentValue({
        event: "hover_start",
        target,
        timestamp: hoverStartRef.current,
      });
    };

    const handleLeave = (e: Event) => {
      const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
      const now = Date.now();
      const duration = hoverStartRef.current ? now - hoverStartRef.current : 0;
      hoverStartRef.current = null;
      Streamlit.setComponentValue({
        event: "hover_end",
        target,
        duration,
        timestamp: now,
      });
    };

    const handleClick = (e: Event) => {
      const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
      Streamlit.setComponentValue({
        event: "click",
        target,
        timestamp: Date.now(),
      });
    };

    elements.forEach((el) => {
      el.addEventListener("mouseenter", handleEnter);
      el.addEventListener("mouseleave", handleLeave);
      el.addEventListener("click", handleClick);
    });

    return () => {
      elements.forEach((el) => {
        el.removeEventListener("mouseenter", handleEnter);
        el.removeEventListener("mouseleave", handleLeave);
        el.removeEventListener("click", handleClick);
      });
    };
  }, [html]);

  useEffect(() => {
    Streamlit.setComponentReady();
    // Streamlit.setFrameHeight(400);
    Streamlit.setFrameHeight(document.body.scrollHeight);
  }, []);

return (
  <div
    style={{
      padding: "0px",
      margin: "0px",
      backgroundColor: "transparent",
      fontFamily: "Arial, sans-serif",
    }}
    dangerouslySetInnerHTML={{ __html: html }}
  />
);

};

const Connected = withStreamlitConnection(EmailComponent);

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<Connected />);
}

export default Connected;
