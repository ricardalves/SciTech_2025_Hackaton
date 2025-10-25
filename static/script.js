document.addEventListener('DOMContentLoaded', function() {
    const botaoGerar = document.getElementById('gerar-imagem');
    const containerImagem = document.getElementById('imagem-container');

    botaoGerar.addEventListener('click', function() {
        // Fazer uma requisição para a rota que gera a imagem
        fetch('/gerar_imagem')
            .then(response => response.json())
            .then(data => {
                // Criar um elemento de imagem e adicionar ao container
                const img = document.createElement('img');
                img.src = data.imagem_url;
                img.alt = 'Gráfico gerado';
                containerImagem.appendChild(img);
            })
            .catch(error => console.error('Erro:', error));
    });
});