"""
Servicio de aplicación para la gestión de la Agenda de Tareas.

Coordina las operaciones CRUD, búsqueda filtrada, prevención de títulos
duplicados en tareas activas y generación de métricas de resumen.
"""

from typing import Dict, List, Optional

from src.excepciones import ErrorValidacionTarea, TareaNoEncontradaError
from src.modelos import EstadoTarea, Prioridad, Tarea
from src.validadores import validar_entero_positivo, validar_instancia_enum


class GestorTareas:
    """
    Gestiona el ciclo de vida de una colección de tareas en memoria
    garantizando la integridad de datos y las reglas de negocio.
    """

    def __init__(self) -> None:
        self._tareas: Dict[int, Tarea] = {}
        self._siguiente_id: int = 1

    def crear_tarea(
        self,
        titulo: str,
        descripcion: str = "",
        prioridad: Prioridad | str = Prioridad.MEDIA,
    ) -> Tarea:
        """
        Registra una nueva tarea validando sus campos y evitando títulos
        duplicados entre las tareas activas (PENDIENTE o EN_PROGRESO).
        """
        if isinstance(titulo, str):
            titulo_normalizado = titulo.strip().lower()
            for tarea_existente in self._tareas.values():
                if (
                    tarea_existente.estado != EstadoTarea.COMPLETADA
                    and tarea_existente.titulo.lower() == titulo_normalizado
                ):
                    raise ErrorValidacionTarea(
                        f"Ya existe una tarea activa con el título '{tarea_existente.titulo}'."
                    )

        nueva_tarea = Tarea(
            id_tarea=self._siguiente_id,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
        )
        self._tareas[self._siguiente_id] = nueva_tarea
        self._siguiente_id += 1
        return nueva_tarea

    def obtener_tarea(self, id_tarea: int) -> Tarea:
        """
        Obtiene una tarea por su identificador único.
        Lanza TareaNoEncontradaError si no existe.
        """
        id_validado = validar_entero_positivo(id_tarea, "id_tarea")
        tarea = self._tareas.get(id_validado)
        if tarea is None:
            raise TareaNoEncontradaError(
                f"No se encontró ninguna tarea con el ID #{id_validado}."
            )
        return tarea

    def listar_tareas(
        self,
        estado: Optional[EstadoTarea | str] = None,
        prioridad: Optional[Prioridad | str] = None,
    ) -> List[Tarea]:
        """
        Retorna la lista de tareas registradas, permitiendo filtrar
        opcionalmente por estado y/o prioridad.
        """
        resultado = list(self._tareas.values())

        if estado is not None:
            estado_validado = validar_instancia_enum(
                estado, EstadoTarea, "estado"
            )
            resultado = [t for t in resultado if t.estado == estado_validado]

        if prioridad is not None:
            prioridad_validada = validar_instancia_enum(
                prioridad, Prioridad, "prioridad"
            )
            resultado = [
                t for t in resultado if t.prioridad == prioridad_validada
            ]

        return resultado

    def cambiar_estado_tarea(
        self, id_tarea: int, nuevo_estado: EstadoTarea | str
    ) -> Tarea:
        """Cambia el estado de una tarea existente respetando las transiciones válidas."""
        tarea = self.obtener_tarea(id_tarea)
        tarea.cambiar_estado(nuevo_estado)
        return tarea

    def actualizar_prioridad_tarea(
        self, id_tarea: int, nueva_prioridad: Prioridad | str
    ) -> Tarea:
        """Actualiza la prioridad de una tarea existente si aún no está completada."""
        tarea = self.obtener_tarea(id_tarea)
        tarea.actualizar_prioridad(nueva_prioridad)
        return tarea

    def eliminar_tarea(self, id_tarea: int) -> Tarea:
        """Elimina una tarea existente por su ID y retorna la instancia eliminada."""
        tarea = self.obtener_tarea(id_tarea)
        del self._tareas[tarea.id_tarea]
        return tarea

    def obtener_resumen(self) -> Dict[str, int]:
        """Calcula contadores generales por estado y prioridad alta."""
        tareas = list(self._tareas.values())
        return {
            "total": len(tareas),
            "pendientes": sum(
                1 for t in tareas if t.estado == EstadoTarea.PENDIENTE
            ),
            "en_progreso": sum(
                1 for t in tareas if t.estado == EstadoTarea.EN_PROGRESO
            ),
            "completadas": sum(
                1 for t in tareas if t.estado == EstadoTarea.COMPLETADA
            ),
            "alta_prioridad": sum(
                1 for t in tareas if t.prioridad == Prioridad.ALTA
            ),
        }
