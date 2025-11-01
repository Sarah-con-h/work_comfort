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
def generar_reporte_por_area(empleados, actividades, registros,
                             archivo='src/data/reportes/reporte_por_area.csv'):
    """
    Genera un reporte de participación agrupado por área
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        areas_dict = {}
        
        for empleado in empleados:
            area = empleado.area
            if area not in areas_dict:
                areas_dict[area] = {'empleados': [], 'participaciones': [], 'calificaciones': []}
            
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
        return True
        
    except Exception as e:
        print(f"\n✗ Error al generar reporte por área: {e}")
        return False


def generar_reporte_detallado(empleados, actividades, registros,
                              archivo='src/data/reportes/reporte_detallado.csv'):
    """
    Genera un reporte detallado con cada participación individual
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        empleados_dict = {emp.id_empleado: emp for emp in empleados}
        actividades_dict = {act.id_actividad: act for act in actividades}
        
        datos_reporte = []
        for registro in registros:
            empleado = empleados_dict.get(registro.empleado_id)
            actividad = actividades_dict.get(registro.actividad_id)
            
            if empleado and actividad:
                estado = "Asistió" if registro.asistio else "No asistió"
                calificacion = f"{registro.calificacion}/5" if registro.asistio else "N/A"
                datos_reporte.append([
                    registro.empleado_id,
                    empleado.nombre,
                    empleado.area,
                    empleado.cargo,
                    registro.actividad_id,
                    actividad.nombre,
                    actividad.fecha,
                    actividad.tipo,
                    estado,
                    calificacion
                ])
        
        datos_reporte.sort(key=lambda x: (x[6], x[1]))
        
        columnas = [
            'ID_Empleado',
            'Nombre_Empleado',
            'Area',
            'Cargo',
            'ID_Actividad',
            'Nombre_Actividad',
            'Fecha_Actividad',
            'Tipo_Actividad',
            'Estado_Asistencia',
            'Calificacion'
        ]
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columnas)
            writer.writerows(datos_reporte)
        
        print(f"\n✓ Reporte detallado generado exitosamente: {archivo}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al generar reporte detallado: {e}")
        return False
 # ===============================
# FUNCIONES DE REPORTES GENERALES
# ===============================

def generar_todos_los_reportes(empleados, actividades, registros):
    """
    Genera todos los reportes disponibles: general, por área y detallado.
    Sirve para obtener un resumen completo en un solo llamado.
    """
    print("\n" + "="*60)
    print("  GENERANDO TODOS LOS REPORTES")
    print("="*60)
    
    exito_general = generar_reporte_general(empleados, actividades, registros)
    exito_area = generar_reporte_por_area(empleados, actividades, registros)
    exito_detallado = generar_reporte_detallado(empleados, actividades, registros)
    
    print("\n" + "="*60)
    total_exitosos = sum([exito_general, exito_area, exito_detallado])
    print(f"  Reportes generados exitosamente: {total_exitosos}/3")
    print("="*60)


def exportar_csv_generico(datos, columnas, archivo, descripcion="CSV"):
    """
    Función genérica para exportar cualquier conjunto de datos a CSV.
    Reutilizable para reportes nuevos.
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


def generar_resumen_ejecutivo(empleados, actividades, registros,
                              archivo='src/data/reportes/resumen_ejecutivo.csv'):
    """
    Genera un resumen ejecutivo con métricas clave del programa:
    - Total empleados, actividades y registros
    - Total asistencias y tasa de participación global
    - Satisfacción promedio
    - Empleados activos y porcentaje
    - Actividad con mayor participación
    """
    try:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        total_empleados = len(empleados)
        total_actividades = len(actividades)
        total_registros = len(registros)
        total_asistencias = sum(1 for r in registros if r.asistio)
        tasa_participacion = round((total_asistencias / total_registros * 100), 2) if total_registros > 0 else 0
        calificaciones = [r.calificacion for r in registros if r.asistio and r.calificacion > 0]
        satisfaccion_global = round(sum(calificaciones) / len(calificaciones), 2) if calificaciones else 0
        empleados_activos = len(set(r.empleado_id for r in registros if r.asistio))
        
        # Actividad con mayor participación
        actividades_participacion = {actividad.nombre:
                                     sum(1 for r in registros if r.actividad_id == actividad.id_actividad and r.asistio)
                                     for actividad in actividades}
        actividad_top = max(actividades_participacion, key=actividades_participacion.get) if actividades_participacion else "N/A"
        
        # Preparar datos del reporte
        datos_reporte = [
            ['Métrica', 'Valor'],
            ['Fecha del reporte', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Total de empleados', total_empleados],
            ['Total de actividades realizadas', total_actividades],
            ['Total de registros', total_registros],
            ['Total de asistencias', total_asistencias],
            ['Tasa de participación global', f"{tasa_participacion}%"],
            ['Satisfacción promedio global', f"{satisfaccion_global}/5"],
            ['Empleados activos', empleados_activos],
            ['Porcentaje de empleados activos', f"{round((empleados_activos / total_empleados * 100), 2)}%" if total_empleados > 0 else "0%"],
            ['Actividad con mayor participación', actividad_top]
        ]
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(datos_reporte)
        
        print(f"\n✓ Resumen ejecutivo generado: {archivo}")
        return True
    except Exception as e:
        print(f"\n✗ Error al generar resumen ejecutivo: {e}")
        return False


# ===============================
# BLOQUE DE PRUEBA DEL MÓDULO
# ===============================

# Este bloque solo se ejecuta si se corre directamente este archivo.
# Para pruebas completas, se recomienda ejecutar desde main.py con datos cargados.
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO REPORTE ===\n")
    print("Este módulo debe ejecutarse desde main.py con datos cargados.")
    print("Para pruebas completas, ejecute: python src/main.py")
