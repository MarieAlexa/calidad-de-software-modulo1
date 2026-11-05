"""
Módulo de validadores reutilizables (Principio DRY - Don't Repeat Yourself).

Concentra las reglas de validación de tipos, textos, rangos y enumeraciones
para evitar duplicación de condicionales en los modelos y servicios.
"""

from enum import Enum
from typing import Type, TypeVar
from src.excepciones import ErrorValidacionTarea

T = TypeVar("T", bound=Enum)

LONGITUD_MINIMA_TITULO = 3
LONGITUD_MAXIMA_TITULO = 100
LONGITUD_MAXIMA_DESCRIPCION = 300


def validar_texto_rango(
    valor: str,
    nombre_campo: str,
    min_len: int,
    max_len: int,
    permitir_vacio: bool = False,
) -> str:
    """
    Valida que un valor sea una cadena de texto, elimina espacios extremos
    y comprueba que su longitud se encuentre dentro del rango [min_len, max_len].
    """
    if not isinstance(valor, str):
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' debe ser una cadena de texto."
        )

    texto_limpio = valor.strip()

    if permitir_vacio and len(texto_limpio) == 0:
        return texto_limpio

    if len(texto_limpio) == 0:
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' no puede estar vacío ni contener solo espacios."
        )

    if len(texto_limpio) < min_len:
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' debe tener al menos {min_len} caracteres "
            f"(actual: {len(texto_limpio)})."
        )

    if len(texto_limpio) > max_len:
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' no puede exceder los {max_len} caracteres "
            f"(actual: {len(texto_limpio)})."
        )

    return texto_limpio


def validar_entero_positivo(valor: int, nombre_campo: str) -> int:
    """
    Valida que un valor sea estrictamente un número entero positivo (> 0).
    Nota: En Python bool es subclase de int, por lo que se excluye explícitamente.
    """
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' debe ser un número entero."
        )

    if valor <= 0:
        raise ErrorValidacionTarea(
            f"El campo '{nombre_campo}' debe ser un entero mayor que cero (recibido: {valor})."
        )

    return valor


def validar_instancia_enum(
    valor: T | str, clase_enum: Type[T], nombre_campo: str
) -> T:
    """
    Valida y convierte un valor (instancia de Enum o cadena con su nombre/valor)
    al tipo enumerado esperado.
    """
    if isinstance(valor, clase_enum):
        return valor

    if isinstance(valor, str):
        clave_normalizada = valor.strip().upper()
        for miembro in clase_enum:
            if miembro.name == clave_normalizada or miembro.value == clave_normalizada:
                return miembro

    valores_permitidos = ", ".join(m.value for m in clase_enum)
    raise ErrorValidacionTarea(
        f"Valor inválido '{valor}' para '{nombre_campo}'. "
        f"Valores permitidos: {valores_permitidos}."
    )
