// Update the API URL to use the correct port
const apiBaseUrl = 'http://127.0.0.1:5000';

async function login() {
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;

    const data = {
        phone: phone,
        password: password
    };

    console.log('Sending API request...');
    const response = await fetch(`/api/login`, {
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
            window.location.href = '/customer';
        }
         if (result.user_type === 'supplier') {
            window.location.href = '/supplier';
        }
        if (result.user_type === 'distributor') {
            window.location.href = '/distributor';
        }else {
            // Handle other user types or show an error message
        }
    } else {
        alert('Login failed. Please check your credentials.');
    }
}
