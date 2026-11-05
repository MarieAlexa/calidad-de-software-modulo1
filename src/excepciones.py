"""
Excepciones personalizadas del dominio para la Agenda de Tareas.

Centraliza los errores de negocio para mantener un control de errores
semántico, limpio y consistente en todas las capas de la aplicación.
"""


class ErrorAgendaTareas(Exception):
    """Excepción base para todos los errores de negocio de la agenda."""


class ErrorValidacionTarea(ErrorAgendaTareas):
    """Se lanza cuando los datos de entrada de una tarea no cumplen las reglas de validación."""


class TareaNoEncontradaError(ErrorAgendaTareas):
    """Se lanza cuando se intenta operar sobre un identificador de tarea inexistente."""


class TransicionEstadoInvalidaError(ErrorAgendaTareas):
    """Se lanza cuando se intenta cambiar el estado de una tarea violando el flujo permitido."""
