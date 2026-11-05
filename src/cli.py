"""
Interfaz de Línea de Comandos (CLI) para el Sistema de Agenda de Tareas.

Permite ejecutar la aplicación de forma interactiva o mediante el modo
demostración (`python3 -m src.cli --demo`) para evidenciar todos los flujos.
"""

import sys
from typing import List

from src.excepciones import ErrorAgendaTareas
from src.gestor_tareas import GestorTareas
from src.modelos import Tarea


def formatear_tabla_tareas(tareas: List[Tarea]) -> str:
    """Genera una representación tabular legible de una lista de tareas."""
    if not tareas:
        return "  (No hay tareas que coincidan con el criterio)"

    encabezado = (
        f"{'ID':<4} | {'PRIORIDAD':<10} | {'ESTADO':<13} | {'TÍTULO':<35} | {'DESCRIPCIÓN'}"
    )
    separador = "-" * 90
    filas = [encabezado, separador]
    for t in tareas:
        filas.append(
            f"#{t.id_tarea:<3} | {t.prioridad.value:<10} | {t.estado.value:<13} | "
            f"{t.titulo:<35} | {t.descripcion}"
        )
    return "\n".join(filas)


def ejecutar_demostracion() -> None:
    """
    Ejecuta un recorrido automatizado por las funcionalidades principales
    y el control de errores del sistema para validación rápida.
    """
    gestor = GestorTareas()
    print("=" * 90)
    print(" DEMOSTRACIÓN DEL SISTEMA: AGENDA DE TAREAS CON CONTROL DE ESTADOS Y PRIORIDADES")
    print("=" * 90)

    print("\n1. Creando tareas iniciales...")
    gestor.crear_tarea(
        "Diseñar matriz de pruebas",
        "Incluir casos válidos, inválidos y casos borde",
        "ALTA",
    )
    gestor.crear_tarea(
        "Implementar validadores DRY",
        "Centralizar validaciones en src/validadores.py",
        "ALTA",
    )
    gestor.crear_tarea(
        "Redactar reflexión ética",
        "Analizar impacto de calidad en banca y salud",
        "MEDIA",
    )
    print(formatear_tabla_tareas(gestor.listar_tareas()))

    print("\n2. Actualizando estados de las tareas #1 y #2...")
    gestor.cambiar_estado_tarea(1, "EN_PROGRESO")
    gestor.cambiar_estado_tarea(2, "COMPLETADA")
    print(formatear_tabla_tareas(gestor.listar_tareas()))

    print("\n3. Probando control de errores ante operaciones inválidas:")
    try:
        gestor.crear_tarea("AB", "Título demasiado corto (< 3 caracteres)", "BAJA")
    except ErrorAgendaTareas as error:
        print(f"   [Bloqueado correctamente] -> {error}")

    try:
        gestor.cambiar_estado_tarea(2, "PENDIENTE")
    except ErrorAgendaTareas as error:
        print(f"   [Bloqueado correctamente] -> {error}")

    try:
        gestor.obtener_tarea(999)
    except ErrorAgendaTareas as error:
        print(f"   [Bloqueado correctamente] -> {error}")

    print("\n4. Resumen de métricas de la agenda:")
    resumen = gestor.obtener_resumen()
    print(
        f"   Total: {resumen['total']} | Pendientes: {resumen['pendientes']} | "
        f"En progreso: {resumen['en_progreso']} | Completadas: {resumen['completadas']} | "
        f"Prioridad Alta: {resumen['alta_prioridad']}"
    )
    print("=" * 90)


def menu_interactivo() -> None:
    """Bucle principal del menú interactivo en consola."""
    gestor = GestorTareas()
    opciones = """
--- AGENDA DE TAREAS (MÓDULO 1 - CALIDAD DE SOFTWARE) ---
1. Crear nueva tarea
2. Listar todas las tareas
3. Filtrar tareas por estado
4. Cambiar estado de una tarea
5. Actualizar prioridad de una tarea
6. Eliminar una tarea
7. Ver resumen de métricas
0. Salir
"""
    while True:
        print(opciones)
        seleccion = input("Seleccione una opción: ").strip()

        try:
            if seleccion == "1":
                titulo = input("Título (3-100 caracteres): ")
                descripcion = input("Descripción (opcional): ")
                prioridad = input("Prioridad (BAJA/MEDIA/ALTA) [MEDIA]: ").strip() or "MEDIA"
                tarea = gestor.crear_tarea(titulo, descripcion, prioridad)
                print(f"Tarea creada exitosamente con ID #{tarea.id_tarea}.")
            elif seleccion == "2":
                print(formatear_tabla_tareas(gestor.listar_tareas()))
            elif seleccion == "3":
                estado = input("Estado a filtrar (PENDIENTE/EN_PROGRESO/COMPLETADA): ")
                print(formatear_tabla_tareas(gestor.listar_tareas(estado=estado)))
            elif seleccion == "4":
                id_tarea = int(input("ID de la tarea: "))
                nuevo_estado = input("Nuevo estado (PENDIENTE/EN_PROGRESO/COMPLETADA): ")
                tarea = gestor.cambiar_estado_tarea(id_tarea, nuevo_estado)
                print(f"Estado actualizado a {tarea.estado.value}.")
            elif seleccion == "5":
                id_tarea = int(input("ID de la tarea: "))
                prioridad = input("Nueva prioridad (BAJA/MEDIA/ALTA): ")
                tarea = gestor.actualizar_prioridad_tarea(id_tarea, prioridad)
                print(f"Prioridad actualizada a {tarea.prioridad.value}.")
            elif seleccion == "6":
                id_tarea = int(input("ID de la tarea a eliminar: "))
                eliminada = gestor.eliminar_tarea(id_tarea)
                print(f"Tarea #{eliminada.id_tarea} ('{eliminada.titulo}') eliminada.")
            elif seleccion == "7":
                resumen = gestor.obtener_resumen()
                print(f"Resumen actual: {resumen}")
            elif seleccion == "0":
                print("Saliendo de la Agenda de Tareas...")
                break
            else:
                print("Opción no reconocida. Intente nuevamente.")
        except ValueError:
            print("[Error de entrada]: El ID debe ser un número entero válido.")
        except ErrorAgendaTareas as error:
            print(f"[Error de validación/negocio]: {error}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        ejecutar_demostracion()
    else:
        menu_interactivo()
