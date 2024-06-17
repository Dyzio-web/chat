document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    let message = document.getElementById('message').value;
    if (message.trim() !== "") {
        addMessageToChatBox(message, 'sent');
        document.getElementById('message').value = '';

        // Wysłanie wiadomości do serwera
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'message=' + encodeURIComponent(message)
        }).then(response => {
            if (response.status === 204) {
                loadMessages();
            }
        });
    }
});

function addMessageToChatBox(message, type) {
    let chatBox = document.getElementById('chat-box');
    let messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Automatyczne przewijanie na dół
}

function loadMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            let chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = '';
            data.messages.forEach(msg => {
                addMessageToChatBox(msg, 'received');
            });
        });
}

setInterval(loadMessages, 5000);  // Odświeżanie wiadomości co 5 sekund
loadMessages();