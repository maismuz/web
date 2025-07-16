from flask import Flask
app = Flask(__name__)
@app.route('/')
def ola_mundo():
    return'ola mundo'
@app.route('/perfil/<nome>')
def perfil(nome):
  return f'<h1>Olá, {nome}!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
