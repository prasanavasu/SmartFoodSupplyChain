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
    `;

    // Visualization buttons
    const visualizationButtons = document.createElement('div');
    visualizationButtons.classList.add('visualization-buttons');
    visualizationButtons.innerHTML = `
        <button class="visualization-button" id="getTopSellingStock" onclick="showVisualization('getTopSellingStock')">Top Selling Stock</button>
        
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
            $(data.id).hide()
            html_data = `
            <a href="${data.imageUrl}" id="${data.id}" target="_blank" title="Visualization">
            <img src="${data.imageUrl}" alt="Visualization" class="visualization-image"id="${data.id}_img"></a>
            <p>${data.name}</p>`;
            if(data.id==='#getTopSellingStock'){
                visualizationDiv.innerHTML = html_data+ ` <button class="visualization-button" id="busiestHour" onclick="showVisualization('busiestHour')">Busiest Hour</button>`

            }else{
                visualizationDiv.innerHTML = html_data
            }
            

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

$("#getTopSellingStock").on("click", function() {
    $('#imagepreview').attr('src', $('##getTopSellingStock_img').attr('src')); // here asign the image to the modal when the user click the enlarge link
    $('#imagemodal').modal('show'); // imagemodal is the id attribute assigned to the bootstrap modal, then i use the show function
 });
 