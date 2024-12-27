from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'raymundosoto.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'raymundosoto'
app.config['MYSQL_PASSWORD'] = 'Soto1981Soto'
app.config['MYSQL_DB'] = 'raymundosoto$flask_auth'

mysql = MySQL(app)

# Clave secreta para las sesiones
app.secret_key = 'mi_secreto_super_seguro'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        correo = request.form['correo']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO users (nombre, apellidos, fecha_nacimiento, correo, username, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, apellidos, fecha_nacimiento, correo, username, password)
            )
            mysql.connection.commit()
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error al registrar: ' + str(e), 'danger')
        finally:
            cur.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
