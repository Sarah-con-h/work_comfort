"""
Módulo para gestionar registros de participación
Responsable: Persona 3
"""

import os

class Registro:
    """Clase que representa la participación de un empleado en una actividad"""
    
    def __init__(self, empleado_id, actividad_id, asistio, calificacion=0):
        """
        Constructor de la clase Registro
        
        Args:
            empleado_id (int): ID del empleado
            actividad_id (int): ID de la actividad
            asistio (bool): True si asistió, False si no
            calificacion (int): Calificación de satisfacción (1-5, 0 si no asistió)
        """
        self.empleado_id = empleado_id
        self.actividad_id = actividad_id
        self.asistio = asistio
        self.calificacion = calificacion if asistio else 0
    
    def to_string(self):
        """Convierte el registro a formato de texto para guardar"""
        return f"{self.empleado_id}|{self.actividad_id}|{self.asistio}|{self.calificacion}"
    
    @staticmethod
    def from_string(linea):
        """
        Crea un objeto Registro desde una línea de texto
        
        Args:
            linea (str): Línea con formato: empleado_id|actividad_id|asistio|calificacion
            
        Returns:
            Registro: Objeto registro creado
        """
        try:
            partes = linea.strip().split('|')
            if len(partes) != 4:
                raise ValueError("Formato inválido de registro")
            
            empleado_id = int(partes[0])
            actividad_id = int(partes[1])
            asistio = partes[2].lower() == 'true'
            calificacion = int(partes[3])
            
            return Registro(empleado_id, actividad_id, asistio, calificacion)
        except Exception as e:
            print(f"Error al leer registro: {e}")
            return None
    
    def __str__(self):
        """Representación en string del registro"""
        estado = "Asistió" if self.asistio else "No asistió"
        calif = f"Satisfacción: {self.calificacion}/5" if self.asistio else ""
        return f"Empleado {self.empleado_id} - Actividad {self.actividad_id}: {estado} {calif}"


