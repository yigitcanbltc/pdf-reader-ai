function toggleChat() {
    const chatBox = document.getElementById('chatBox');
    if (chatBox.style.display === 'block') {
        chatBox.style.display = 'none';
    } else {
        chatBox.style.display = 'block';
    }
}

function sendMessage(event) {
    if (event && event.key !== 'Enter' && event.type !== 'click') return;

    const userInput = document.getElementById('userInput').value;
    if (userInput.trim()) {
        const chatContent = document.getElementById('chatContent');

        // Kullanıcı mesajını ekleyelim
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user');
        userMessage.innerHTML = `
            <i class="fas fa-user message-icon"></i>
            <div class="message-text">${userInput}</div>
        `;
        chatContent.appendChild(userMessage);

        // Backend'e istekte bulun
        fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userInput }),
        })
            .then(response => response.json())
            .then(data => {
                // Backend'den gelen yanıtı ekle
                const robotMessage = document.createElement('div');
                robotMessage.classList.add('message', 'robot');
                robotMessage.innerHTML = `
                    <i class="fas fa-robot message-icon"></i>
                    <div class="message-text">${data.answer}</div>
                `;
                chatContent.appendChild(robotMessage);

                // Sohbet içeriğini en alta kaydır
                chatContent.scrollTop = chatContent.scrollHeight;
            })
            .catch(error => {
                console.error('Hata:', error);
            });

        // Input'u sıfırla
        document.getElementById('userInput').value = '';
    }
}