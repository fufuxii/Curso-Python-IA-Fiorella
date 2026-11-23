import time


class Temporizador:

    def __init__(
        self,
        duracion_inicial=60,
        reduccion=10,
        minimo=10,
        reloj=time.monotonic
    ):
        self.duracion_inicial = duracion_inicial
        self.duracion = duracion_inicial
        self.reduccion = reduccion
        self.minimo = minimo

        self.palabras_encontradas = 0

        self._reloj = reloj
        self._inicio = None

    def iniciar(self):
        """Inicia el temporizador."""
        self._inicio = self._reloj()

    def reiniciar(self):
        """Reinicia el contador con la duración actual."""
        self._inicio = self._reloj()

    def registrar_palabra(self):
        """
        Registra una palabra válida y reinicia el tiempo.
        Cada 5 palabras reduce la duración en 10 segundos.
        """

        self.palabras_encontradas += 1

        if self.palabras_encontradas % 5 == 0:
            self.duracion = max(
                self.minimo,
                self.duracion - self.reduccion
            )

        self.reiniciar()

    @property
    def iniciado(self):
        return self._inicio is not None

    def restante(self):
        """Devuelve los segundos restantes."""

        if self._inicio is None:
            return self.duracion

        transcurrido = self._reloj() - self._inicio

        return max(0, self.duracion - transcurrido)

    @property
    def terminado(self):
        return self.iniciado and self.restante() <= 0

    def formateado(self):
        """Devuelve el tiempo en formato MM:SS."""

        segundos = int(self.restante() + 0.999)

        return f"{segundos // 60}:{segundos % 60:02d}"
