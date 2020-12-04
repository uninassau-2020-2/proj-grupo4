from flask import Flask, render_template, request, url_for, redirect, g, session
from flask_sqlalchemy import SQLAlchemy


# CONFIGURANDO FLASK E O BANCO
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# ----------------------------------------------------------------CLASSE USUÁIO--------------------------------------------------------------------


class Usuario(db.Model):
    # CRIAÇÃO DA TABELA DO BANCO
    __tablename = 'usuario'
    id_Usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    adm = db.Column(db.Boolean)
    venda_usuario = db.relationship('Venda', backref='addVenda', lazy='select')

    # CONSTRUTOR
    def __init__(self, email, senha, adm):
        self.email = email
        self.senha = senha
        self.adm = adm

# ROTA DA PAGINA INDEX


@app.route('/home')
def index():
    return render_template('index.html')


@app.before_request
def auth():
    if 'usuario_id' in session:
        user = Usuario.query.filter_by(
            id_Usuario=session['usuario_id']).first()
        g.user = user


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def login():
    if request.method == 'POST' or 'OPTIONS':
        session.pop('usuario_id', None)
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            session['usuario_id'] = usuario.id_Usuario
            return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('login.html')

# ROTA DA PAGINA USUÁRIO


@app.route('/usuario')
def usuario():
    return render_template('usuarioView/usuario.html')

# ROTA DA  PAGINA DO CADASTRO


@app.route('/cadastrarUsuario')
def cadastrarUsuario():
    return render_template('usuarioView/cadastroUsuario.html')

# ROTA DO METODO DE CADASTRAR


@app.route('/cadastrarUsuario', methods=['GET', 'POST'])
# METODO DE CADASTRAR
def cadastroUsuario():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        adm = False if request.form.get('adm') is None else True

        if email and senha and adm is not None:
            u = Usuario(email, senha, adm)
            db.session.add(u)
            db.session.commit()

        return redirect(url_for('usuario'))

# ROTA DA PAGINA DE LISTA


@app.route('/listaUsuario')
# METODO DE LISTAR
def listaUsuario():
    usuarios = Usuario.query.all()
    return render_template('usuarioView/listaUsuario.html', usuarios=usuarios)

# excluir pelo ID


@app.route('/excluirUsuario/<int:id>')
def excluirUsuario(id):
    usuario = Usuario.query.filter_by(id_Usuario=id).first()
    db.session.delete(usuario)
    db.session.commit()
    # apos excluir vai voltar para pagina de listar
    usuarios = usuario.query.all()
    return render_template('usuarioView/listaUsuario.html', usuarios=usuarios)

# ATUALIZAR pelo ID recebendo um get do parametro e retornando um post


@app.route('/atualizarUsuario/<int:id>', methods=['GET', 'POST'])
def atualizarUsuario(id):
    usuario = Usuario.query.filter_by(id_Usuario=id).first()

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        adm = False if request.form.get('adm') is None else True

        if email and senha and adm is not None:
            usuario.email = email
            usuario.senha = senha
            usuario.adm = adm

            db.session.commit()

            return redirect(url_for('listaUsuario'))

    return render_template('usuarioView/atualizarUsuario.html', usuario=usuario)


    # ----------------------------------------------------------------TABELA DE RELACIONAMENTO fornecedor_produto--------------------------------------------------------------------
fornecedor_produto = db.Table('fornecedor_produto',
                              db.Column('codProduto', db.Integer, db.ForeignKey(
                                  'produto._codProduto'), primary_key=True),
                              db.Column('codFornecedor', db.Integer, db.ForeignKey(
                                  'fornecedor._codFornecedor'), primary_key=True)
                              )

# ----------------------------------------------------------------CLASSE PRODUTO--------------------------------------------------------------------


class Produto(db.Model):
    # CRIAÇÃO DA TABELA DO BANCO
    __tablename = 'produto'
    _codProduto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeProduto = db.Column(db.String)
    valorProduto = db.Column(db.Float)
    qntEstoque = db.Column(db.Integer)
    fornecido = db.relationship('Fornecedor', secondary=fornecedor_produto, lazy='subquery',
                                backref=db.backref('fornec', lazy=True))

    # CONSTRUTOR
    def _init_(self, nomeProduto, valorProduto, qntEstoque):
        self.nomeProduto = nomeProduto
        self.valorProduto = valorProduto
        self.qntEstoque = qntEstoque


# ROTA DA PAGINA USUÁRIO


@app.route('/produtoPage')
def produtoPage():
    return render_template('produtoView/produto.html')

# ROTA DA  PAGINA DO CADASTRO


@app.route('/produto/cadastrar')
def cadastrarProdutos():
    return render_template('produtoView/cadastroProdutos.html')

# ROTA DO METODO DE CADASTRAR


