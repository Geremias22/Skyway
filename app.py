from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask import Flask, render_template, request, jsonify
from controllers.generador_vuelos import buscar_vuelos
from controllers.generador_hoteles import buscar_hoteles
from controllers.google_places import get_place_details_by_text
from controllers.generador_actividades import buscar_actividades
from controllers.dashboard_generator import generar_dashboard_completo
from db import db  # asumiendo que tienes una conexión MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, url_for, session, flash
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/vuelos")
def mostrar_vuelos():
    vuelos = buscar_vuelos(
        origen="MAD",
        destino="BCN",
        fecha="2025-06-01"
    )
    return render_template(
        "resultados_vuelos.html",
        vuelos=vuelos,
        origen="MAD",
        destino="BCN"
    )
    # return render_template("resultados_vuelos.html", vuelos=vuelos, origen=vuelos[0]["salida"], destino=vuelos[0]["llegada"])

@app.route('/buscar', methods=['GET', 'POST'])
def procesar_busqueda_con_destino():
    if request.method == 'POST':
        # Nombres correctos desde el formulario
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        fecha = request.form.get('fecha')
        dias = request.form.get('dias')
        personas = request.form.get('personas')

        if not all([origen, destino, fecha, dias, personas]):
            return "Faltan datos en el formulario", 400

        print("DEBUG:", origen, destino, fecha, dias, personas)

        return redirect(url_for('mostrar_dashboard', 
                                origen=origen, 
                                destino=destino, 
                                dias=dias, 
                                fecha=fecha,
                                personas=personas))
    else:
        return render_template("buscar.html")


@app.route('/explorar', methods=['GET', 'POST'])
def procesar_busqueda_sin_destino():
    if request.method == 'POST':
        # Procesar formulario
        location = request.form.get('location')
        personas = request.form.get('days')
        fecha = request.form.get('date')

        # Aquí puedes hacer validaciones, generar datos, etc.
        return redirect(url_for('mostrar_dashboard', 
                                origen=location, 
                                destino="LEN",  # esto lo puedes ajustar luego
                                dias=personas, 
                                fecha=fecha,
                                personas=personas))
    else:
        # Mostrar el formulario
        return render_template("explorar.html")



@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = db.usuarios.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        session["username"] = user["username"]
        flash("Sesión iniciada correctamente.")
        return redirect(url_for("inicio"))
    else:
        flash("Correo o contraseña incorrectos.")
        return redirect(url_for("inicio"))

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    if password != confirm:
        flash("Las contraseñas no coinciden.")
        return redirect(url_for("inicio"))

    if db.usuarios.find_one({"email": email}):
        flash("El correo ya está registrado.")
        return redirect(url_for("inicio"))

    pw_hash = generate_password_hash(password)
    db.usuarios.insert_one({
        "username": username,
        "email": email,
        "password": pw_hash
    })
    session["username"] = username
    flash("Registro exitoso.")
    return redirect(url_for("inicio"))
# --------------------------------------------------------------------------------------

@app.route("/hotel/<hotel_id>/gm-info")
def ruta_gm_info(hotel_id):
    datos = buscar_hoteles(destino_code="BCN", noches=2)
    hotel = next((h for h in datos["hoteles"] if h["hotelId"] == hotel_id), None)
    if not hotel:
        return jsonify({"error": "Hotel no encontrado"}), 404

    # Directamente Text Search + Details
    detalles = get_place_details_by_text(hotel["nombre"], "Barcelona")
    if not detalles:
        return ("", 204)
    return jsonify(detalles)

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

@app.route("/actividades")
def ruta_actividades():
    # Para BCN usamos coordenadas aproximadas del centro
    lat_bc, lon_bc = 41.3851, 2.1734
    actividades = buscar_actividades(lat_bc, lon_bc, radius_km=5)
    return render_template(
        "resultados_actividades.html",
        actividades=actividades,
        ciudad="Barcelona"
    )


# @app.route("/dashboard")
# def mostrar_dashboard():
#     # ⚠️ Puedes hacerlo dinámico leyendo de query params o base de datos
#     datos = generar_dashboard_completo(
#         origen="BCN",
#         destino="LEN",
#         dias="4",  
#         fecha="2025-08-18",
#         personas="2"
#     )
#     return render_template("dashboard.html", **datos)


@app.route("/dashboard")
def mostrar_dashboard():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    dias = request.args.get('dias')
    fecha = request.args.get('fecha')
    personas = request.args.get('personas')

    datos = generar_dashboard_completo(
        origen=origen,
        destino=destino,
        dias=dias,
        fecha=fecha,
        personas=personas
    )
    return render_template("dashboard.html", **datos)
    
if __name__ == "__main__":
    app.run(debug=True)
