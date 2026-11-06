"""
Suite de pruebas unitarias y funcionales para el Sistema de Agenda de Tareas.

Parte 1: Flujos Correctos (Happy Path) - CP-01 a CP-05.
"""

import unittest

from src.gestor_tareas import GestorTareas
from src.modelos import EstadoTarea, Prioridad


class TestAgendaTareas(unittest.TestCase):
    """Pruebas sistemáticas del dominio y del servicio GestorTareas."""

    def setUp(self) -> None:
        """Inicializa un gestor limpio antes de cada caso de prueba."""
        self.gestor = GestorTareas()

    # =========================================================================
    # 1. FLUJOS CORRECTOS (HAPPY PATH)
    # =========================================================================

    def test_cp01_crear_tarea_valida_asigna_estado_pendiente_e_id_incremental(self) -> None:
        """CP-01: Crear una tarea válida con título, descripción y prioridad ALTA."""
        tarea = self.gestor.crear_tarea(
            titulo="Preparar entrega de calidad",
            descripcion="Consolidar informe técnico en PDF",
            prioridad="ALTA",
        )
        self.assertEqual(tarea.id_tarea, 1)
        self.assertEqual(tarea.titulo, "Preparar entrega de calidad")
        self.assertEqual(tarea.prioridad, Prioridad.ALTA)
        self.assertEqual(tarea.estado, EstadoTarea.PENDIENTE)

    def test_cp02_transicion_completa_estados_pendiente_a_en_progreso_a_completada(self) -> None:
        """CP-02: Validar el ciclo de vida completo PENDIENTE -> EN_PROGRESO -> COMPLETADA."""
        tarea = self.gestor.crear_tarea("Implementar pruebas unitarias")
        self.gestor.cambiar_estado_tarea(tarea.id_tarea, EstadoTarea.EN_PROGRESO)
        self.assertEqual(tarea.estado, EstadoTarea.EN_PROGRESO)

        self.gestor.cambiar_estado_tarea(tarea.id_tarea, EstadoTarea.COMPLETADA)
        self.assertEqual(tarea.estado, EstadoTarea.COMPLETADA)

    def test_cp03_filtrar_tareas_por_estado_y_prioridad(self) -> None:
        """CP-03: Filtrar tareas combinando criterios de estado y nivel de prioridad."""
        t1 = self.gestor.crear_tarea("Tarea crítica 1", prioridad="ALTA")
        t2 = self.gestor.crear_tarea("Tarea crítica 2", prioridad="ALTA")
        self.gestor.crear_tarea("Tarea rutinaria", prioridad="BAJA")

        self.gestor.cambiar_estado_tarea(t2.id_tarea, "EN_PROGRESO")

        altas_pendientes = self.gestor.listar_tareas(
            estado="PENDIENTE", prioridad="ALTA"
        )
        self.assertEqual(len(altas_pendientes), 1)
        self.assertEqual(altas_pendientes[0].id_tarea, t1.id_tarea)

    def test_cp04_eliminar_tarea_y_verificar_resumen_metricas(self) -> None:
        """CP-04: Eliminar una tarea existente y comprobar la actualización del resumen."""
        t1 = self.gestor.crear_tarea("Tarea temporal", prioridad="BAJA")
        self.gestor.crear_tarea("Tarea permanente", prioridad="ALTA")

        eliminada = self.gestor.eliminar_tarea(t1.id_tarea)
        self.assertEqual(eliminada.id_tarea, t1.id_tarea)

        resumen = self.gestor.obtener_resumen()
        self.assertEqual(resumen["total"], 1)
        self.assertEqual(resumen["alta_prioridad"], 1)

    def test_cp05_permitir_mismo_titulo_si_tarea_anterior_esta_completada(self) -> None:
        """CP-05: Permitir crear una tarea con igual título cuando la anterior ya fue COMPLETADA."""
        t1 = self.gestor.crear_tarea("Revisión semanal de código")
        self.gestor.cambiar_estado_tarea(t1.id_tarea, "COMPLETADA")

        t2 = self.gestor.crear_tarea("Revisión semanal de código")
        self.assertEqual(t2.id_tarea, 2)
        self.assertEqual(t2.estado, EstadoTarea.PENDIENTE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
