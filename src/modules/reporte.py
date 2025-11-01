import csv
import os
from datetime import datetime

# ---------------------------------------------------------
# REPORTE GENERAL: Muestra resultado global por actividad
# ---------------------------------------------------------
def generar_reporte_general(empleados, actividades, registros, 
                           archivo='src/data/reportes/reporte_general.csv'):
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        datos_reporte = []

        # Recorre todas las actividades y calcula métricas generales
        for actividad in actividades:
            registros_act = [r for r in registros if r.actividad_id == actividad.id_actividad]
            total_registros = len(registros_act)
            asistencias = sum(1 for r in registros_act if r.asistio)

            # Calcula satisfacción solo de quienes asistieron y calificaron
            calificaciones = [r.calificacion for r in registros_act if r.asistio and r.calificacion > 0]
            satisfaccion_promedio = round(sum(calificaciones) / len(calificaciones), 2) if calificaciones else 0

            # % de participación
            tasa_participacion = round((asistencias / total_registros * 100), 2) if total_registros > 0 else 0

            # Datos del reporte por actividad
            datos_reporte.append([
                actividad.id_actividad,
                actividad.nombre,
                actividad.fecha,
                actividad.tipo,
                asistencias,
                total_registros,
                f"{tasa_participacion}%",
                f"{satisfaccion_promedio}/5"
            ])

        # Encabezados del CSV
        columnas = [
            'ID_Actividad','Nombre_Actividad','Fecha','Tipo',
            'Asistencias','Total_Registros','Tasa_Participacion','Satisfaccion_Promedio'
        ]

        # Exporta archivo CSV
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)

        print(f"\n✓ Reporte general generado: {archivo}")
        return True
    except Exception as e:
        print(f"\n✗ Error al generar reporte general: {e}")
        return False


# ---------------------------------------------------------
# REPORTE POR ÁREA: Muestra participación por cada área
# ---------------------------------------------------------
def generar_reporte_por_area(empleados, actividades, registros,
                             archivo='src/data/reportes/reporte_por_area.csv'):
    """
    Organiza los datos por áreas y calcula métricas como:
    empleados activos, participaciones y satisfacción promedio por área.
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        areas_dict = {}

        # Agrupa datos por área
        for empleado in empleados:
            area = empleado.area
            if area not in areas_dict:
                areas_dict[area] = {'empleados': [], 'participaciones': [], 'calificaciones': []}

            areas_dict[area]['empleados'].append(empleado.id_empleado)

            # Registros del empleado
            participaciones_emp = [r for r in registros if r.empleado_id == empleado.id_empleado and r.asistio]
            areas_dict[area]['participaciones'].extend(participaciones_emp)

            # Calificaciones válidas
            calificaciones_emp = [r.calificacion for r in participaciones_emp if r.calificacion > 0]
            areas_dict[area]['calificaciones'].extend(calificaciones_emp)

        # Prepara datos finales del reporte por área
        datos_reporte = []
        for area, datos in areas_dict.items():
            total_empleados = len(datos['empleados'])
            total_participaciones = len(datos['participaciones'])
            empleados_activos = len(set(p.empleado_id for p in datos['participaciones']))  # Empleados que sí participaron
            satisfaccion = round(sum(datos['calificaciones']) / len(datos['calificaciones']), 2) if datos['calificaciones'] else 0
            promedio_participaciones = round(total_participaciones / total_empleados, 2) if total_empleados > 0 else 0

            datos_reporte.append([
                area, total_empleados, empleados_activos, total_participaciones,
                promedio_participaciones, f"{satisfaccion}/5"
            ])

        # Ordena áreas de mayor a menor participación
        datos_reporte.sort(key=lambda x: x[3], reverse=True)

        columnas = [
            'Area','Total_Empleados','Empleados_Activos',
            'Total_Participaciones','Promedio_Por_Empleado','Satisfaccion_Promedio'
        ]

        # Exporta a CSV
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)

        print(f"\n✓ Reporte por área generado: {archivo}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al generar reporte por área: {e}")
        return False


# ---------------------------------------------------------
# REPORTE DETALLADO: Cada registro individual
# ---------------------------------------------------------
def generar_reporte_detallado(empleados, actividades, registros,
                              archivo='src/data/reportes/reporte_detallado.csv'):
    """
    Crea un reporte donde se muestra cada participación con:
    empleado, actividad, estado y calificación.
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)

        # Diccionarios para acceder rápido por ID
        empleados_dict = {emp.id_empleado: emp for emp in empleados}
        actividades_dict = {act.id_actividad: act for act in actividades}

        datos_reporte = []

        # Crea un registro detallado por cada asistencia
        for registro in registros:
            empleado = empleados_dict.get(registro.empleado_id)
            actividad = actividades_dict.get(registro.actividad_id)

            if empleado and actividad:
                estado = "Asistió" if registro.asistio else "No asistió"
                calificacion = f"{registro.calificacion}/5" if registro.asistio else "N/A"

                datos_reporte.append([
                    registro.empleado_id, empleado.nombre, empleado.area, empleado.cargo,
                    registro.actividad_id, actividad.nombre, actividad.fecha, actividad.tipo,
                    estado, calificacion
                ])

        # Ordenado por fecha y luego por nombre
        datos_reporte.sort(key=lambda x: (x[6], x[1]))

        columnas = [
            'ID_Empleado','Nombre','Area','Cargo','ID_Actividad',
            'Actividad','Fecha','Tipo','Asistencia','Calificacion'
        ]

        # Exporta a CSV
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)

        print(f"\n✓ Reporte detallado generado: {archivo}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al generar reporte detallado: {e}")
        return False


