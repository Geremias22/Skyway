from flask import Flask, render_template, request
from controllers.generador_vuelos import buscar_vuelos
from controllers.generador_hoteles import buscar_hoteles
print("✅ buscar_hoteles importado correctamente")

app = Flask(__name__)

@app.route("/")
def inicio():
    return "<h1>Bienvenido a Skyway ✈️</h1><p>Visita <a href='/vuelos'>/vuelos</a> para ver resultados.</p>"

@app.route("/vuelos")
def mostrar_vuelos():
    vuelos = buscar_vuelos()  # Esta función ya prepara y devuelve los vuelos procesados
    return render_template("resultados_vuelos.html", vuelos=vuelos, origen=vuelos[0]["salida"], destino=vuelos[0]["llegada"])

@app.route('/buscar', methods=['POST'])
def procesar_busqueda():
    # Obtener los datos del formulario
    lugar = request.form.get('location')
    num_personas = request.form.get('days')
    fecha = request.form.get('date')
    print(lugar, num_personas, fecha)


# @app.route('/hoteles')
# def ruta_hoteles():
#     hoteles = buscar_hoteles()
#     print("🏨 hoteles pasados al template:", hoteles)
#     return render_template('resultados_hoteles.html', hoteles=hoteles)

@app.route("/hoteles")
def ruta_hoteles():
    datos = buscar_hoteles(destino_code="BCN", noches=2)
    return render_template(
        "resultados_hoteles.html",
        total_hotels=datos["total_hotels"],
        total_offers=datos["total_offers"],
        hoteles=datos["hoteles"],
        check_in=datos["check_in"],
        check_out=datos["check_out"]
    )

# @app.route('/actividades')
# def ruta_actividades():
#     actividades = buscar_actividades()
#     return render_template('resultados_actividades.html', actividades=actividades)
    
if __name__ == "__main__":
    app.run(debug=True)
