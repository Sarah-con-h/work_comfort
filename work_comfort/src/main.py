import sys
import os

# Agregar el directorio modules al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Importar módulos
from modules import empleado, actividad, registro, reporte


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_banner():
    """Muestra el banner del sistema"""
    print("\n" + "=" * 70)
    print(" " * 10 + "SISTEMA DE GESTIÓN DE BIENESTAR LABORAL WORK_COMFORT")
    print("=" * 70)


def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\nMENÚ PRINCIPAL")
    print("-" * 70)
    print("  1. Registrar empleado")
    print("  2. Registrar actividad de bienestar")
    print("  3. Registrar participación en actividad")
    print("-" * 70)
    print("  4. Ver lista de empleados")
    print("  5. Ver lista de actividades")
    print("  6. Ver estadísticas de participación")
    print("-" * 70)
    print("  7. Generar reporte general (CSV)")
    print("  8. Generar reporte por área (CSV)")
    print("  9. Generar reporte detallado (CSV)")
    print(" 10. Generar todos los reportes (CSV)")
    print(" 11. Generar resumen ejecutivo (CSV)")
    print("-" * 70)
    print("  0. Salir del sistema")
    print("-" * 70)


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")


def opcion_registrar_empleado():
    limpiar_pantalla()
    mostrar_banner()
    empleado.registrar_empleado_interactivo()
    pausar()


def opcion_registrar_actividad():
    limpiar_pantalla()
    mostrar_banner()
    actividad.registrar_actividad_interactiva()
    pausar()


def opcion_registrar_participacion():
    limpiar_pantalla()
    mostrar_banner()

    print("\n--- EMPLEADOS DISPONIBLES ---")
    empleados = empleado.cargar_empleados()
    if empleados:
        for emp in empleados:
            print(f"  ID {emp.id_empleado}: {emp.nombre}")
    else:
        print("No hay empleados registrados")

    print("\n--- ACTIVIDADES DISPONIBLES ---")
    actividades = actividad.cargar_actividades()
    if actividades:
        for act in actividades:
            print(f"  ID {act.id_actividad}: {act.nombre} ({act.fecha})")
    else:
        print("No hay actividades registradas")

    if not empleados or not actividades:
        print("Debe registrar empleados y actividades primero")
        pausar()
        return

    registro.registrar_participacion_interactiva()
    pausar()


def opcion_ver_empleados():
    limpiar_pantalla()
    mostrar_banner()
    empleado.listar_empleados()
    pausar()


def opcion_ver_actividades():
    limpiar_pantalla()
    mostrar_banner()
    actividad.listar_actividades()
    pausar()


def opcion_ver_estadisticas():
    limpiar_pantalla()
    mostrar_banner()
    registro.mostrar_estadisticas_generales()

    print("\n" + "=" * 60)
    print("  ESTADÍSTICAS POR ACTIVIDAD")
    print("=" * 60)

    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not actividades:
        print("No hay actividades registradas")
    elif not registros:
        print("No hay registros de participación")
    else:
        for act in actividades:
            stats = registro.calcular_estadisticas(registros, act.id_actividad)
            print(f"\n[{act.id_actividad}] {act.nombre} ({act.fecha})")
            print(f"  Asistencias: {stats['asistencias']}/{stats['total_registros']}")
            print(f"  Tasa de participación: {stats['tasa_participacion']}%")
            print(f"  Satisfacción promedio: {stats['satisfaccion_promedio']}/5")

    pausar()


def opcion_generar_reporte_general():
    limpiar_pantalla()
    mostrar_banner()
    print("\nGenerando reporte general...")

    empleados = empleado.cargar_empleados()
    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not actividades:
        print("No hay actividades registradas para generar el reporte")
    elif not registros:
        print("No hay registros de participación para generar el reporte")
    else:
        reporte.generar_reporte_general(empleados, actividades, registros)

    pausar()


def opcion_generar_reporte_por_area():
    limpiar_pantalla()
    mostrar_banner()
    print("\nGenerando reporte por área...")

    empleados = empleado.cargar_empleados()
    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not empleados:
        print("No hay empleados registrados para generar el reporte")
    elif not registros:
        print("No hay registros de participación para generar el reporte")
    else:
        reporte.generar_reporte_por_area(empleados, actividades, registros)

    pausar()


def opcion_generar_reporte_detallado():
    limpiar_pantalla()
    mostrar_banner()
    print("\nGenerando reporte detallado...")

    empleados = empleado.cargar_empleados()
    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not registros:
        print("No hay registros de participación para generar el reporte")
    else:
        reporte.generar_reporte_detallado(empleados, actividades, registros)

    pausar()


