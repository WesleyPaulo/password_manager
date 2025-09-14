from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from flask import jsonify
import pandas as pd

from crud import Crud
from gerador_senha import PasswordGenerator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ph = PasswordHasher()

crud = Crud()
gen = PasswordGenerator()

# Tabela do banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

# Criar o banco na primeira execução
with app.app_context():
    db.create_all()

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

# ===================== API CRUD LOCKER =====================

# READ - listar tudo
@app.route('/home', methods=['GET'])
def home_page():
    # Se for chamada via navegador → renderiza HTML
    if request.headers.get("Accept") and "text/html" in request.headers.get("Accept"): # type: ignore
        return render_template("home.html")
    # Se for chamada via fetch → retorna JSON
    df = pd.read_csv("locker.csv")
    return jsonify(df.to_dict(orient="records"))

# CREATE - gera senha nova automaticamente
@app.route('/home', methods=['POST'])
def create_senha():
    data = request.get_json()
    site = data.get("site")
    user = data.get("user")
    password = gen.generate_password()  # senha automática
    crud.create(site, user, password)
    return jsonify({"message": "Registro criado com sucesso!", "site": site, "user": user, "password": password})

# UPDATE - gera nova senha automaticamente ao atualizar
@app.route('/home', methods=['PUT'])
def update_senha():
    data = request.get_json()
    site = data.get("site")
    new_user = data.get("user")
    new_password = gen.generate_password()  # senha automática
    success = crud.update(site, new_user=new_user, new_password=new_password)
    if success:
        return jsonify({"message": "Registro atualizado com sucesso!", "site": site, "user": new_user, "password": new_password})
    return jsonify({"error": "Site não encontrado"}), 404

# DELETE
@app.route('/home', methods=['DELETE'])
def delete_senha():
    data = request.get_json()
    site = data.get("site")
    success = crud.delete(site)
    if success:
        return jsonify({"message": "Registro deletado com sucesso!", "site": site})
    return jsonify({"error": "Site não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)