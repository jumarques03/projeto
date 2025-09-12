// script/inversor.js

document.addEventListener('DOMContentLoaded', () => {
    const baseUrl = 'https://api-smartsolargrid.onrender.com/site';

    const carregarStatusInversor = async () => {
        try {
            const response = await fetch(`${baseUrl}/status_aparelhos`);
            if (!response.ok) {
                throw new Error('Falha ao buscar os dados do inversor.');
            }
            const data = await response.json();

            // Pega cada elemento pelo ID que definimos no HTML
            const statusEl = document.getElementById('status-inversor');
            const bateriaEl = document.getElementById('status-bateria');
            const solarEl = document.getElementById('status-solar');
            const consumoEl = document.getElementById('status-consumo');

            // Atualiza o texto de cada elemento com os dados da API
            if (data) {
                statusEl.textContent = data.inversor_status;
                bateriaEl.textContent = data.bateria_carga;
                solarEl.textContent = `${data.producao_solar_watts} W`;
                consumoEl.textContent = `${data.consumo_casa_watts} W`;
            }

        } catch (error) {
            console.error("Erro ao carregar status do inversor:", error);
            // Coloca uma mensagem de erro nos cards se a API falhar
            document.getElementById('status-inversor').textContent = "Erro";
            document.getElementById('status-bateria').textContent = "Erro";
            document.getElementById('status-solar').textContent = "Erro";
            document.getElementById('status-consumo').textContent = "Erro";
        }
    };

    // Chama a função para carregar os dados assim que a página estiver pronta
    carregarStatusInversor();

    // Opcional: Recarregar os dados a cada 10 segundos
    setInterval(carregarStatusInversor, 10000); 
});