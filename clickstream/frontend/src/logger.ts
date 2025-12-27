/**
 * Evento atómico de interacción capturado en cliente.
 *
 * Representa acciones básicas (hover / click) sobre elementos
 * instrumentados mediante atributos data-track.
 *
 * No incluye métricas derivadas (latencias, TFA, heurísticos),
 * que se calculan posteriormente en el backend.
 */
export type ClickstreamEvent = {
  event: "hover_start" | "hover_end" | "click";
  target: string | null;
  timestamp: number;
  duration?: number;
};

/**
 * Registra listeners de interacción sobre el DOM renderizado
 * y emite eventos crudos de clickstream con timestamps locales.
 *
 * La función no interpreta ni agrega eventos:
 * su única responsabilidad es la instrumentación y emisión.
 */
export function attachClickstreamLogger(
  root: HTMLElement,
  emit: (e: ClickstreamEvent) => void
) {
  // Marca temporal de inicio de hover para calcular duración
  let hoverStart: number | null = null;

  // Selección de elementos explícitamente instrumentados (data-track)
  const elements = root.querySelectorAll("[data-track]");

  // Handler de entrada de hover: registra inicio y emite evento
  const onEnter = (e: Event) => {
    const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
    hoverStart = Date.now();
    emit({
      event: "hover_start",
      target,
      timestamp: hoverStart,
    });
  };

  // Handler de salida de hover: calcula duración y emite evento
  const onLeave = (e: Event) => {
    const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
    const now = Date.now();
    emit({
      event: "hover_end",
      target,
      duration: hoverStart ? now - hoverStart : 0,
      timestamp: now,
    });
    hoverStart = null;
  };

  // Handler de click: emite evento inmediato con timestamp
  const onClick = (e: Event) => {
    const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
    emit({
      event: "click",
      target,
      timestamp: Date.now(),
    });
  };

  elements.forEach((el) => {
    el.addEventListener("mouseenter", onEnter);
    el.addEventListener("mouseleave", onLeave);
    el.addEventListener("click", onClick);
  });

  // Función de cleanup: elimina listeners para evitar fugas de memoria
  return () => {
    elements.forEach((el) => {
      el.removeEventListener("mouseenter", onEnter);
      el.removeEventListener("mouseleave", onLeave);
      el.removeEventListener("click", onClick);
    });
  };
}
