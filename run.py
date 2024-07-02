import os
from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_cors import CORS
from app.database import init_app
from app.views import *

# Obtener la ruta absoluta al directorio actual
basedir = os.path.abspath(os.path.dirname(__file__))

# Ruta al directorio de plantillas
template_dir = os.path.join(basedir, 'templates')

# Ruta al directorio de archivos estáticos
static_dir = os.path.join(basedir,  'static')

# Inicialización de Flask con la carpeta de plantillas y estáticos especificada
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicializar la base de datos con la aplicación Flask
init_app(app)
# Permitir solicitudes desde cualquier origen
CORS(app)

# Rutas para el CRUD de la entidad Registro
app.route('/api/users/', methods=['POST'])(create_user)
app.route('/api/users/', methods=['GET'])(get_all_users)
app.route('/api/users/<int:user_id>', methods=['GET'])(get_user)
app.route('/api/users/<int:user_id>', methods=['PUT'])(update_user)
app.route('/api/users/<int:user_id>', methods=['DELETE'])(delete_user)

# Rutas web adicionales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planes')
def planes():
    return render_template('planes.html')

@app.route('/DondeEstamos')
def DondeEstamos():
    return render_template('DondeEstamos.html')

@app.route('/Acceder', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        
        user = Registro.get_by_email_and_password(email, password)
        
        if user:
            session['logged_in'] = True
            session['user_email'] = email
            session['user_role'] = user.rol
            
            if user.rol == 'admin':
                return redirect(url_for('gestion'))
            else:
                return redirect(url_for('index'))
        else:
            error = 'Usuario inexistente o contraseña incorrecta'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/Registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        password = request.form['psw']
        
        existing_user = Registro.get_by_email(email)
        
        if existing_user:
            flash('El usuario ya existe. Por favor, intente con otro correo electrónico.', 'error')
            return redirect(url_for('registro'))
        
        new_user = Registro(name=nombre, email=email, password=password)
        new_user.save()
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/Salir')
def salir():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/gestion')
def gestion():
    users = Registro.get_all()
    return render_template('administrador/gestion.html', usuarios=users)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        
        existing_user = Registro.get_by_email(email)
        
        if existing_user:
            flash('El usuario ya existe. Por favor, intente con otro correo electrónico.', 'error')
            return redirect(url_for('create'))
        
        new_user = Registro(name=nombre, email=email, password=password, rol=rol)
        new_user.save()
        return redirect(url_for('gestion'))
    
    return render_template('administrador/usuario_create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = Registro.get_by_id(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.rol = request.form['rol']
        user.save()
        return redirect(url_for('gestion'))
    
    return render_template('administrador/usuario_edit.html', usuario=user)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user = Registro.get_by_id(id)
    if user:
        user.delete()
    return redirect(url_for('gestion'))

@app.route('/Medicos')
def medicos():
    return render_template('medicos.html')

@app.route('/MetodosDePagos')
def metodos_de_pagos():
    return render_template('MetodosDePagos.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')

@app.route('/preguntas')
def preguntas():
    return render_template('preguntas.html')

if __name__ == '__main__':
    app.run(debug=True)
