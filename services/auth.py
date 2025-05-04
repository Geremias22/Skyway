from db import db
from getpass import getpass
try:
    # Use Werkzeug for password hashing
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    raise ImportError("Instala Werkzeug: pip install werkzeug")


def gestionar_usuario():
    """
    Gestiona el flujo de autenticación y registro de usuarios por consola.
    Permite 'login' o 'register' (registrarse), valida credenciales y guarda usuario.
    Devuelve el nombre de usuario una vez autenticado.
    """
    while True:
        accion = input("🔐 ¿Quieres iniciar sesión o registrarte? (login/register): ").strip().lower()
        # Login existente
        if accion in ["login", "l"]:
            email = input("📧 Correo: ").strip().lower()
            contrasena = getpass("🔑 Contraseña: ")
            usuario = db.usuarios.find_one({"email": email})
            if usuario and check_password_hash(usuario.get("password", ""), contrasena):
                print(f"✅ Sesión iniciada. ¡Bienvenido {usuario.get('username')}!")
                return usuario.get('username')
            else:
                print("❌ Usuario o contraseña incorrectos. Inténtalo de nuevo.")

        # Registro nuevo
        elif accion in ["register", "r", "registrar"]:
            username = input("👤 Nombre de usuario: ").strip()
            email = input("📧 Correo: ").strip().lower()
            # Verificar email único
            if db.usuarios.find_one({"email": email}):
                print("❌ Este correo ya está registrado.")
                continue
            # Pedir y confirmar contraseña
            while True:
                contr1 = getpass("🔑 Contraseña: ")
                contr2 = getpass("🔑 Repite la contraseña: ")
                if contr1 != contr2:
                    print("❌ Las contraseñas no coinciden. Intenta de nuevo.")
                else:
                    break
            # Crear usuario con hash de contraseña
            pw_hash = generate_password_hash(contr1)
            db.usuarios.insert_one({
                "username": username,
                "email": email,
                "password": pw_hash
            })
            print(f"✅ Cuenta creada correctamente. ¡Bienvenido {username}!")
            return username

        else:
            print("Por favor, escribe 'login' para iniciar sesión o 'register' para crear una cuenta.")
