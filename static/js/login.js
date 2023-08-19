// Update the API URL to use the correct port
const apiBaseUrl = 'http://127.0.0.1:5000';

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = {
        username: username,
        password: password
    };

    console.log('Sending API request...');
    const response = await fetch(`${apiBaseUrl}/api/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log('API response:', result);

    if (response.ok) {
        if (result.user_type === 'customer') {
            window.location.href = '/customer_dashboard';
        }
         if (result.user_type === 'supplier') {
            window.location.href = '/supplier_dashboard';
        }
        if (result.user_type === 'distributor') {
            window.location.href = '/distributor_dashboard';
        }else {
            // Handle other user types or show an error message
        }
    } else {
        alert('Login failed. Please check your credentials.');
    }
}
