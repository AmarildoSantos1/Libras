from flask import Flask, render_template, request, redirect, url_for
import os
from biblioteca import Biblioteca, Livro, Usuario, UsuarioJaExisteException

app = Flask(__name__)

# Configuração da pasta para armazenar as fotos enviadas
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Inicializa a classe Biblioteca
biblioteca = Biblioteca()

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar um novo livro
@app.route('/adicionar_livro', methods=['POST'])
def adicionar_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    temas = request.form['temas'].split(",")
    
    livro = Livro(titulo, autor, int(ano), temas)
    biblioteca.adicionar_livro(livro)
    return redirect(url_for('index'))

# Rota para upload de foto
@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    if 'foto' not in request.files:
        return redirect(request.url)
    
    foto = request.files['foto']
    if foto.filename == '':
        return redirect(request.url)
    
    if foto:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(filepath)
        return redirect(url_for('index'))

# Rota para cadastro de usuários
@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    
    try:
        usuario = Usuario(nome, email)
        biblioteca.cadastrar_usuario(usuario)
    except UsuarioJaExisteException as e:
        print(f"Erro: {str(e)}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
