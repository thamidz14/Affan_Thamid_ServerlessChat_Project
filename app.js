const apiUrl = 'https://pa4fj5qvvi.execute-api.us-east-1.amazonaws.com/chat';

async function postMessage() {
    try {
        const message = document.getElementById('messageInput').value;
        if (!message.trim()) {
            console.error('Message cannot be empty');
            return;
        }

        const username = 'bigbrodie94'; // You might want to add a username input field
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": username,
                "message": message
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData);
            return;
        }
        
        const data = await response.json();
        console.log('Message posted:', data);
        document.getElementById('messageInput').value = ''; // Clear input after successful post
        await getMessages();
    } catch (error) {
        console.error('Error posting message:', error);
    }
}

async function getMessages() {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error:', errorData);
            return;
        }

        const data = await response.json();
        const messages = data.messages || [];
        const chatDiv = document.getElementById('chat');
        chatDiv.innerHTML = '';
        
        messages.sort((a, b) => a.Timestamp - b.Timestamp).forEach(msg => {
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message';
            msgDiv.textContent = `${msg.Username}: ${msg.Message}`;
            chatDiv.appendChild(msgDiv);
        });

        chatDiv.scrollTop = chatDiv.scrollHeight; // Auto-scroll to bottom
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

// Add event listener for Enter key in message input
document.getElementById('messageInput')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        postMessage();
    }
});

// Initial load of messages
getMessages();

// Refresh messages periodically
setInterval(getMessages, 5000);
