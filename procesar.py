import pdfplumber
import json

pdf_path = "lista resultados cv inei eda 2026.pdf"  # Cambia esto por la ruta de tu archivo PDF
datos_totales = []

print("Leyendo el PDF, esto puede tomar unos segundos...")
with pdfplumber.open(pdf_path) as pdf:
    contador = 1
    for i, pagina in enumerate(pdf.pages):
        tabla = pagina.extract_table()
        if tabla:
            # Omitimos los encabezados de las páginas si se repiten
            for fila in tabla:
                # Ajusta los índices según cómo salgan las columnas de tu PDF
                # Ejemplo: [Nro, Sede, Paterno, Materno, Nombres, DNI, Resultado]
                if len(fila) >= 7 and fila[0] != "N°":  
                    # Limpiamos espacios en blanco y unimos los apellidos y nombres en uno solo
                    paterno = (fila[2] or "").strip()
                    materno = (fila[3] or "").strip()
                    nombres_val = (fila[4] or "").strip()
                    
                    nombre_completo = f"{paterno} {materno} {nombres_val}".strip()

                    registro = {
                        "nro": str(contador),
                        "sede": fila[1],
                        "apellidosNombres": nombre_completo,  # Apellidos y nombres unidos en uno solo
                        "dni": fila[5],
                        "resultado": fila[6]
                    }
                    datos_totales.append(registro)
                    contador += 1

# Guardamos los datos en un archivo JSON externo
with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos_totales, f, ensure_ascii=False, indent=4)

print(f"¡Proceso terminado! Se extrajeron {len(datos_totales)} registros en 'datos.json'.")