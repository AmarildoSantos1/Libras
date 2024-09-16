from flask import Flask, jsonify, request
import os
from biblioteca import Biblioteca, Livro, Usuario, UsuarioJaExisteException

app = Flask(__name__)

# Inicializa a classe Biblioteca
biblioteca = Biblioteca()

# Endpoint para adicionar livro (POST)
@app.route('/api/livros', methods=['POST'])
def adicionar_livro():
    dados = request.json
    titulo = dados.get('titulo')
    autor = dados.get('autor')
    ano = dados.get('ano')
    temas = dados.get('temas').split(",")

    livro = Livro(titulo, autor, int(ano), temas)
    biblioteca.adicionar_livro(livro)
    return jsonify({"mensagem": "Livro adicionado com sucesso!"}), 201

# Endpoint para listar livros (GET)
@app.route('/api/livros', methods=['GET'])
def listar_livros():
    livros = biblioteca.arvore_livros.listar_livros()
    lista_livros = [{"titulo": livro.titulo, "autor": livro.autor, "ano": livro.ano, "temas": livro.temas} for livro in livros]
    return jsonify(lista_livros)

# Endpoint para cadastrar usuário (POST)
@app.route('/api/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')

    try:
        usuario = Usuario(nome, email)
        biblioteca.cadastrar_usuario(usuario)
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
    except UsuarioJaExisteException as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
