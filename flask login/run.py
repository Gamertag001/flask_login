from flask import Flask, render_template_string, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# --- Configuración base ---
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesaria para sesiones

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirige si intentas acceder a rutas protegidas

# --- Clase User (simulación de usuarios en memoria) ---
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Base de datos de ejemplo (simulada con un diccionario)
users = {
    "erick": User(1, "erick", "erickgarc"),
    "carlos": User(2, "carlos", "1234")
}

# --- Cargar usuario ---
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

# --- Rutas ---
@app.route("/")
def home():
    return f"Hola {current_user.username}!" if current_user.is_authenticated else "Hola, invitado. <a href='/login'>Inicia sesión</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Credenciales incorrectas"
    
    # Plantilla simple de login
    return render_template_string("""
        <form method="POST">
            <input name="username" placeholder="Usuario"><br>
            <input name="password" type="password" placeholder="Contraseña"><br>
            <button type="submit">Iniciar sesión</button>
        </form>
    """)

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Bienvenido {current_user.username}! <a href='/logout'>Cerrar sesión</a>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# --- Ejecutar ---
if __name__ == "__main__":
    app.run(debug=True)
