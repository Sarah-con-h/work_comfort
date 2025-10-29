

import os
from datetime import datetime

class Actividad:
    """Clase que representa una actividad de bienestar laboral"""
    
    def _init_(self, id_actividad, nombre, fecha, tipo, descripcion=""):
        """
        Constructor de la clase Actividad
        
        Args:
            id_actividad (int): Identificador único de la actividad
            nombre (str): Nombre de la actividadCrear
            fecha (str): Fecha en formato YYYY-MM-DD
            tipo (str): Tipo de actividad (Pausa activa, Taller, etc.)
            descripcion (str): Descripción opcional de la actividad
        """
        self.id_actividad = id_actividad
        self.nombre = nombre
        self.fecha = fecha
        self.tipo = tipo
        self.descripcion = descripcion
    def to_string(self):
        """Convierte la actividad a formato de texto para guardar"""
        return f"{self.id_actividad}|{self.nombre}|{self.fecha}|{self.tipo}|{self.descripcion}"
    
  
    @staticmethod
    def from_string(linea):
        """
        Crea un objeto Actividad desde una línea de texto
        
        Args:
            linea (str): Línea con formato: id|nombre|fecha|tipo|descripcion
            
        Returns:
            Actividad: Objeto actividad creado
        """
        try:
            partes = linea.strip().split('|')
            if len(partes) < 4:
                raise ValueError("Formato inválido de actividad")
            
            id_act = int(partes[0])
            nombre = partes[1]
            fecha = partes[2]
            tipo = partes[3]
            descripcion = partes[4] if len(partes) > 4 else ""
            
            return Actividad(id_act, nombre, fecha, tipo, descripcion)
        except Exception as e:
            print(f"Error al leer actividad: {e}")
            return None
    
    


