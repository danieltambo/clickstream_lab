/**
 * Renderer
 * --------
 * Componente responsable exclusivamente de renderizar el HTML
 * dentro del iframe.
 *
 * - No gestiona eventos
 * - No mide interacción
 * - No contiene lógica experimental
 *
 * La separación renderer / logger es intencional para mantener
 * una arquitectura clara y facilitar el análisis posterior.
 */

import React from "react";

// Props necesarias para renderizar el estímulo y exponer su nodo DOM al logger
interface RendererProps {
  html: string;
  containerRef: React.RefObject<HTMLDivElement>;
}

// Renderiza el HTML del estímulo y asigna la referencia al contenedor DOM
export const Renderer = ({ html, containerRef }: RendererProps) => {
  return (
    <div className="cs-root" ref={containerRef}>
      <div
        className="cs-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
};
