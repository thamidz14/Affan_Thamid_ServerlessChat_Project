const apiUrl = 'https://pa4fj5qvvi.execute-api.us-east-1.amazonaws.com/test/chat';

async function postMessage() {
    const message = document.getElementById('messageInput').value;
    const response = await fetch({apiUrl}, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: ({
            "description": message
        })
    });
    const data = await response.json();
    console.log(apiUrl)
    console.log('Message posted:', data);
    getMessages();
}

async function getMessages() {
    const response = await fetch({apiUrl});
    const messages = await response.json();
    const chatDiv = document.getElementById('chat');
    chatDiv.innerHTML = '';
    messages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.textContent = `${msg.Timestamp}: ${msg.Message}`;
        chatDiv.appendChild(msgDiv);
    });
}

getMessages();
