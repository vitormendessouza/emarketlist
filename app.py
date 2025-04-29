from flask import Flask, render_template, request, redirect, url_for
from model import db, Item
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    itens = Item.query.all()
    return render_template('index.html', itens=itens)

@app.route('/add', methods=['POST'])
def add():
    nome = request.form.get('nome')
    if nome:
        novo_item = Item(nome=nome)
        db.session.add(novo_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/comprar/<int:id>')
def comprar(id):
    item = Item.query.get(id)
    if item:
        item.comprado = not item.comprado
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/remover/<int:id>')
def remover(id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
