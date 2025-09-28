document.addEventListener('DOMContentLoaded', () => {
    // --- ELEMENTOS DO DOM ---
    const form = document.getElementById('add-load-form');
    const input = document.getElementById('load-input');
    const list = document.getElementById('load-list');
    
    const statusList = document.getElementById('status-list');
    const batteryForecast = document.getElementById('battery-forecast');

    const baseUrl = 'https://smartsolargrid.onrender.com/site';

    // --- FUNÇÕES DA API (GERENCIADOR DE CARGAS) ---

    const carregarCargas = async () => {
        try {
            const response = await fetch(`${baseUrl}/lista_cargas_prioritarias`);
            if (!response.ok) throw new Error('Não foi possível carregar a lista.');
            const data = await response.json();
            
            list.innerHTML = '';
            for (const id in data.cargas_prioritarias) {
                const nomeDaCarga = data.cargas_prioritarias[id];
                addLoadItemToScreen(nomeDaCarga, id);
            }
        } catch (error) {
            console.error("Erro ao carregar cargas:", error);
            list.innerHTML = '<li>Falha ao carregar a lista.</li>';
        }
    };

    const adicionarCarga = async (nomeDaCarga) => {
        try {
            const response = await fetch(`${baseUrl}/escolher_cargas_prioritarias`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dispositivo: nomeDaCarga })
            });
            if (!response.ok) throw new Error('Falha ao adicionar a carga.');
            carregarCargas();
        } catch (error) {
            console.error("Erro ao adicionar carga:", error);
            alert("Não foi possível adicionar a nova carga.");
        }
    };

    const removerCarga = async (idDaCarga) => {
        try {
            const response = await fetch(`${baseUrl}/remover_carga_prioritaria?carga_id=${idDaCarga}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Falha ao remover a carga.');
        } catch (error) {
            console.error("Erro ao remover carga:", error);
            alert("Não foi possível remover a carga.");
        }
    };

    // --- FUNÇÕES DA API (NOVOS WIDGETS) ---

    const carregarStatusCargas = async () => {
        try {
            const response = await fetch(`${baseUrl}/consumo_aparelhos`); 
            if (!response.ok) throw new Error('Não foi possível carregar o status.');
            const data = await response.json();
            
            statusList.innerHTML = '';

            const aparelhos = data.consumo_de_cada_aparelho;
            if (aparelhos && Object.keys(aparelhos).length > 0) {
                 for (const nomeAparelho in aparelhos) {
                    const consumo = aparelhos[nomeAparelho];
                    const li = document.createElement('li');
                    const nomeLimpo = nomeAparelho.replace('Consumo ', '');

                    li.innerHTML = `
                        <span>
                            <span class="status-indicator"></span>
                            ${nomeLimpo}
                        </span>
                        <span class="consumption-value">${consumo}W</span>
                    `;
                    statusList.appendChild(li);
                }
            } else {
                 statusList.innerHTML = '<p>Nenhuma carga prioritária ativa no momento.</p>';
            }
        } catch (error) {
            console.error("Erro ao carregar status das cargas:", error);
            statusList.innerHTML = '<p>Não foi possível carregar o status.</p>';
        }
    };

    const carregarPrevisaoBateria = async () => {
        try {
            // *** CORREÇÃO APLICADA AQUI ***
            // Ajustado o nome do endpoint para bater com o seu arquivo de rotas.
            const response = await fetch(`${baseUrl}/informacoes_consumo`);
            if (!response.ok) throw new Error('Não foi possível carregar a previsão.');
            const data = await response.json();

            batteryForecast.textContent = data.duracao || 'Informação indisponível.';
        } catch (error) {
            console.error("Erro ao carregar previsão da bateria:", error);
            batteryForecast.textContent = 'Falha ao carregar a previsão.';
        }
    };

    // --- FUNÇÃO AUXILIAR PARA MANIPULAR O HTML ---
    function addLoadItemToScreen(loadName, id) {
        const li = document.createElement('li');
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
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const newLoadName = input.value.trim();
        if (newLoadName) {
            adicionarCarga(newLoadName);
            input.value = '';
            input.focus();
        }
    });
    
    list.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const listItem = event.target.parentElement;
            const idParaRemover = listItem.getAttribute('data-id');
            if (idParaRemover) {
                removerCarga(idParaRemover);
                listItem.remove();
            }
        }
    });

    // --- INICIALIZAÇÃO E ATUALIZAÇÃO AUTOMÁTICA ---
    function inicializarEAtualizar() {
        carregarCargas();
        carregarStatusCargas();
        carregarPrevisaoBateria();
    }

    inicializarEAtualizar();
});