class Livro:
    def __init__(self, titulo, autor, ano, temas):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.temas = temas

class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class UsuarioJaExisteException(Exception):
    pass

class LivroNaoEncontradoException(Exception):
    pass

class ArvoreBinariaDeLivros:
    def __init__(self):
        self.livros = []

    def inserir(self, livro):
        self.livros.append(livro)

    def listar_livros(self):
        return self.livros

    def ordenar_livros(self, criterio="titulo"):
        if criterio == "titulo":
            self.livros.sort(key=lambda livro: livro.titulo)
        elif criterio == "autor":
            self.livros.sort(key=lambda livro: livro.autor)
        return self.livros

class GrafoAutores:
    def __init__(self):
        self.autores = {}

    def adicionar_livro(self, livro):
        for autor in livro.autor:
            if autor not in self.autores:
                self.autores[autor] = []
            self.autores[autor].extend(livro.temas)

    def recomendar_por_tema(self, tema):
        recomendacoes = []
        for autor, temas in self.autores.items():
            if tema in temas:
                recomendacoes.append(autor)
        return recomendacoes

class Biblioteca:
    def __init__(self):
        self.usuarios = {}
        self.arvore_livros = ArvoreBinariaDeLivros()
        self.grafo_autores = GrafoAutores()

    def adicionar_livro(self, livro):
        self.arvore_livros.inserir(livro)
        self.grafo_autores.adicionar_livro(livro)

    def cadastrar_usuario(self, usuario):
        if usuario.email in self.usuarios:
            raise UsuarioJaExisteException("Usuário com esse e-mail já existe.")
        self.usuarios[usuario.email] = usuario

    def recomendar_livros_por_autor(self, autor):
        recomendacoes = []
        for livro in self.arvore_livros.listar_livros():
            if livro.autor == autor:
                recomendacoes.append(livro)
        return recomendacoes

    def recomendar_livros_por_tema(self, tema):
        return self.grafo_autores.recomendar_por_tema(tema)
