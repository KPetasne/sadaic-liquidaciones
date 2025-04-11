from flask import Flask, render_template, request, send_file
from backend.extract import extraer_y_procesar_tablas
from backend.combine import combinar_tablas
from backend.summarize import generar_tabla_resumida
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    tabla_resumida = None
    csv_path = None
    tabla_disponible = False

    if request.method == "POST":
        file = request.files["file"]

        # Validar el archivo
        if file and file.filename != "":
            # Asegurarse de que exista el directorio 'temp'
            os.makedirs("temp", exist_ok=True)

            # Guardar el archivo subido con un nombre único
            filename = f"{uuid.uuid4()}_{file.filename}"
            file_path = f"temp/{filename}"
            file.save(file_path)

            # Procesar el archivo PDF
            tablas = extraer_y_procesar_tablas(file_path)
            tabla_combinada = combinar_tablas(tablas)
            tabla_resumida = generar_tabla_resumida(tabla_combinada)

            # Guardar el archivo CSV
            csv_path = "temp/resultados.csv"
            tabla_resumida.to_csv(csv_path, index=False)

            # Actualizar el estado de la tabla
            if not tabla_resumida.empty:
                tabla_disponible = True
        else:
            return "Por favor, sube un archivo válido.", 400

    return render_template("index.html", tabla_resumida=tabla_resumida, csv_path=csv_path, tabla_disponible=tabla_disponible)

@app.route("/descargar_csv", methods=["GET"])
def descargar_csv():
    # Ruta al archivo CSV generado
    csv_path = request.args.get("csv_path")
    if os.path.exists(csv_path):
        return send_file("../"+csv_path, as_attachment=True)
    return "Archivo no encontrado", 404

if __name__ == "__main__":
    app.run(debug=True, port=8080)
