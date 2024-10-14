document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const userInput = inputField.value.trim();
    
    if (userInput) {
        displayMessage(userInput, 'user');
        inputField.value = '';
        
        // Call the API to get the response
        const response = await fetchResponse(userInput);
        displayMessage(response, 'assistant');
    }
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;

    chatBox.appendChild(messageElement);
    
    // Trigger animation
    setTimeout(() => {
        messageElement.classList.add('show');
    }, 10);
    
    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function fetchResponse(userInput) {
    try {
        const response = await fetch('http://localhost:8080/api/cashgpt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ hukum: userInput }) // Sending the user input as "hukum"
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching the response:', error);
        return 'Sorry, I could not get a response. Please try again.';
    }
}