def opcion_generar_todos_reportes():
    limpiar_pantalla()
    mostrar_banner()

    empleados = empleado.cargar_empleados()
    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not empleados or not actividades or not registros:
        print("Faltan datos para generar los reportes:")
        if not empleados:
            print("  - No hay empleados registrados")
        if not actividades:
            print("  - No hay actividades registradas")
        if not registros:
            print("  - No hay registros de participación")
    else:
        reporte.generar_todos_los_reportes(empleados, actividades, registros)

    pausar()


def opcion_generar_resumen_ejecutivo():
    limpiar_pantalla()
    mostrar_banner()
    print("\nGenerando resumen ejecutivo...")

    empleados = empleado.cargar_empleados()
    actividades = actividad.cargar_actividades()
    registros = registro.cargar_registros()

    if not empleados or not actividades or not registros:
        print("Faltan datos para generar el resumen")
    else:
        reporte.generar_resumen_ejecutivo(empleados, actividades, registros)

    pausar()


def menu_principal():
    while True:
        limpiar_pantalla()
        mostrar_banner()
        mostrar_menu_principal()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_registrar_empleado()
        elif opcion == "2":
            opcion_registrar_actividad()
        elif opcion == "3":
            opcion_registrar_participacion()
        elif opcion == "4":
            opcion_ver_empleados()
        elif opcion == "5":
            opcion_ver_actividades()
        elif opcion == "6":
            opcion_ver_estadisticas()
        elif opcion == "7":
            opcion_generar_reporte_general()
        elif opcion == "8":
            opcion_generar_reporte_por_area()
        elif opcion == "9":
            opcion_generar_reporte_detallado()
        elif opcion == "10":
            opcion_generar_todos_reportes()
        elif opcion == "11":
            opcion_generar_resumen_ejecutivo()
        elif opcion == "0":
            limpiar_pantalla()
            mostrar_banner()
            print("\nGracias por usar el Sistema de Gestión de Bienestar Laboral.")
            print("Hasta pronto")
            print("=" * 70 + "\n")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción del menú.")
            pausar()


def cargar_datos_de_prueba():
    print("\n¿Desea cargar datos de prueba? (s/n): ", end="")
    respuesta = input().strip().lower()

    if respuesta == 's':
        print("\nCargando datos de prueba...")

        # Empleados de prueba
        emp1 = empleado.Empleado(1, "Ana Martínez", "Recursos Humanos", "Coordinadora")
        emp2 = empleado.Empleado(2, "Carlos Gómez", "Tecnología", "Desarrollador")
        emp3 = empleado.Empleado(3, "Laura Pérez", "Ventas", "Ejecutiva")
        emp4 = empleado.Empleado(4, "Miguel Torres", "Marketing", "Analista")
        emp5 = empleado.Empleado(5, "Sandra Ruiz", "Finanzas", "Contadora")

        empleado.agregar_empleado(emp1)
        empleado.agregar_empleado(emp2)
        empleado.agregar_empleado(emp3)
        empleado.agregar_empleado(emp4)
        empleado.agregar_empleado(emp5)

        # Actividades de prueba
        act1 = actividad.Actividad(1, "Pausa activa matutina", "2025-10-15",
                                   "Pausa activa", "Ejercicios de estiramiento")
        act2 = actividad.Actividad(2, "Taller de manejo de estrés", "2025-10-20",
                                   "Taller", "Técnicas de relajación")
        act3 = actividad.Actividad(3, "Jornada deportiva", "2025-10-25",
                                   "Jornada deportiva", "Torneo de fútbol")

        actividad.agregar_actividad(act1)
        actividad.agregar_actividad(act2)
        actividad.agregar_actividad(act3)

        # Registros de prueba
        registros = [
            registro.Registro(1, 1, True, 5),
            registro.Registro(2, 1, True, 4),
            registro.Registro(3, 1, True, 5),
            registro.Registro(4, 1, False, 0),
            registro.Registro(5, 1, True, 4),
            registro.Registro(1, 2, True, 5),
            registro.Registro(2, 2, True, 5),
            registro.Registro(3, 2, False, 0),
            registro.Registro(4, 2, True, 3),
            registro.Registro(1, 3, True, 4),
            registro.Registro(3, 3, True, 5),
            registro.Registro(5, 3, True, 4)
        ]
        for r in registros:
            registro.registrar_participacion(r)

        print("Datos de prueba cargados exitosamente")
        pausar()


def main():
    try:
        limpiar_pantalla()
        mostrar_banner()
        print("\nBienvenido al Sistema de Gestión de Bienestar Laboral")
        print("Desarrollado para optimizar la gestión de actividades de bienestar\n")
        print("=" * 70)

        empleados_existentes = empleado.cargar_empleados()
        if not empleados_existentes:
            cargar_datos_de_prueba()

        menu_principal()

    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario")
        print("Hasta pronto.\n")
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("Por favor, contacte al administrador del sistema.\n")


if __name__ == "__main__":
    main()
