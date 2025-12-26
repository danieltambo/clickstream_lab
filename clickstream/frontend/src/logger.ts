export type ClickstreamEvent = {
  event: "hover_start" | "hover_end" | "click";
  target: string | null;
  timestamp: number;
  duration?: number;
};

export function attachClickstreamLogger(
  root: HTMLElement,
  emit: (e: ClickstreamEvent) => void
) {
  let hoverStart: number | null = null;

  const elements = root.querySelectorAll("[data-track]");

  const onEnter = (e: Event) => {
    const target = (e.currentTarget as HTMLElement).getAttribute("data-track");
    hoverStart = Date.now();
    emit({
      event: "hover_start",
      target,
      timestamp: hoverStart,
    });
  };

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

  return () => {
    elements.forEach((el) => {
      el.removeEventListener("mouseenter", onEnter);
      el.removeEventListener("mouseleave", onLeave);
      el.removeEventListener("click", onClick);
    });
  };
}
