import csv
import os
from datetime import datetime

def generar_reporte_general(empleados, actividades, registros, 
                           archivo='src/data/reportes/reporte_general.csv'):
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        datos_reporte = []
        for actividad in actividades:
            registros_act = [r for r in registros if r.actividad_id == actividad.id_actividad]
            total_registros = len(registros_act)
            asistencias = sum(1 for r in registros_act if r.asistio)
            calificaciones = [r.calificacion for r in registros_act if r.asistio and r.calificacion > 0]
            satisfaccion_promedio = round(sum(calificaciones) / len(calificaciones), 2) if calificaciones else 0
            tasa_participacion = round((asistencias / total_registros * 100), 2) if total_registros > 0 else 0
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
        columnas = [
            'ID_Actividad',
            'Nombre_Actividad',
            'Fecha',
            'Tipo',
            'Asistencias',
            'Total_Registros',
            'Tasa_Participacion',
            'Satisfaccion_Promedio'
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)
        print(f"\n✓ Reporte general generado exitosamente: {archivo}")
        print(f"  Total de actividades reportadas: {len(datos_reporte)}")
        return True
    except Exception as e:
        print(f"\n✗ Error al generar reporte general: {e}")
        return False


def generar_reporte_por_area(empleados, actividades, registros,
                             archivo='src/data/reportes/reporte_por_area.csv'):
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        areas_dict = {}
        for empleado in empleados:
            area = empleado.area
            if area not in areas_dict:
                areas_dict[area] = {
                    'empleados': [],
                    'participaciones': [],
                    'calificaciones': []
                }
            areas_dict[area]['empleados'].append(empleado.id_empleado)
            participaciones_emp = [r for r in registros if r.empleado_id == empleado.id_empleado and r.asistio]
            areas_dict[area]['participaciones'].extend(participaciones_emp)
            calificaciones_emp = [r.calificacion for r in participaciones_emp if r.calificacion > 0]
            areas_dict[area]['calificaciones'].extend(calificaciones_emp)
        datos_reporte = []
        for area, datos in areas_dict.items():
            total_empleados = len(datos['empleados'])
            total_participaciones = len(datos['participaciones'])
            empleados_activos = len(set(p.empleado_id for p in datos['participaciones']))
            satisfaccion = round(sum(datos['calificaciones']) / len(datos['calificaciones']), 2) if datos['calificaciones'] else 0
            promedio_participaciones = round(total_participaciones / total_empleados, 2) if total_empleados > 0 else 0
            datos_reporte.append([
                area,
                total_empleados,
                empleados_activos,
                total_participaciones,
                promedio_participaciones,
                f"{satisfaccion}/5"
            ])
        datos_reporte.sort(key=lambda x: x[3], reverse=True)
        columnas = [
            'Area',
            'Total_Empleados',
            'Empleados_Activos',
            'Total_Participaciones',
            'Promedio_Participaciones_Por_Empleado',
            'Satisfaccion_Promedio'
        ]
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)
        print(f"\n✓ Reporte por área generado exitosamente: {archivo}")
        print(f"  Total de áreas reportadas: {len(datos_reporte)}")
        return True
    except Exception as e:
        print(f"\n✗ Error al generar reporte por área: {e}")
        return False
