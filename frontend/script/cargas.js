// script/cargas.js

document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURAÇÃO ---
    const form = document.getElementById('add-load-form');
    const input = document.getElementById('load-input');
    const list = document.getElementById('load-list');
    const baseUrl = 'http://127.0.0.1:8000/site'; // URL base da sua API

    // --- FUNÇÕES DA API ---

    // 1. GET: Busca a lista de cargas no backend e exibe na tela
    const carregarCargas = async () => {
        try {
            const response = await fetch(`${baseUrl}/lista_cargas_prioritarias`);
            if (!response.ok) {
                throw new Error('Não foi possível carregar a lista.');
            }
            const data = await response.json();
            
            list.innerHTML = ''; // Limpa a lista antes de adicionar os itens atualizados

            // Transforma o objeto de cargas em itens da lista
            for (const id in data.cargas_prioritarias) {
                const nomeDaCarga = data.cargas_prioritarias[id];
                addLoadItemToScreen(nomeDaCarga, id); // Usa a função auxiliar para criar o <li>
            }
        } catch (error) {
            console.error("Erro ao carregar cargas:", error);
            alert("Não foi possível carregar a lista de cargas.");
        }
    };

    // 2. POST: Adiciona uma nova carga no backend
const adicionarCarga = async (nomeDaCarga) => {
    try {
        const response = await fetch(`${baseUrl}/escolher_cargas_prioritarias`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            // A CORREÇÃO ESTÁ AQUI:
            // Empacotamos a string dentro de um objeto com a chave "dispositivo"
            body: JSON.stringify({ dispositivo: nomeDaCarga }) 
        });
        
        if (!response.ok) {
            // Lança um erro se a resposta não for 2xx
            throw new Error('Falha ao adicionar a carga.');
        }

        // Se a API adicionou com sucesso, recarregamos a lista inteira
        carregarCargas();

    } catch (error) {
        console.error("Erro ao adicionar carga:", error);
        alert("Não foi possível adicionar a nova carga. Verifique o console para mais detalhes.");
    }
};

    // 3. DELETE: Remove uma carga do backend
    const removerCarga = async (idDaCarga) => {
        try {
            const response = await fetch(`${baseUrl}/remover_carga_prioritaria?carga_id=${idDaCarga}`, {
                method: 'DELETE'
            });
            if (!response.ok) {
                throw new Error('Falha ao remover a carga.');
            }
            // Não precisamos recarregar a lista inteira, podemos só remover o item da tela.
            // Opcional: recarregar com carregarCargas() para reordenar os números.
        } catch (error) {
            console.error("Erro ao remover carga:", error);
            alert("Não foi possível remover a carga.");
        }
    };

    // --- FUNÇÃO AUXILIAR PARA MANIPULAR O HTML ---

    // Esta função apenas cria os elementos na tela.
    // Adicionamos o 'id' para saber quem deletar depois.
    function addLoadItemToScreen(loadName, id) {
        const li = document.createElement('li');
        // PONTO-CHAVE: Armazenamos o ID do banco de dados no próprio elemento!
        li.setAttribute('data-id', id);

        const textNode = document.createTextNode(loadName);
        
        const deleteButton = document.createElement('button');
        deleteButton.className = 'delete-btn';
        deleteButton.innerHTML = '&times;';

        li.appendChild(textNode);
        li.appendChild(deleteButton);
        list.appendChild(li);
    }

    // --- EVENTOS ---

    // Evento de envio do formulário (ADICIONAR)
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const newLoadName = input.value.trim();
        if (newLoadName) {
            adicionarCarga(newLoadName); // Chama a função da API
            input.value = '';
            input.focus();
        }
    });

    // Evento de clique na lista (REMOVER)
    list.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const listItem = event.target.parentElement;
            const idParaRemover = listItem.getAttribute('data-id'); // Pega o ID que guardamos

            if (idParaRemover) {
                removerCarga(idParaRemover); // Chama a função da API
                listItem.remove(); // Remove o item da tela imediatamente para melhor UX
            }
        }
    });

    // --- INICIALIZAÇÃO ---
    // Assim que a página carrega, busca a lista inicial de cargas.
    carregarCargas();
});