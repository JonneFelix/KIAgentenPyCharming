// Wait for the entire DOM to load before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const sendButton = document.getElementById('send-button');
    const chatInput = document.getElementById('chat-input');
    const chatWindow = document.getElementById('chat-window');
    const modelSelect = document.getElementById('model-select');
    const pdfDisplay = document.getElementById('pdf-display');

    // Define a list of greetings for the bot to use
    const greetings = [
        "Hello! How can I help you with your PDF?",
        "Welcome! What would you like to know about your PDF?",
        "Hi! How can I assist you with your PDF?",
        "Good day. What can I do for you regarding your PDF?",
    ];

    // Parse URL parameters to get the PDF filename
    const urlParams = new URLSearchParams(window.location.search);
    const pdfFilename = urlParams.get('pdf');
    // Get the PDF text data from the dataset attribute of the PDF display element
    const pdfText = pdfDisplay.dataset.pdfText;

    // If a PDF filename is provided in the URL
    if (pdfFilename) {
        // Create an iframe to display the PDF
        const iframe = document.createElement('iframe');
        iframe.src = `/uploads/${pdfFilename}`;
        iframe.classList.add('w-100', 'h-100');
        pdfDisplay.innerHTML = '';
        pdfDisplay.appendChild(iframe);

        // Select a random greeting and display it in the chat window
        const randomGreeting = greetings[Math.floor(Math.random() * greetings.length)];
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        botMessageElement.innerHTML = `<img src="/static/images/Chat-bot-profilbild.jpg" alt="Bot" class="profile-pic"> <div>${randomGreeting}</div>`;
        chatWindow.appendChild(botMessageElement);
        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to send a message
    const sendMessage = async () => {
        const message = chatInput.value;
        const model = modelSelect.value;
        // Check if the message is not empty
        if (message.trim() !== '') {
            // Create a new message element for the user
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', 'user-message');
            messageElement.innerHTML = `<img src="/static/images/User_1.png" alt="User" class="profile-pic"> <div>${message}</div>`;
            chatWindow.appendChild(messageElement);
            // Clear the chat input field
            chatInput.value = '';
            // Scroll to the bottom of the chat window
            chatWindow.scrollTop = chatWindow.scrollHeight;

            // Send the message to the server and get the response
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message, model: model, pdf_text: pdfText })
            });
            const data = await response.json();
            const botMessage = data.choices[0].message.content;

            // Create a new message element for the bot response
            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('message', 'bot-message');
            botMessageElement.innerHTML = `<img src="/static/images/Chat-bot-profilbild.jpg" alt="Bot" class="profile-pic"> <div>${botMessage}</div>`;
            chatWindow.appendChild(botMessageElement);
            // Scroll to the bottom of the chat window
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    };

    // Add an event listener to the send button to send the message when clicked
    sendButton.addEventListener('click', sendMessage);
    // Add an event listener to the chat input to send the message when Enter key is pressed
    chatInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});