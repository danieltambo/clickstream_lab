import React from "react";

interface RendererProps {
  html: string;
  containerRef: React.RefObject<HTMLDivElement>;
}

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