def validar_fecha(fecha_str):
    """
    Valida que una fecha tenga formato YYYY-MM-DD
    
    Args:
        fecha_str (str): Fecha a validar
        
    Returns:
        bool: True si la fecha es válida, False en caso contrario
    """
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def agregar_actividad(actividad, archivo='src/data/actividades.txt'):
    """
    Agrega una actividad al archivo de datos
    
    Args:
        actividad (Actividad): Objeto actividad a guardar
        archivo (str): Ruta del archivo de actividades
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        # Agregar al archivo
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(actividad.to_string() + '\n')
        print(f"✓ Actividad '{actividad.nombre}' registrada exitosamente")
    except Exception as e:
        print(f"✗ Error al guardar actividad: {e}")


def cargar_actividades(archivo='src/data/actividades.txt'):
    """
    Carga todas las actividades desde el archivo
    
    Args:
        archivo (str): Ruta del archivo de actividades
        
    Returns:
        list: Lista de objetos Actividad
    """
    actividades = []
    try:
        if not os.path.exists(archivo):
            print(f"⚠ El archivo {archivo} no existe. Se creará al agregar actividades.")
            return actividades
        
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                if linea.strip():  # Ignorar líneas vacías
                    act = Actividad.from_string(linea)
                    if act:
                        actividades.append(act)
    except Exception as e:
        print(f"✗ Error al cargar actividades: {e}")
    
    return actividades


def listar_actividades():
    """Muestra en consola todas las actividades registradas"""
    actividades = cargar_actividades()
    
    if not actividades:
        print("\n⚠ No hay actividades registradas")
        return
    
    print("\n" + "="*70)
    print("  LISTA DE ACTIVIDADES DE BIENESTAR")
    print("="*70)
    for act in actividades:
        print(f"{act}")
        if act.descripcion:
            print(f"    → {act.descripcion}")
    print("="*70)
    print(f"Total de actividades: {len(actividades)}")
  
def obtener_actividad_por_id(id_actividad):
    """
    Busca una actividad por su ID
    
    Args:
        id_actividad (int): ID de la actividad a buscar
        
    Returns:
        Actividad: Objeto actividad encontrado o None
    """
    actividades = cargar_actividades()
    for act in actividades:
        if act.id_actividad == id_actividad:
            return act
    return None


def validar_id_unico(id_actividad):
    """
    Verifica que el ID de la actividad no exista
    
    Args:
        id_actividad (int): ID a verificar
        
    Returns:
        bool: True si el ID es único, False si ya existe
    """
    actividades = cargar_actividades()
    for act in actividades:
        if act.id_actividad == id_actividad:
            return False
    return True
def registrar_actividad_interactiva():
    """Función interactiva para registrar una actividad desde consola"""
    print("\n" + "="*70)
    print("  REGISTRO DE NUEVA ACTIVIDAD DE BIENESTAR")
    print("="*70)
    
    try:
        # Solicitar ID
        while True:
            id_act = input("ID de la actividad: ").strip()
            if not id_act.isdigit():
                print("✗ El ID debe ser un número entero")
                continue
            id_act = int(id_act)
            if not validar_id_unico(id_act):
                print("✗ Este ID ya existe. Ingrese otro.")
                continue
            break
        
        # Solicitar nombre
        while True:
            nombre = input("Nombre de la actividad: ").strip()
            if len(nombre) < 3:
                print("✗ El nombre debe tener al menos 3 caracteres")
                continue
            break
        
        # Solicitar fecha
        while True:
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            if not validar_fecha(fecha):
                print("✗ Formato de fecha inválido. Use YYYY-MM-DD (ej: 2025-10-28)")
                continue
            break
        
        # Solicitar tipo
        print("\nTipos de actividad:")
        tipos = [
            "Pausa activa",
            "Taller",
            "Jornada deportiva",
            "Capacitación",
            "Conferencia",
            "Actividad recreativa",
            "Programa de salud"
        ]
        for i, tipo in enumerate(tipos, 1):
            print(f"  {i}. {tipo}")
        
        while True:
            tipo_op = input("Seleccione el número del tipo (o escriba uno nuevo): ").strip()
            if tipo_op.isdigit() and 1 <= int(tipo_op) <= len(tipos):
                tipo = tipos[int(tipo_op) - 1]
                break
            elif len(tipo_op) > 0:
                tipo = tipo_op
                break
            else:
                print("✗ Debe ingresar un tipo válido")
        
        # Solicitar descripción (opcional)
        descripcion = input("Descripción (opcional, presione Enter para omitir): ").strip()
        
        # Crear y guardar actividad
        nueva_actividad = Actividad(id_act, nombre, fecha, tipo, descripcion)
        agregar_actividad(nueva_actividad)
        
    except KeyboardInterrupt:
        print("\n\n✗ Registro cancelado por el usuario")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")



def obtener_actividades_por_fecha(fecha_inicio, fecha_fin=None):
    """
    Obtiene actividades dentro de un rango de fechas

    Args:
        fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD
        fecha_fin (str): Fecha final en formato YYYY-MM-DD (opcional)

    Returns:
        list: Lista de actividades en el rango
    """
    actividades = cargar_actividades()
    resultado = []

    try:
        fecha_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_f = datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else fecha_ini

        for act in actividades:
            fecha_act = datetime.strptime(act.fecha, '%Y-%m-%d')
            if fecha_ini <= fecha_act <= fecha_f:
                resultado.append(act)
    except ValueError:
        print("✗ Error en el formato de fechas")

    return resultado
   


def obtener_actividades_por_tipo(tipo):
    """
    Obtiene actividades de un tipo específico

    Args:
        tipo (str): Tipo de actividad a buscar

    Returns:
        list: Lista de actividades del tipo especificado
    """
    actividades = cargar_actividades()
    return [act for act in actividades if act.tipo.lower() == tipo.lower()]


# Prueba del módulo (solo se ejecuta si se corre este archivo directamente)
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO ACTIVIDAD ===\n")

    # Crear actividades de prueba
    act1 = Actividad(1, "Pausa activa matutina", "2025-10-15", "Pausa activa",
                     "Ejercicios de estiramiento y relajación")
    act2 = Actividad(2, "Taller de meditación", "2025-10-20", "Taller",
                     "Técnicas de mindfulness para reducir estrés")
    act3 = Actividad(3, "Jornada deportiva", "2025-10-25", "Jornada deportiva",
                     "Torneo de fútbol y voleibol")
    
    


    # Buscar por tipo
    print("\n--- Actividades tipo 'Taller' ---")
    talleres = obtener_actividades_por_tipo("Taller")
    for taller in talleres:
        print(f"  - {taller}")






def validar_id_unico(id_actividad):
    """
    Verifica que el ID de la actividad no exista
    
    Args:
        id_actividad (int): ID a verificar
        
    Returns:
        bool: True si el ID es único, False si ya existe
    """
    actividades = cargar_actividades()
    for act in actividades:
        if act.id_actividad == id_actividad:
            return False
    return True



    
  


def obtener_actividades_por_fecha(fecha_inicio, fecha_fin=None):
    """
    Obtiene actividades dentro de un rango de fechas
    
    Args:
        fecha_inicio (str): Fecha inicial en formato YYYY-MM-DD
        fecha_fin (str): Fecha final en formato YYYY-MM-DD (opcional)
        
    Returns:
        list: Lista de actividades en el rango
    """
    actividades = cargar_actividades()
    resultado = []
    
    try:
        fecha_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_f = datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else fecha_ini
        
        for act in actividades:
            fecha_act = datetime.strptime(act.fecha, '%Y-%m-%d')
            if fecha_ini <= fecha_act <= fecha_f:
                resultado.append(act)
    except ValueError:
        print("✗ Error en el formato de fechas")
    
    return resultado


def obtener_actividades_por_tipo(tipo):
    """
    Obtiene actividades de un tipo específico
    
    Args:
        tipo (str): Tipo de actividad a buscar
        
    Returns:
        list: Lista de actividades del tipo especificado
    """
    actividades = cargar_actividades()
    return [act for act in actividades if act.tipo.lower() == tipo.lower()]


# Prueba del módulo (solo se ejecuta si se corre este archivo directamente)
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO ACTIVIDAD ===\n")
    
    # Crear actividades de prueba
    act1 = Actividad(1, "Pausa activa matutina", "2025-10-15", "Pausa activa", 
                     "Ejercicios de estiramiento y relajación")
    act2 = Actividad(2, "Taller de meditación", "2025-10-20", "Taller", 
                     "Técnicas de mindfulness para reducir estrés")
    act3 = Actividad(3, "Jornada deportiva", "2025-10-25", "Jornada deportiva", 
                     "Torneo de fútbol y voleibol")
    
   
    
    
    
    # Buscar por tipo
    print("\n--- Actividades tipo 'Taller' ---")
    talleres = obtener_actividades_por_tipo("Taller")
    for taller in talleres:
        print(f"  - {taller}")
    
 