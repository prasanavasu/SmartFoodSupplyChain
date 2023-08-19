

function hub_change(){
    var product = $('#product_select').val()
    if (product){
        fetch(`/find_hub/${product}`)
        .then(response => response.json())
        .then(data => {
//            usernameElement.textContent = `Welcome, ${data.username}!`;
        $('#hub_select').empty()
            // Clear existing table rows   
            $('#hub_select').append(`<option value="">Select</option>`); 
            data.hubs.forEach(function(item) {
                $('#hub_select').append(`<option value="${item}">${item}</option>`);
            });
           
        });
}
    }
    