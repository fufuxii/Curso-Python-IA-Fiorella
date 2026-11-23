"""Temporizador basado en reloj monotónico (compatible con Streamlit:
solo guarda el instante de inicio, no necesita hilos)."""
import time


class Temporizador:
    def __init__(self, duracion: float, reloj=time.monotonic):
        self.duracion = duracion
        self._reloj = reloj
        self._inicio: float | None = None

    def iniciar(self) -> None:
        self._inicio = self._reloj()

    @property
    def iniciado(self) -> bool:
        return self._inicio is not None

    def restante(self) -> float:
        if self._inicio is None:
            return self.duracion
        return max(0.0, self.duracion - (self._reloj() - self._inicio))

    @property
    def terminado(self) -> bool:
        return self.iniciado and self.restante() <= 0

    def formateado(self) -> str:
        s = int(self.restante() + 0.999)
        return f"{s // 60}:{s % 60:02d}"