# ---------------------------------------------------------
# GENERA TODOS LOS REPORTES
# ---------------------------------------------------------
def generar_todos_los_reportes(empleados, actividades, registros):
    """
    Ejecuta los 3 reportes principales de una sola vez.
    Útil para generar resumen completo rápido.
    """
    print("\n" + "="*60)
    print("  GENERANDO TODOS LOS REPORTES")
    print("="*60)
    
    exito_general = generar_reporte_general(empleados, actividades, registros)
    exito_area = generar_reporte_por_area(empleados, actividades, registros)
    exito_detallado = generar_reporte_detallado(empleados, actividades, registros)
    
    total_exitosos = sum([exito_general, exito_area, exito_detallado])
    print(f"\n✓ Reportes generados: {total_exitosos}/3")


# ---------------------------------------------------------
# EXPORTACIÓN GENÉRICA A CSV PARA FUTUROS REPORTES
# ---------------------------------------------------------
def exportar_csv_generico(datos, columnas, archivo, descripcion="CSV"):
    """
    Función reutilizable para exportar cualquier tipo de reporte a CSV.
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos)

        print(f"✓ {descripcion} exportado: {archivo}")
        return True
    except Exception as e:
        print(f"✗ Error al exportar {descripcion}: {e}")
        return False


# ---------------------------------------------------------
# RESUMEN EJECUTIVO: Vista rápida con indicadores clave
# ---------------------------------------------------------
def generar_resumen_ejecutivo(empleados, actividades, registros,
                              archivo='src/data/reportes/resumen_ejecutivo.csv'):
    """
    Muestra datos clave del programa: asistencia, participación,
    satisfacción y actividad con más participación.
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)

        total_empleados = len(empleados)
        total_actividades = len(actividades)
        total_registros = len(registros)
        total_asistencias = sum(1 for r in registros if r.asistio)

        # Porcentaje de participación
        tasa_participacion = round((total_asistencias / total_registros * 100), 2) if total_registros > 0 else 0

        # Calificación promedio solo de asistentes
        calificaciones = [r.calificacion for r in registros if r.asistio and r.calificacion > 0]
        satisfaccion_global = round(sum(calificaciones) / len(calificaciones), 2) if calificaciones else 0

        empleados_activos = len(set(r.empleado_id for r in registros if r.asistio))

        # Actividad con mayor asistencia
        actividades_participacion = {
            actividad.nombre: sum(1 for r in registros if r.actividad_id == actividad.id_actividad and r.asistio)
            for actividad in actividades
        }
        actividad_top = max(actividades_participacion, key=actividades_participacion.get) if actividades_participacion else "N/A"

        # Datos finales del resumen
        datos_reporte = [
            ['Métrica', 'Valor'],
            ['Fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Total empleados', total_empleados],
            ['Total actividades', total_actividades],
            ['Total registros', total_registros],
            ['Total asistencias', total_asistencias],
            ['Participación global', f"{tasa_participacion}%"],
            ['Satisfacción global', f"{satisfaccion_global}/5"],
            ['Empleados activos', empleados_activos],
            ['% Activos', f"{round((empleados_activos / total_empleados * 100), 2)}%" if total_empleados else "0%"],
            ['Actividad destacada', actividad_top]
        ]

        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos_reporte)

        print(f"\n✓ Resumen ejecutivo generado: {archivo}")
        return True
    except Exception as e:
        print(f"\n✗ Error al generar resumen ejecutivo: {e}")
        return False


# ---------------------------------------------------------
# BLOQUE PARA PRUEBAS DIRECTAS DEL MÓDULO
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO REPORTE ===")
    print("Ejecutar desde main.py con datos reales para pruebas completas.")
