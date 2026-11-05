# Agenda de Tareas con Control de Estados y Prioridades

**Asignatura:** Calidad de Software — Módulo 1  
**Equipo de Desarrollo:**
- **Manuel Matute** (`manuel.matute@uip.edu.pa`) — Arquitectura de dominio, validadores DRY y lógica CRUD (`feature/core-logic`).
- **Alexandra Rangel** — Diseño y ejecución de pruebas unitarias/funcionales y validación de calidad (`feature/unit-tests`).

---

## 1. Arquitectura y Principios de Calidad Aplicados

Prototipo desarrollado en **Python 3** aplicando principios de **Clean Code**, **DRY (*Don't Repeat Yourself*)**, tipado estático y manejo defensivo de excepciones:

```text
calidad-de-software-modulo1/
├── README.md                       # Documentación técnica y especificación de casos de prueba
├── src/
│   ├── __init__.py
│   ├── excepciones.py              # Jerarquía de excepciones de dominio personalizadas
│   ├── validadores.py              # Funciones de validación centralizadas (Principio DRY)
│   ├── modelos.py                  # Entidad Tarea, Enums y reglas de transición de estados
│   ├── gestor_tareas.py            # Lógica de negocio CRUD, filtros y resumen estadístico
│   └── cli.py                      # Interfaz de consola interactiva y modo demostración
└── tests/
    ├── __init__.py
    └── test_gestor_tareas.py       # Suite de 15 pruebas unitarias y funcionales (CP-01 a CP-15)
```

---

## 2. Ejecución del Sistema y Pruebas

Requiere **Python 3.10+** (únicamente biblioteca estándar, sin dependencias externas).

```bash
# Ejecutar recorrido de demostración automatizada
python3 -m src.cli --demo

# Ejecutar menú interactivo en consola
python3 -m src.cli

# Ejecutar suite completa de pruebas unitarias
python3 -m unittest discover -s tests -v
```

---

## 3. Especificación de Casos de Prueba (`tests/test_gestor_tareas.py`)

La suite de pruebas está dividida en tres bloques para cubrir flujos nominales, entradas inválidas y valores límite (*boundary values*):

| ID | Categoría | Caso de Prueba | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **CP-01** | Flujo Correcto | Crear tarea válida con datos completos | Se asigna `id_tarea=1`, `prioridad=ALTA` y `estado=PENDIENTE` |
| **CP-02** | Flujo Correcto | Ciclo completo `PENDIENTE` → `EN_PROGRESO` → `COMPLETADA` | Transiciones exitosas en cada etapa |
| **CP-03** | Flujo Correcto | Filtrar tareas por combinación de estado y prioridad | Retorna únicamente las tareas que cumplen ambos criterios |
| **CP-04** | Flujo Correcto | Eliminar tarea existente y consultar métricas | Se elimina el registro y `obtener_resumen()` actualiza los totales |
| **CP-05** | Flujo Correcto | Reutilizar título de una tarea previamente `COMPLETADA` | Permite crear la nueva tarea activa con nuevo ID |
| **CP-06** | Entrada Inválida | Título vacío o compuesto solo por espacios (`"     "`) | Lanza `ErrorValidacionTarea` |
| **CP-07** | Entrada Inválida | Prioridad no existente (`"CRITICA_EXTREMA"`) | Lanza `ErrorValidacionTarea` |
| **CP-08** | Entrada Inválida | Crear tarea activa con título duplicado (*case-insensitive*) | Lanza `ErrorValidacionTarea` |
| **CP-09** | Entrada Inválida | Modificar estado o prioridad de una tarea ya `COMPLETADA` | Lanza `TransicionEstadoInvalidaError` |
| **CP-10** | Entrada Inválida | Consultar ID inexistente (`999`), negativo (`-5`) o booleano (`True`) | Lanza `TareaNoEncontradaError` / `ErrorValidacionTarea` |
| **CP-11** | Caso Borde | Límite inferior de longitud de título (2 vs 3 caracteres) | 2 caracteres falla; 3 caracteres aprueba |
| **CP-12** | Caso Borde | Límite superior de longitud de título (100 vs 101 caracteres) | 100 caracteres aprueba; 101 caracteres falla |
| **CP-13** | Caso Borde | Límite superior de descripción (300 vs 301 caracteres) | 300 caracteres aprueba; 301 caracteres falla |
| **CP-14** | Caso Borde | Listar y obtener resumen con la agenda vacía | Retorna `[]` y contadores en `0` |
| **CP-15** | Caso Borde | Entradas con espacios laterales y minúsculas (`"  alta  "`) | Recorta espacios y normaliza al enumerado correspondiente |