def registrar_participacion(registro, archivo='src/data/participacion.txt'):
    """
    Registra la participación de un empleado en una actividad
    
    Args:
        registro (Registro): Objeto registro a guardar
        archivo (str): Ruta del archivo de participación
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        # Validar si ya existe un registro para este empleado y actividad
        registros = cargar_registros(archivo)
        existe = any(r.empleado_id == registro.empleado_id and 
                    r.actividad_id == registro.actividad_id 
                    for r in registros)
        
        if existe:
            print(f"⚠ Ya existe un registro para el empleado {registro.empleado_id} en la actividad {registro.actividad_id}")
            respuesta = input("¿Desea sobrescribirlo? (s/n): ")
            if respuesta.lower() != 's':
                print("✗ Registro cancelado")
                return
            # Eliminar el registro existente
            registros = [r for r in registros if not (r.empleado_id == registro.empleado_id and 
                                                      r.actividad_id == registro.actividad_id)]
            # Reescribir archivo
            with open(archivo, 'w', encoding='utf-8') as f:
                for r in registros:
                    f.write(r.to_string() + '\n')
        
        # Agregar nuevo registro
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(registro.to_string() + '\n')
        print(f"✓ Participación registrada exitosamente")
        
    except Exception as e:
        print(f"✗ Error al guardar participación: {e}")


def cargar_registros(archivo='src/data/participacion.txt'):
    """
    Carga todos los registros desde el archivo
    
    Args:
        archivo (str): Ruta del archivo de participación
        
    Returns:
        list: Lista de objetos Registro
    """
    registros = []
    try:
        if not os.path.exists(archivo):
            print(f"⚠ El archivo {archivo} no existe. Se creará al agregar registros.")
            return registros
        
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                if linea.strip():  # Ignorar líneas vacías
                    reg = Registro.from_string(linea)
                    if reg:
                        registros.append(reg)
    except Exception as e:
        print(f"✗ Error al cargar registros: {e}")
    
    return registros


def calcular_estadisticas(registros=None, actividad_id=None):
    """
    Calcula estadísticas de participación y satisfacción
    
    Args:
        registros (list): Lista de registros (si es None, los carga del archivo)
        actividad_id (int): ID de actividad específica (None para todas)
        
    Returns:
        dict: Diccionario con estadísticas calculadas
    """
    if registros is None:
        registros = cargar_registros()
    
    # Filtrar por actividad si se especifica
    if actividad_id is not None:
        registros = [r for r in registros if r.actividad_id == actividad_id]
    
    if not registros:
        return {
            'total_registros': 0,
            'asistencias': 0,
            'ausencias': 0,
            'tasa_participacion': 0.0,
            'satisfaccion_promedio': 0.0,
            'calificaciones': []
        }
    
    # Calcular métricas
    asistencias = sum(1 for r in registros if r.asistio)
    ausencias = len(registros) - asistencias
    tasa_participacion = (asistencias / len(registros)) * 100 if registros else 0
    
    # Calificaciones de quienes asistieron
    calificaciones = [r.calificacion for r in registros if r.asistio and r.calificacion > 0]
    satisfaccion_promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    
    return {
        'total_registros': len(registros),
        'asistencias': asistencias,
        'ausencias': ausencias,
        'tasa_participacion': round(tasa_participacion, 2),
        'satisfaccion_promedio': round(satisfaccion_promedio, 2),
        'calificaciones': calificaciones
    }

def obtener_participantes_actividad(actividad_id, registros=None):
    """
    Obtiene los IDs de empleados que participaron en una actividad
    
    Args:
        actividad_id (int): ID de la actividad
        registros (list): Lista de registros (opcional)
        
    Returns:
        list: Lista de IDs de empleados que asistieron
    """
    if registros is None:
        registros = cargar_registros()
    
    participantes = [r.empleado_id for r in registros 
                    if r.actividad_id == actividad_id and r.asistio]
    
    return participantes


def obtener_actividades_empleado(empleado_id, registros=None):
    """
    Obtiene las actividades en las que participó un empleado
    
    Args:
        empleado_id (int): ID del empleado
        registros (list): Lista de registros (opcional)
        
    Returns:
        list: Lista de IDs de actividades donde asistió
    """
    if registros is None:
        registros = cargar_registros()
    
    actividades = [r.actividad_id for r in registros 
                  if r.empleado_id == empleado_id and r.asistio]
    
    return actividades


def mostrar_estadisticas_generales():
    """Muestra estadísticas generales en consola"""
    registros = cargar_registros()
    
    if not registros:
        print("\n⚠ No hay registros de participación")
        return
    
    stats = calcular_estadisticas(registros)
    
    print("\n" + "="*60)
    print("  ESTADÍSTICAS GENERALES DE PARTICIPACIÓN")
    print("="*60)
    print(f"Total de registros:        {stats['total_registros']}")
    print(f"Asistencias:               {stats['asistencias']}")
    print(f"Ausencias:                 {stats['ausencias']}")
    print(f"Tasa de participación:     {stats['tasa_participacion']}%")
    print(f"Satisfacción promedio:     {stats['satisfaccion_promedio']}/5")
    print("="*60)


def registrar_participacion_interactiva():
    """Función interactiva para registrar participación desde consola"""
    print("\n" + "="*60)
    print("  REGISTRO DE PARTICIPACIÓN")
    print("="*60)
    
    try:
        # Solicitar ID del empleado
        while True:
            emp_id = input("ID del empleado: ").strip()
            if not emp_id.isdigit():
                print("✗ El ID debe ser un número entero")
                continue
            emp_id = int(emp_id)
            break
        
        # Solicitar ID de la actividad
        while True:
            act_id = input("ID de la actividad: ").strip()
            if not act_id.isdigit():
                print("✗ El ID debe ser un número entero")
                continue
            act_id = int(act_id)
            break
        
        # Preguntar si asistió
        while True:
            asistio_input = input("¿El empleado asistió? (s/n): ").strip().lower()
            if asistio_input in ['s', 'n']:
                asistio = asistio_input == 's'
                break
            print("✗ Responda 's' para sí o 'n' para no")
        
        # Si asistió, solicitar calificación
        calificacion = 0
        if asistio:
            while True:
                calif_input = input("Calificación de satisfacción (1-5): ").strip()
                if calif_input.isdigit() and 1 <= int(calif_input) <= 5:
                    calificacion = int(calif_input)
                    break
                print("✗ La calificación debe ser un número entre 1 y 5")
        
        # Crear y guardar registro
        nuevo_registro = Registro(emp_id, act_id, asistio, calificacion)
        registrar_participacion(nuevo_registro)
        
    except KeyboardInterrupt:
        print("\n\n✗ Registro cancelado por el usuario")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")


# Prueba del módulo (solo se ejecuta si se corre este archivo directamente)
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO REGISTRO ===\n")
    
    # Crear registros de prueba
    reg1 = Registro(1, 1, True, 5)
    reg2 = Registro(1, 2, True, 4)
    reg3 = Registro(2, 1, True, 5)
    reg4 = Registro(3, 1, False, 0)
    reg5 = Registro(2, 2, True, 3)
    
    # Guardar registros
    registrar_participacion(reg1)
    registrar_participacion(reg2)
    registrar_participacion(reg3)
    registrar_participacion(reg4)
    registrar_participacion(reg5)
    
    # Mostrar estadísticas generales
    mostrar_estadisticas_generales()