document.addEventListener('DOMContentLoaded', function() {
    const inStockTable = document.getElementById('in-stock-product-table');
    const outOfStockTable = document.getElementById('out-of-stock-product-table');

     // Initialize productSelect and hubSelect
    const productSelect = document.getElementById('product-select');
    const hubSelect = document.getElementById('hub-select');

    // Function to populate a table with products
    function populateTable(tableElement, products) {
        products.forEach(product => {
            const row = document.createElement('tr');
            const productCell = document.createElement('td');
            const quantityCell = document.createElement('td');
            const statusCell = document.createElement('td');

            productCell.textContent = product.product_name;
            quantityCell.textContent = product.quantity;
            statusCell.textContent = product.status;

            row.appendChild(productCell);
            row.appendChild(quantityCell);
            row.appendChild(statusCell);
            tableElement.appendChild(row);
        });
    }

    // Fetch product data from the API
    fetch('/api/checkproductstock')
        .then(response => response.json())
        .then(data => {
            const inStockProducts = data.products.filter(product => product.status === 'In Stock');
            const outOfStockProducts = data.products.filter(product => product.status === 'Out of Stock');

            // Populate the In Stock Products table
            populateTable(inStockTable, inStockProducts);

            // Populate the Out of Stock Products table
            populateTable(outOfStockTable, outOfStockProducts);

            // Populate the product select options
            outOfStockProducts.forEach(product => {
                const productOption = document.createElement('option');
                productOption.value = product.product_name;
                productOption.textContent = product.product_name;
                productSelect.appendChild(productOption);
            });

            // Demo hub values
            const demoHubs = ['Hub A', 'Hub B', 'Hub C'];
            // Populate the hub select options (if you have 'hubs' data)
            demoHubs.forEach(hub => {
                const hubOption = document.createElement('option');
                hubOption.value = hub;
                hubOption.textContent = hub;
                hubSelect.appendChild(hubOption);
            });
        });


    const requestForm = document.getElementById('request-form');
    requestForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const productSelect = document.getElementById('product-select');
        const selectedProduct = productSelect.value;

        const hubSelect = document.getElementById('hub-select');
        const selectedHub = hubSelect.value;

        // Prepare the data to send
        const requestData = {
            product: selectedProduct,
            hub: selectedHub
        };


       fetch('/api/send_request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            alert('Request sent successfully!');
            // You can update the UI or perform other actions here
        })
        .catch(error => {
            console.error('Error sending request:', error);
            alert('Error sending request. Please try again.');
        });
    });
});
