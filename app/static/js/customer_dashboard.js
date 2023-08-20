// Update the API URL to use the correct port

document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const productTable = document.getElementById('product-table');
    const welcomeMessage = document.getElementById('welcome-message');
    const chatbotInterface = document.getElementById('chatbot-interface'); // Update this line
    const visualizationContainer = document.getElementById('visualization-container'); // Add this line


    // Static chatbot messages
    chatbotInterface.innerHTML = `
        <div class="chat-message">I am Infinity Virtual Assistant</div>
        <div class="chat-message">Glad you're here!</div>
        <div class="chat-message">I'm here to assist you.</div>
    `;

    // Visualization buttons
    const visualizationButtons = document.createElement('div');
    visualizationButtons.classList.add('visualization-buttons');
    visualizationButtons.innerHTML = `
        <button class="visualization-button" id="selling_stock" onclick="showVisualization('getTopSellingStock')">Top Selling Stock</button>
        <button class="visualization-button"id="busiest_hour" onclick="showVisualization('busiestHour')">Busiest Hour</button>
    `;
    chatbotInterface.appendChild(visualizationButtons);

});

// Function to toggle the chatbot interface
function toggleChatbot() {
    const chatbotInterface = document.getElementById('chatbot-interface');
    chatbotInterface.classList.toggle('show');
    chatbotInterface.style.display = chatbotInterface.classList.contains('show') ? 'block' : 'none';
}

// Function to show visualization

function showVisualization(buttonId) {
    console.log(`Button ${buttonId} clicked`);

    // Disable only the clicked button
    const clickedButton = document.getElementById(`visualization-button-${buttonId}`);
    if (clickedButton) {
        clickedButton.disabled = true;
    }

    // Fetch the visualization data
    fetch(`/api/visualizations/${buttonId}`)
        .then(response => response.json())
        .then(data => {
            const chatbotInterface = document.getElementById('chatbot-interface');

            // Create a div to hold the visualization image
            const visualizationDiv = document.createElement('div');
            visualizationDiv.classList.add('visualization-container');
            visualizationDiv.innerHTML = `
                <img src="${data.imageUrl}" alt="Visualization" class="visualization-image">
            `;

            // Append the visualization div to the chatbot interface
            chatbotInterface.appendChild(visualizationDiv);

            // Scroll the chatbot interface to the bottom to show the visualization
            chatbotInterface.scrollTop = chatbotInterface.scrollHeight;

            // Keep the chatbot open without toggling it
            chatbotInterface.style.display = 'block';
        })
        .catch(error => {
            console.error('Error fetching visualization data:', error);
        });
}
