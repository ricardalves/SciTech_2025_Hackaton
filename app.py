from flask import Flask, render_template, jsonify, send_file
import os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

# Pasta para imagens geradas
GENERATED_IMAGE_FOLDER = 'static/generated'
if not os.path.exists(GENERATED_IMAGE_FOLDER):
    os.makedirs(GENERATED_IMAGE_FOLDER)

# Função exemplo que gera um gráfico e salva como imagem
def gerar_grafico(nome_arquivo):
    # Dados exemplo
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title('Gráfico de Seno')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Salvar a imagem
    caminho = os.path.join(GENERATED_IMAGE_FOLDER, nome_arquivo)
    plt.savefig(caminho)
    plt.close()
    
    return caminho

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerar uma nova imagem
@app.route('/gerar_imagem')
def gerar_imagem():
    # Gera um nome único para a imagem
    nome_arquivo = f"grafico_{np.random.randint(1000)}.png"
    caminho_imagem = gerar_grafico(nome_arquivo)
    
    # Retorna o caminho relativo para a imagem
    return jsonify({'imagem_url': f'/static/generated/{nome_arquivo}'})

if __name__ == '__main__':
    app.run(debug=True)