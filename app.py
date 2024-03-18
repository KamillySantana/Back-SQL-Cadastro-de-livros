from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/livros'
app.config['SECRET_KEY'] = 'ASDFGHJKL'
db = SQLAlchemy(app)


class Livro(db.Model):
    id_livros = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(254))
    ano_publicado = db.Column(db.Integer)

@app.route('/')
def index():
    livros = Livro.query.all()
    return render_template('cadastro_livros.html', outro=livros)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicado = request.form['ano_publicado']

    livro = Livro.query.filter_by(titulo=titulo).first()
    if livro:
        flash("Livro já existente!")
        return redirect(url_for('novo'))

    novo_livro = Livro(titulo=titulo, autor=autor, ano_publicado=ano_publicado)
    db.session.add(novo_livro)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    livro = Livro.query.filter_by(id_livros=id).first()
    return render_template('editar.html', titulo='Editando Livro', livro=livro)

@app.route('/atualizar', methods=['POST'])
def atualizar():
   livro = Livro.query.filter_by(id_livros=request.form['id']).first()
   livro.titulo = request.form['titulo']
   livro.autor = request.form['autor']
   livro.ano_publicado = request.form['ano_publicado']


   db.session.add(livro)
   db.session.commit()

   return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    Livro.query.filter_by(id_livros=id).delete()
    db.session.commit()
    flash('Livro excluido com sucesso.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)