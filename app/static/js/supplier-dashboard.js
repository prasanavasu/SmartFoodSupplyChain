document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const inboxList = document.getElementById('inbox-list');
    const productRequestTable = document.getElementById('product-request-table');

    // Simulated inbox messages
    const inboxMessages = [
        'Pending request: Product A',
        'Pending request: Product B',
        'Approval required: Product C',
    ];

    // Simulated product requests
    const productRequests = [
        { product: 'Product A', quantity: 50, address: '123 Main St.', status: 'Pending' },
        { product: 'Product B', quantity: 30, address: '456 Elm St.', status: 'Pending' },
        { product: 'Product C', quantity: 70, address: '789 Oak St.', status: 'Approval Required' },
    ];

    // Populate inbox messages
    inboxMessages.forEach(message => {
        const listItem = document.createElement('li');
        listItem.textContent = message;
        inboxList.appendChild(listItem);
    });

    // Populate product request table
    productRequests.forEach(request => {
        const row = document.createElement('tr');
        const productCell = document.createElement('td');
        const quantityCell = document.createElement('td');
        const addressCell = document.createElement('td');
        const statusCell = document.createElement('td');

        productCell.textContent = request.product;
        quantityCell.textContent = request.quantity;
        addressCell.textContent = request.address;
        statusCell.textContent = request.status;

        row.appendChild(productCell);
        row.appendChild(quantityCell);
        row.appendChild(addressCell);
        row.appendChild(statusCell);
        productRequestTable.appendChild(row);
    });

    // Set the username dynamically
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');
    usernameElement.textContent = username;
});
