document.addEventListener('DOMContentLoaded', () => {
  // Seus elementos HTML (estão perfeitos)
  const form = document.getElementById('chat-form');
  const input = document.getElementById('chat-input');
  const messagesContainer = document.getElementById('chat-messages');

  // URL do seu endpoint de chatbot no backend
  const apiUrl = 'http://127.0.0.1:8000/site/assistente';

  // Sua função de adicionar mensagem (está perfeita)
  function addMessage(text, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const p = document.createElement('p');
    p.textContent = text;
    
    messageDiv.appendChild(p);
    messagesContainer.appendChild(messageDiv);
    
    // Rola para a mensagem mais recente
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // --- ALTERAÇÃO PRINCIPAL AQUI ---
  // Trocamos a simulação por uma chamada real à API
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const userText = input.value.trim();

    if (userText) {
      // 1. Adiciona a mensagem do usuário na tela (seu código original)
      addMessage(userText, 'user-message');
      input.value = '';
      
      try {
        // 2. Envia a pergunta do usuário para a API
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // Envia o texto no formato JSON que o backend espera
          body: JSON.stringify({ pergunta: userText }),
        });

        if (!response.ok) {
          throw new Error(`Erro do servidor: ${response.status}`);
        }

        const botData = await response.json();
        
        // Supondo que sua IA retorne um JSON com uma chave "resposta" ou "mensagem"
        const botText = botData.resposta || botData.mensagem || "Não recebi uma resposta válida.";

        // 3. Adiciona a resposta REAL do bot na tela
        addMessage(botText, 'bot-message');

      } catch (error) {
        console.error('Erro ao conectar com a API do chatbot:', error);
        addMessage('Desculpe, estou com problemas para me conectar. Tente novamente mais tarde.', 'bot-message');
      }
    }
  });
});