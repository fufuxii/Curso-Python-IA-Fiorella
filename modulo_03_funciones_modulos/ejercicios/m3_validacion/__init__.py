"""Módulo 3 - Práctica 3: librería de validación de datos.

El paquete agrupa las validaciones en tres módulos: ``texto``, ``numeros`` y
``fechas``. Este fichero reexporta las funciones más usadas.
"""

from .texto import esta_vacio, normalizar_nombre, es_email, es_dni
from .numeros import es_entero, es_decimal, a_decimal, en_rango
from .fechas import es_fecha, edad, es_mayor_de_edad

__all__ = [
    "esta_vacio",
    "normalizar_nombre",
    "es_email",
    "es_dni",
    "es_entero",
    "es_decimal",
    "a_decimal",
    "en_rango",
    "es_fecha",
    "edad",
    "es_mayor_de_edad",
]

__version__ = "1.0.0"
