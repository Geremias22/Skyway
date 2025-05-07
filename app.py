from flask import Flask, render_template, request
from controllers.generador_vuelos import buscar_vuelos

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
    
if __name__ == "__main__":
    app.run(debug=True)
