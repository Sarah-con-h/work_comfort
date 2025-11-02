# Sistema de Gestión de Work_Comfort

Sistema en Python para registrar y analizar actividades de bienestar laboral, generando reportes automáticos en CSV.

---

## Información del Proyecto

- **Categoría:** Procesos de Apoyo
- **Versión Python:** 3.13.9
- **Equipo:** Sarah Castri, Beicker Torres, Mariana Valderrama y Daniel Luque
- **Fecha:** Noviembre 2025

---

## ¿Por qué seleccionamos esta solución?

### Contexto del Problema

En las organizaciones modernas, el bienestar laboral es fundamental para mantener empleados motivados y productivos. Las empresas realizan diversas actividades como pausas activas, talleres de manejo de estrés, jornadas deportivas y capacitaciones de salud mental.

### Problema Identificado

Sin embargo, identificamos varios problemas en la gestión de estos programas:

-  **Falta de registro organizado:** Las actividades se realizan pero no se documenta quién participó
-  **Sin medición de impacto:** No se sabe si las actividades son efectivas
-  **Datos dispersos:** Información en hojas de papel, Excel separados, sin consolidar
-  **Imposibilidad de análisis:** No hay forma de identificar tendencias o áreas con baja participación
-  **Dificultad para tomar decisiones:** ¿Qué actividades invertir más? ¿Qué áreas necesitan más atención?

### ¿Por qué es importante sistematizar esto?

1. **Mejora la gestión de recursos:** Saber qué actividades tienen mejor aceptación permite optimizar el presupuesto
2. **Identifica necesidades:** Detectar áreas o empleados con baja participación
3. **Mide el impacto real:** Cuantificar la satisfacción con las actividades
4. **Facilita reportes:** Generar informes automáticos para recursos humanos o gerencia
5. **Cumplimiento normativo:** Documentar las actividades de salud ocupacional requeridas por ley

### ¿Por qué Python?

Seleccionamos Python para esta solución porque:

-  **Simplicidad:** Sintaxis clara, ideal para procesar datos
-  **Biblioteca CSV nativa:** No necesitamos pandas, usamos el módulo csv estándar
-  **Fácil de mantener:** Código legible que cualquier persona puede entender
-  **Multiplataforma:** Funciona en Windows, Mac y Linux
-  **Ideal para automatización:** Perfecta para generar reportes automáticos

### Beneficios de nuestra solución

**Para Recursos Humanos:**
- Reportes automáticos de participación
- Identificación de empleados menos participativos
- Datos para presentar a gerencia

**Para la Gerencia:**
- Métricas claras del programa de bienestar
- ROI (retorno de inversión) en actividades
- Toma de decisiones basada en datos

**Para los Empleados:**
- Registro de su participación
- Transparencia en las actividades disponibles
- Reconocimiento de su compromiso

---

## Estructura del Proyecto

```
Work_Comfort/
├── src/
│   ├── main.py                    # Programa principal con menú
│   ├── modules/
│   │   ├── __init__.py           # Inicializa el paquete
│   │   ├── empleado.py           # Gestión de empleados
│   │   ├── actividad.py          # Gestión de actividades
│   │   ├── registro.py           # Registros y estadísticas
│   │   └── reporte.py            # Generación de CSV
│   └── data/
│       ├── empleados.txt         # Base de datos de empleados
│       ├── actividades.txt       # Base de datos de actividades
│       ├── participacion.txt     # Base de datos de registros
│       └── reportes/             # Carpeta para CSVs generados
├── tests/
│   └── test_basico.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalación

### Requisitos previos

- **Python 3.8 o superior**
- **Git** (opcional)
- **Terminal/CMD**

### Verificar Python

```bash
python --version
# Debe mostrar: Python 3.8.x o superior
```

### Paso 1: Obtener el código

**Opción A: Clonar con Git**
```bash
git clone https://github.com/TU-USUARIO/Work_Comfort.git
cd bienestar-laboral
```

### Paso 2: Ejecutar el programa

```bash
python src/main.py
```

### Primera ejecución

Al ejecutar por primera vez, el sistema preguntará si deseas cargar **datos de prueba**. Escribe `s` para cargar:
- 5 empleados de ejemplo
- 3 actividades de ejemplo
- 12 registros de participación

---

## Manual de Usuario

### Menú Principal

```
┌─────────────────────────────────────────────────────────────────────┐
│                           MENÚ PRINCIPAL                            │
├─────────────────────────────────────────────────────────────────────┤
│  1. Registrar empleado                                              │
│  2. Registrar actividad de bienestar                                │
│  3. Registrar participación en actividad                            │
├─────────────────────────────────────────────────────────────────────┤
│  4. Ver lista de empleados                                          │
│  5. Ver lista de actividades                                        │
│  6. Ver estadísticas de participación                               │
├─────────────────────────────────────────────────────────────────────┤
│  7. Generar reporte general (CSV)                                   │
│  8. Generar reporte por área (CSV)                                  │
│  9. Generar reporte detallado (CSV)                                 │
│ 10. Generar todos los reportes (CSV)                                │
│ 11. Generar resumen ejecutivo (CSV)                                 │
├─────────────────────────────────────────────────────────────────────┤
│  0. Salir del sistema                                               │
└─────────────────────────────────────────────────────────────────────┘
```

###  Registrar Empleado

Permite registrar a los empleados de la organización.

• Ejemplo: ID=1 — Daniel Luque(Tecnología) — Desarrollador Senior

• Validaciones: 

 ID único (int)


 Nombre ≥ 3 caracteres


 Área obligatoria

---

###  Registrar Actividad

Registra actividades de bienestar (pausas activas, talleres, jornadas).

• Ejemplo: ID=1 — Pausa activa matutina — Fecha: 2025-11-05 — Tipo: Pausa activa

• Validaciones:  ID único, Fecha formato YYYY‑MM‑DD,  Nombre ≥ 3 caracteres

---

###  Registrar Participación

Registra asistencia y calificación de satisfacción.

• Ejemplo: Empleado=1, Actividad=1, Asistió: s, Calificación: 5

• Validaciones: 
Empleado y actividad existen

Calificación 1–5 (si asistió)


Sin duplicados

---

###  Ver Lista de Empleados

Muestra todos los empleados registrados con su cargo y área, y el total.

---

###  Ver Lista de Actividades

Listado de actividades con fecha, tipo y una breve descripción.

---

###  Ver Estadísticas

Métricas clave: total registros, asistencias, ausencias, tasa de participación (%) y satisfacción promedio (1–5).

---

### Generar reportes CSV

Exporta datos para análisis en Excel (ruta: `src/data/reportes/`).

-  Reporte general: resumen por actividad (asistencias, tasa, satisfacción).
-  Reporte por área: métricas agrupadas por departamento.
-  Reporte detallado: cada participación individual.
-  Generar todos los reportes a la vez.
-  Resumen ejecutivo: métricas clave en formato ejecutivo.

---




