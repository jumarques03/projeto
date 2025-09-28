// frontend/script/dashboard.js (VERSÃO COMPLETA)

document.addEventListener('DOMContentLoaded', () => {
    const baseUrl = 'https://smartsolargrid.onrender.com/site';

    // =======================================================
    // LÓGICA DO STATUS ATUAL (BATERIA, ETC.)
    // =======================================================
    const carregarStatusAtual = async () => {
        try {
            const response = await fetch(`${baseUrl}/status_aparelhos`);
            if (!response.ok) {
                throw new Error('Falha ao buscar status dos aparelhos.');
            }
            const data = await response.json();

            const elementoSoc = document.getElementById('status-soc-valor');
            if (elementoSoc && data && data.bateria_carga) {
                elementoSoc.textContent = data.bateria_carga;
            }
        } catch (error) {
            console.error("Erro ao carregar status atual:", error);
            const elementoSoc = document.getElementById('status-soc-valor');
            if(elementoSoc) elementoSoc.textContent = "Erro";
        }
    };

    // =======================================================
    // LÓGICA DOS GRÁFICOS
    // =======================================================
    const fetchChartData = async (endpoint) => {
        try {
            const response = await fetch(`${baseUrl}${endpoint}`);
            if (!response.ok) {
                console.error(`Erro ao buscar ${endpoint}: ${response.statusText}`);
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error(`Falha na conexão para ${endpoint}:`, error);
            return null;
        }
    };

    const renderChart = (canvasId, chartData) => {
        const canvasElement = document.getElementById(canvasId);
        if (!canvasElement || !chartData) {
            console.error(`Canvas com id "${canvasId}" ou dados do gráfico não encontrados.`);
            return;
        }

        const ctx = canvasElement.getContext('2d');
        new Chart(ctx, {
            type: chartData.type,
            data: chartData.data,
            options: chartData.options
        });
    };
    
    const carregarTodosOsGraficos = async () => {
        const graficosParaCarregar = [
            { id: 'graficoGeracaoSolar', endpoint: '/geracao_solar' },
            { id: 'graficoEnergiaConcessionaria', endpoint: '/energia_consumida_concessionaria' },
            { id: 'graficoCargaConsumida', endpoint: '/carga_consumida' },
            { id: 'graficoDadosBateria', endpoint: '/dados_bateria' },
            { id: 'graficoNivelBateria', endpoint: '/nivel_bateria' }
        ];

        for (const grafico of graficosParaCarregar) {
            const dadosDoGrafico = await fetchChartData(grafico.endpoint);
            if (dadosDoGrafico) {
                renderChart(grafico.id, dadosDoGrafico);
            }
        }
    };

    // =======================================================
    // LÓGICA DO CLIMA
    // =======================================================
    const carregarClima = async () => {
        const cidade = "São Paulo,SP";

        try {
            const response = await fetch(`${baseUrl}/clima?local=${encodeURIComponent(cidade)}`);
            if (!response.ok) {
                throw new Error('Não foi possível buscar os dados do clima.');
            }
            const data = await response.json();

            document.getElementById('clima-localizacao').textContent = `${data.localizacao} (${data.dia})`;
            document.getElementById('clima-descricao').textContent = data.descricao;
            document.getElementById('clima-temp-max').innerHTML = `<strong>Max:</strong> ${data.temperatura_maxima}`;
            document.getElementById('clima-temp-min').innerHTML = `<strong>Min:</strong> ${data.temperatura_minima}`;
            document.getElementById('clima-chuva').innerHTML = `<strong>Chuva:</strong> ${data['chance_de_chuva(%)']}`;

            const previsaoContainer = document.getElementById('clima-previsao');
            previsaoContainer.innerHTML = ''; 

            if (data.previsao_proximos_dias && data.previsao_proximos_dias.length > 0) {
                data.previsao_proximos_dias.slice(0, 3).forEach(dia => {
                    const diaElemento = document.createElement('div');
                    diaElemento.className = 'forecast-day';
                    diaElemento.innerHTML = `<p class="day-name">${dia.dia_semana}</p><p>${dia.max} / ${dia.min}</p>`;
                    previsaoContainer.appendChild(diaElemento);
                });
            }

        } catch (error) {
            console.error("Erro ao carregar clima:", error);
            document.getElementById('clima-localizacao').textContent = "Erro de Clima";
        }
    };

    // =======================================================
    // INICIALIZAÇÃO DO DASHBOARD
    // =======================================================
    const iniciarDashboard = () => {
        carregarStatusAtual();
        carregarTodosOsGraficos();
        carregarClima();
    };

    iniciarDashboard();
});