@app.route('/produto/cadastro', methods=['GET', 'POST'])
# METODO DE CADASTRAR
def cadastroProdutos():
    if request.method == 'POST':
        nomeProduto = request.form['nomeProduto']
        valorProduto = request.form['valorProduto']
        qntEstoque = request.form['qntEstoque']
        listaCodigoFornecedores = [1, 2, 3]

        if nomeProduto and valorProduto and qntEstoque and listarFornecedores:
            p = Produto(nomeProduto=nomeProduto,
                        valorProduto=valorProduto, qntEstoque=qntEstoque)

            for codFornecedor in listaCodigoFornecedores:
                fornecedor = Fornecedor.query.filter_by(
                    _codFornecedor=codFornecedor).first()
                p.fornecido.append(fornecedor)

        db.session.add(p)
        db.session.commit()
        return redirect(url_for('produtoPage'))

# ROTA DA PAGINA DE LISTA


@app.route('/produtos')
# METODO DE LISTAR
def listarProdutos():
    produtos = Produto.query.all()
    return render_template('produtoView/listaProdutos.html', produtos=produtos)

# excluir pelo ID


@app.route('/produtos/excluir/<int:codProduto>')
def excluirProdutos(codProduto):
    produto = Produto.query.filter_by(_codProduto=codProduto).first()
    db.session.delete(produto)
    db.session.commit()
    # apos excluir vai voltar para pagina de listar
    produtos = Produto.query.all()
    return render_template('produtoView/listaProdutos.html', produtos=produtos)

# ATUALIZAR pelo ID recebendo um get do parametro e retornando um post


@app.route('/produtos/atualizar/<int:codProduto>', methods=['GET', 'POST'])
def atualizarProdutos(codProduto):
    produto = Produto.query.filter_by(_codProduto=codProduto).first()

    if request.method == 'POST':
        nomeP = request.form.get('nomeProduto')
        valorP = request.form.get('valorProduto')
        qntEstoqueP = request.form.get('qntEstoque')

        if nomeP and valorP and qntEstoqueP:
            produto.nomeProduto = nomeP
            produto.valorProduto = valorP
            produto.qntEstoque = qntEstoqueP

            db.session.commit()

            return redirect(url_for('listarProdutos'))

    return render_template('produtoView/atualizarProdutos.html', produto=produto)

# ------------------------------------------------------------------- CLASSE FORNECEDOR -----------------------------------------------------


class Fornecedor(db.Model):
    # CRIAÇÃO DA TABELA DO BANCO
    __tablename = 'fornecedor'
    _codFornecedor = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    nomeFornecedor = db.Column(db.String)
    telefoneFornecedor = db.Column(db.String)
    cpf_cnpjFornecedor = db.Column(db.String)
    tipoFornecedor = db.Column(db.String)

    # CONSTRUTOR
    def _init_(self, nome, telefone, cpf, email):
        self.nomeFornecedor = nomeFornecedor
        self.telefone = telefone
        self.cpf_cnpjFornecedor = cpf_cnpjFornecedor
        self.tipoFornecedor = tipoFornecedor


# ROTA DA PAGINA USUÁRIO


@app.route('/fornecedorPage')
def fornecedorPage():
    return render_template('fornecedorView/fornecedor.html')

# ROTA DA  PAGINA DO CADASTRO


@app.route('/fornecedor/cadastrar')
def cadastrarFornecedores():
    return render_template('fornecedorView/cadastroFornecedores.html')

# ROTA DO METODO DE CADASTRAR


@app.route('/fornecedor/cadastro', methods=['GET', 'POST'])
# METODO DE CADASTRAR
def cadastroFornecedores():
    if request.method == 'POST':
        nomeFornecedor = request.form['nomeFornecedor']
        telefoneFornecedor = request.form['telefoneFornecedor']
        cpf_cnpjFornecedor = request.form['cpf_cnpjFornecedor']
        tipoFornecedor = request.form['tipoFornecedor']

        if nomeFornecedor and telefoneFornecedor and cpf_cnpjFornecedor and tipoFornecedor:
            f = Fornecedor(nomeFornecedor=nomeFornecedor, telefoneFornecedor=telefoneFornecedor,
                           cpf_cnpjFornecedor=cpf_cnpjFornecedor, tipoFornecedor=tipoFornecedor)
            db.session.add(f)
            db.session.commit()

        return redirect(url_for('fornecedorPage'))

# ROTA DA PAGINA DE LISTA


@app.route('/fornecedores')
# METODO DE LISTAR
def listarFornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedorView/listaFornecedores.html', fornecedores=fornecedores)

# excluir pelo ID


@app.route('/fornecedores/excluir/<int:codFornecedor>')
def excluirFornecedores(codFornecedor):
    fornecedor = Fornecedor.query.filter_by(
        _codFornecedor=codFornecedor).first()
    db.session.delete(fornecedor)
    db.session.commit()
    # apos excluir vai voltar para pagina de listar
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedorView/listaFornecedores.html', fornecedores=fornecedores)

