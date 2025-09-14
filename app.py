from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from flask import jsonify
import pandas as pd
import hashlib
import os

from crud import Crud
from gerador_senha import PasswordGenerator



app = Flask(__name__)
app.secret_key = "segredo_muito_seguro"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ph = PasswordHasher()
gen = PasswordGenerator()

# Tabela do banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

# Criar o banco na primeira execução
with app.app_context():
    db.create_all()
    
# ===================== UTILS =====================
def get_csv_filename(senha_hash: str) -> str:
    """Gera nome seguro de CSV a partir do hash da senha"""
    safe_hash = hashlib.sha256(senha_hash.encode()).hexdigest()
    return f"locker_{safe_hash}.csv"

def get_user_crud() -> Crud:
    """Retorna um Crud configurado para o usuário logado"""
    if "user_csv" not in session:
        return None # type: ignore
    return Crud(session["user_csv"])

#home
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario:
            try:
                ph.verify(usuario.senha_hash, senha)
                csv_file = get_csv_filename(usuario.senha_hash)
                
                
                print(csv_file)
                session['user_csv'] = csv_file
                
                return redirect(url_for('home_page'))    
            except:
                return 'Senha incorreta.'
        else:
            return 'Usuário não encontrado.'
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        if Usuario.query.filter_by(nome=nome).first():
            return 'Usuário já existe.'
        senha_hash = ph.hash(senha)
        novo_usuario = Usuario(nome=nome, senha_hash=senha_hash) # type: ignore
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ===================== API CRUD LOCKER =====================

# READ - listar tudo
@app.route('/home', methods=['GET'])
def home_page():
    if 'user_csv' not in session:
        return redirect(url_for('login'))
    # Se for chamada via navegador → renderiza HTML
    if request.headers.get("Accept") and "text/html" in request.headers.get("Accept"): # type: ignore
        return render_template("home.html")
    # Se for chamada via fetch → retorna JSON
    crud = get_user_crud()
    df = crud.list_all()
    return jsonify(df.to_dict(orient="records"))

# CREATE - gera senha nova automaticamente
@app.route('/home', methods=['POST'])
def create_senha():
    if 'user_csv' not in session:
        return redirect(url_for('login'))
    data = request.get_json()
    site = data.get("site")
    user = data.get("user")
    password = gen.generate_password()  # senha automática
    
    crud = get_user_crud()
    crud.create(site, user, password)
    return jsonify({"message": "Registro criado com sucesso!", "site": site, "user": user, "password": password})

# UPDATE - gera nova senha automaticamente ao atualizar
@app.route('/home', methods=['PUT'])
def update_senha():
    data = request.get_json()
    site = data.get("site")
    new_user = data.get("user")
    new_password = gen.generate_password()  # senha automática
    
    crud = get_user_crud()
    success = crud.update(site, new_user=new_user, new_password=new_password)
    if success:
        return jsonify({"message": "Registro atualizado com sucesso!", "site": site, "user": new_user, "password": new_password})
    return jsonify({"error": "Site não encontrado"}), 404

# DELETE
@app.route('/home', methods=['DELETE'])
def delete_senha():
    data = request.get_json()
    site = data.get("site")
    
    crud = get_user_crud()
    success = crud.delete(site)
    if success:
        return jsonify({"message": "Registro deletado com sucesso!", "site": site})
    return jsonify({"error": "Site não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)