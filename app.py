from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para armazenar os canhotos adicionados
canhotos = []
# Variável para manter a data padrão (primeira data a ser preenchida)
data_default = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_default

    if request.method == 'POST':
        data = request.form['data']
        quantidade = int(request.form['quantidade'])

        # Atualiza a data_default quando a data é mudada manualmente
        data_default = data

        # Adiciona o canhoto à lista
        canhotos.append({'data': data, 'quantidade': quantidade})

        return redirect(url_for('index'))

    return render_template('index.html', canhotos=canhotos, data_default=data_default)

@app.route('/excluir/<int:index>', methods=['GET'])
def excluir(index):
    # Remove o canhoto da lista pelo índice
    canhotos.pop(index)
    return redirect(url_for('index'))

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if request.method == 'POST':
        # Atualiza os dados do canhoto
        canhotos[index]['data'] = request.form['data']
        canhotos[index]['quantidade'] = int(request.form['quantidade'])
        # Atualiza a data_default quando a data for modificada no editar
        global data_default
        data_default = request.form['data']
        return redirect(url_for('index'))

    # Preenche os campos com os dados atuais do canhoto
    canhoto = canhotos[index]
    return render_template('editar.html', canhoto=canhoto, index=index)

@app.route('/calcular_total', methods=['POST'])
def calcular_total():
    total = sum(canhoto['quantidade'] for canhoto in canhotos)
    return render_template('index.html', canhotos=canhotos, total=total, data_default=data_default)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
