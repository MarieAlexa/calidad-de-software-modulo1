"""
Modelos de dominio para la Agenda de Tareas.

Define las enumeraciones de Prioridad y EstadoTarea, las reglas de transición
de estados permitidas y la entidad principal Tarea.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Set

from src.excepciones import TransicionEstadoInvalidaError
from src.validadores import (
    LONGITUD_MAXIMA_DESCRIPCION,
    LONGITUD_MAXIMA_TITULO,
    LONGITUD_MINIMA_TITULO,
    validar_entero_positivo,
    validar_instancia_enum,
    validar_texto_rango,
)


class Prioridad(Enum):
    """Niveles de prioridad permitidos para una tarea."""

    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class EstadoTarea(Enum):
    """Estados posibles dentro del ciclo de vida de una tarea."""

    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"


TRANSICIONES_PERMITIDAS: Dict[EstadoTarea, Set[EstadoTarea]] = {
    EstadoTarea.PENDIENTE: {EstadoTarea.EN_PROGRESO, EstadoTarea.COMPLETADA},
    EstadoTarea.EN_PROGRESO: {EstadoTarea.PENDIENTE, EstadoTarea.COMPLETADA},
    EstadoTarea.COMPLETADA: set(),
}


@dataclass
class Tarea:
    """
    Entidad de dominio que representa una tarea dentro de la agenda.
    Aplica validaciones automáticas al instanciarse y controla sus transiciones.
    """

    id_tarea: int
    titulo: str
    descripcion: str = ""
    prioridad: Prioridad = Prioridad.MEDIA
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    fecha_creacion: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self.id_tarea = validar_entero_positivo(self.id_tarea, "id_tarea")
        self.titulo = validar_texto_rango(
            self.titulo,
            "titulo",
            min_len=LONGITUD_MINIMA_TITULO,
            max_len=LONGITUD_MAXIMA_TITULO,
            permitir_vacio=False,
        )
        self.descripcion = validar_texto_rango(
            self.descripcion,
            "descripcion",
            min_len=0,
            max_len=LONGITUD_MAXIMA_DESCRIPCION,
            permitir_vacio=True,
        )
        self.prioridad = validar_instancia_enum(
            self.prioridad, Prioridad, "prioridad"
        )
        self.estado = validar_instancia_enum(
            self.estado, EstadoTarea, "estado"
        )

    def cambiar_estado(self, nuevo_estado: EstadoTarea | str) -> None:
        """
        Actualiza el estado de la tarea verificando que la transición sea válida.
        Una tarea COMPLETADA se considera finalizada y no admite nuevos cambios de estado.
        """
        estado_destino = validar_instancia_enum(
            nuevo_estado, EstadoTarea, "estado"
        )

        if self.estado == EstadoTarea.COMPLETADA:
            raise TransicionEstadoInvalidaError(
                f"La tarea #{self.id_tarea} ya está COMPLETADA y no puede cambiar de estado."
            )

        if self.estado == estado_destino:
            raise TransicionEstadoInvalidaError(
                f"La tarea #{self.id_tarea} ya se encuentra en el estado '{estado_destino.value}'."
            )

        estados_validos = TRANSICIONES_PERMITIDAS.get(self.estado, set())
        if estado_destino not in estados_validos:
            raise TransicionEstadoInvalidaError(
                f"Transición no permitida de '{self.estado.value}' a '{estado_destino.value}'."
            )

        self.estado = estado_destino

    def actualizar_prioridad(self, nueva_prioridad: Prioridad | str) -> None:
        """
        Actualiza la prioridad de la tarea, siempre que no esté completada.
        """
        if self.estado == EstadoTarea.COMPLETADA:
            raise TransicionEstadoInvalidaError(
                f"No se puede modificar la prioridad de la tarea #{self.id_tarea} porque está COMPLETADA."
            )

        self.prioridad = validar_instancia_enum(
            nueva_prioridad, Prioridad, "prioridad"
        )

    def a_diccionario(self) -> dict:
        """Retorna una representación en diccionario de la tarea."""
        return {
            "id_tarea": self.id_tarea,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad.value,
            "estado": self.estado.value,
            "fecha_creacion": self.fecha_creacion.isoformat(timespec="seconds"),
        }
