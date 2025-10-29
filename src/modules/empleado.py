import os

class Empleado:
    """Clase que representa un empleado de la organización"""
    
    def __init__(self, id_empleado, nombre, area, cargo):
        """
        Constructor de la clase Empleado
        
        Args:
            id_empleado (int): Identificador único del empleado
            nombre (str): Nombre completo del empleado
            area (str): Área o departamento donde trabaja
            cargo (str): Cargo o posición del empleado
        """
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.area = area
        self.cargo = cargo
    
    def to_string(self):
        """Convierte el empleado a formato de texto para guardar"""
        return f"{self.id_empleado}|{self.nombre}|{self.area}|{self.cargo}"
    
    @staticmethod
    def from_string(linea):
        """
        Crea un objeto Empleado desde una línea de texto
        
        Args:
            linea (str): Línea con formato: id|nombre|area|cargo
            
        Returns:
            Empleado: Objeto empleado creado
        """
        try:
            partes = linea.strip().split('|')
            if len(partes) != 4:
                raise ValueError("Formato inválido de empleado")
            return Empleado(int(partes[0]), partes[1], partes[2], partes[3])
        except Exception as e:
            print(f"Error al leer empleado: {e}")
            return None
    
    def __str__(self):
        """Representación en string del empleado"""
        return f"[{self.id_empleado}] {self.nombre} - {self.cargo} ({self.area})"


def agregar_empleado(empleado, archivo='src/data/empleados.txt'):
    """
    Agrega un empleado al archivo de datos
    
    Args:
        empleado (Empleado): Objeto empleado a guardar
        archivo (str): Ruta del archivo de empleados
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        
        # Agregar al archivo
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(empleado.to_string() + '\n')
        print(f"✓ Empleado '{empleado.nombre}' registrado exitosamente")
    except Exception as e:
        print(f"✗ Error al guardar empleado: {e}")


def cargar_empleados(archivo='src/data/empleados.txt'):
    """
    Carga todos los empleados desde el archivo
    
    Args:
        archivo (str): Ruta del archivo de empleados
        
    Returns:
        list: Lista de objetos Empleado
    """
    empleados = []
    try:
        if not os.path.exists(archivo):
            print(f"⚠ El archivo {archivo} no existe. Se creará al agregar empleados.")
            return empleados
        
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                if linea.strip():  # Ignorar líneas vacías
                    emp = Empleado.from_string(linea)
                    if emp:
                        empleados.append(emp)
    except Exception as e:
        print(f"✗ Error al cargar empleados: {e}")
    
    return empleados


def listar_empleados():
    """Muestra en consola todos los empleados registrados"""
    empleados = cargar_empleados()
    
    if not empleados:
        print("\n⚠ No hay empleados registrados")
        return
    
    print("\n" + "="*60)
    print("  LISTA DE EMPLEADOS")
    print("="*60)
    for emp in empleados:
        print(emp)
    print("="*60)
    print(f"Total de empleados: {len(empleados)}")


def obtener_empleado_por_id(id_empleado):
    """
    Busca un empleado por su ID
    
    Args:
        id_empleado (int): ID del empleado a buscar
        
    Returns:
        Empleado: Objeto empleado encontrado o None
    """
    empleados = cargar_empleados()
    for emp in empleados:
        if emp.id_empleado == id_empleado:
            return emp
    return None


def validar_id_unico(id_empleado):
    """
    Verifica que el ID del empleado no exista
    
    Args:
        id_empleado (int): ID a verificar
        
    Returns:
        bool: True si el ID es único, False si ya existe
    """
    empleados = cargar_empleados()
    for emp in empleados:
        if emp.id_empleado == id_empleado:
            return False
    return True


def registrar_empleado_interactivo():
    """Función interactiva para registrar un empleado desde consola"""
    print("\n" + "="*60)
    print("  REGISTRO DE NUEVO EMPLEADO")
    print("="*60)
    
    try:
        # Solicitar ID
        while True:
            id_emp = input("ID del empleado: ").strip()
            if not id_emp.isdigit():
                print("✗ El ID debe ser un número entero")
                continue
            id_emp = int(id_emp)
            if not validar_id_unico(id_emp):
                print("✗ Este ID ya existe. Ingrese otro.")
                continue
            break
        
        # Solicitar nombre
        while True:
            nombre = input("Nombre completo: ").strip()
            if len(nombre) < 3:
                print("✗ El nombre debe tener al menos 3 caracteres")
                continue
            break
        
        # Solicitar área
        print("\nÁreas disponibles:")
        areas = ["Recursos Humanos", "Tecnología", "Ventas", "Marketing", 
                 "Finanzas", "Operaciones", "Administración"]
        for i, area in enumerate(areas, 1):
            print(f"  {i}. {area}")
        
        while True:
            area_op = input("Seleccione el número del área (o escriba una nueva): ").strip()
            if area_op.isdigit() and 1 <= int(area_op) <= len(areas):
                area = areas[int(area_op) - 1]
                break
            elif len(area_op) > 0:
                area = area_op
                break
            else:
                print("✗ Debe ingresar un área válida")
        
        # Solicitar cargo
        cargo = input("Cargo: ").strip()
        if not cargo:
            cargo = "Sin especificar"
        
        # Crear y guardar empleado
        nuevo_empleado = Empleado(id_emp, nombre, area, cargo)
        agregar_empleado(nuevo_empleado)
        
    except KeyboardInterrupt:
        print("\n\n✗ Registro cancelado por el usuario")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")


# Prueba del módulo (solo se ejecuta si se corre este archivo directamente)
if __name__ == "__main__":
    print("=== PRUEBA DEL MÓDULO EMPLEADO ===\n")
    
    # Crear empleados de prueba
    emp1 = Empleado(1, "Juan Pérez", "Recursos Humanos", "Coordinador")
    emp2 = Empleado(2, "María García", "Tecnología", "Desarrolladora")
    emp3 = Empleado(3, "Carlos López", "Ventas", "Ejecutivo")
    
    # Guardar empleados
    agregar_empleado(emp1)
    agregar_empleado(emp2)
    agregar_empleado(emp3)
    
    # Listar empleados
    listar_empleados()
    
    # Buscar empleado
    print("\n--- Búsqueda de empleado ---")
    emp_encontrado = obtener_empleado_por_id(2)
    if emp_encontrado:
        print(f"Empleado encontrado: {emp_encontrado}")
    
    # Registro interactivo
    print("\n--- Registro interactivo ---")
    respuesta = input("¿Desea registrar un empleado? (s/n): ")
    if respuesta.lower() == 's':
        registrar_empleado_interactivo()
<<<<<<< HEAD
        listar_empleados()
=======
        listar_empleados()

# **Archivo:** `src/modules/empleado.py`

"""Responsabilidades:
- Clase `Empleado` con atributos: id, nombre, área, cargo
- Función para agregar empleados
- Función para listar empleados
- Guardar/cargar empleados desde archivo"""
>>>>>>> 03b8455 (Responsabilidades del archivo de sarah)
