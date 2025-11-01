from pathlib import Path
from src.modules.reporte import exportar_csv_generico

def test_exportar_csv_generico(tmp_path):
    archivo = tmp_path / "reporte_test.csv"
    datos = [[1, 2, 3], [4, 5, 6]]
    columnas = ["col1", "col2", "col3"]

    exito = exportar_csv_generico(datos, columnas, str(archivo), descripcion="Test CSV")
    assert exito is True
    assert archivo.exists()
    contenido = archivo.read_text(encoding="utf-8")
    assert "col1" in contenido
    assert "1" in contenido