# ATUALIZAR pelo ID recebendo um get do parametro e retornando um post


@app.route('/fornecedores/atualizar/<int:codFornecedor>', methods=['GET', 'POST'])
def atualizarFornecedores(codFornecedor):
    fornecedor = Fornecedor.query.filter_by(
        _codFornecedor=codFornecedor).first()

    if request.method == 'POST':
        nomeF = request.form['nomeFornecedor']
        telefoneF = request.form['telefoneFornecedor']
        cpf_cnpjF = request.form['cpf_cnpjFornecedor']
        tipoF = request.form['tipoFornecedor']

        if nomeF and telefoneF and cpf_cnpjF:
            fornecedor.nomeFornecedor = nomeF
            fornecedor.telefoneFornecedor = telefoneF
            fornecedor.cpf_cnpjFornecedor = cpf_cnpjF
            fornecedor.tipoFornecedor = tipoF

            db.session.commit()

            return redirect(url_for('listarFornecedores'))

    return render_template('fornecedorView/atualizarFornecedores.html', fornecedor=fornecedor)


# ----------------------------------------------------------------TABELA DE RELACIONAMENTO venda_produto--------------------------------------------------------------------
venda_produto = db.Table('venda_produto',
                         db.Column('codVenda', db.Integer, db.ForeignKey(
                             'venda._codVenda'), primary_key=True),
                         db.Column('codProduto', db.Integer, db.ForeignKey(
                             'produto._codProduto'), primary_key=True),
                         db.Column('qntProduto', db.Integer)
                         )
# ----------------------------------------------------------------CLASSE VENDAS--------------------------------------------------------------------


class Venda(db.Model):
    # CRIAÇÃO DA TABELA DO BANCO
    __tablename = 'venda'
    _codVenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qtd_produto = db.Column(db.Integer)
    valor_total = db.Column(db.Float)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuario.id_Usuario'))
    vender = db.relationship('Produto', secondary=venda_produto, lazy='subquery',
                             backref=db.backref('vender', lazy=True))
    # id do usuario

    # CONSTRUTOR
    def __init__(self, qtd_produto, valor_total):  # id do usuario
        self.qtd_produto = qtd_produto
        self.valor_total = valor_total
        # id do usuario


# ROTA DA PAGINA VENDAS


@app.route('/vendaPage')
def vendaPage():
    return render_template('vendaView/venda.html')

# ROTA DA  PAGINA DO CADASTRO


@app.route('/venda/cadastrar')
def cadastrarVendas():
    return render_template('vendaView/cadastroVendas.html')

# ROTA DO METODO DE CADASTRAR


@app.route('/venda/cadastro', methods=['GET', 'POST'])
# METODO DE CADASTRAR
def cadastroVendas():
    if request.method == 'POST':
        # id do usuario
        valor_total = request.form['valor_total']
        qtd_produto = request.form['qtd_produto']

        if valor_total and qtd_produto:  # and id do usuario
            v = Venda(valor_total=valor_total, qtd_produto=qtd_produto)
            db.session.add(v)
            g.user.venda_usuario.append(v)
            db.session.commit()

        return redirect(url_for('vendaPage'))

# ROTA DA PAGINA DE LISTA


@app.route('/vendas')
# METODO DE LISTAR
def listarVendas():
    vendas = Venda.query.all()
    return render_template('vendaView/listaVendas.html', vendas=vendas)

# excluir pelo ID


@app.route('/vendas/excluir/<int:codVenda>')
def excluirVendas(codVenda):
    venda = Venda.query.filter_by(_codVenda=codVenda).first()
    db.session.delete(venda)
    db.session.commit()
    # apos excluir vai voltar para pagina de listar
    vendas = Venda.query.all()
    return render_template('vendaView/listaVendas.html', vendas=vendas)

# ATUALIZAR pelo ID recebendo um get do parametro e retornando um post


# @app.route('/vendas/atualizar/<int:codVenda>', methods=['GET', 'POST'])
# def atualizarVendas(codVenda):
#     venda = Venda.query.filter_by(_codVenda=codVenda).first()

#     if request.method == 'POST':
#         valor_totalV = request.form['valor_total']
#         qtd_produtoV = request.form['qtd_produto']
#         # id do usuario
#
#        if valor_totalV and qtd_produtoV:  # and id do usuario
#            venda.valor_total = valor_totalV
#            venda.qtd_produto = qtd_produtoV
#            # and id do usuario

#            db.session.commit()

#           return redirect(url_for('listarVendas'))

#    return render_template('vendaView/atualizarVendas.html', venda=venda)


# inicia o aplicativo
db.create_all()
chave = Usuario.query.filter_by(id_Usuario=1).first()
if chave is None:
    users = Usuario('admin', 'admin', True)
    db.session.add(users)
    db.session.commit()

if __name__ == '__main__':
    app.secret_key = 'adsoadsojidasjiodasoiasf809qw123123'
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
