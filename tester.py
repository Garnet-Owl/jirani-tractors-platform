// Select the farmer form element by its id
const farmerForm = document.getElementById('farmer-form');
// Add an event listener to the farmer form element for the submit event
farmerForm.addEventListener('submit', (event) => {
    // Prevent the default behavior of the submit event, which is to reload the page
    event.preventDefault();
    // Get the input values from the farmer form element
    const name = farmerForm.name.value;
    const phone = farmerForm.phone.value;
    const location = farmerForm.location.value;
    const land_size = farmerForm.land_size.value;
    // Create a data object with the input values as properties
    const data = {name, phone, location, land_size};
    // Use the fetch API to send a POST request to the /farmers endpoint with the data object as the body
    fetch('/farmers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    // Use a then method to handle the response from the server
    .then(response => {
        // Check if the response status is OK (200)
        if (response.ok) {
            // Return the response as JSON
            return response.json();
        } else {
            // Throw an error with the response status text
            throw new Error(response.statusText);
        }
    })
    // Use another then method to handle the JSON data from the response
    .then(data => {
        // Use an alert function to display the message from the data
        alert(data.message);
        // Reset the farmer form element
        farmerForm.reset();
    })
    // Use a catch method to handle any errors from the fetch API or the then methods
    .catch(error => {
        // Use an alert function to display the error message
        alert(error.message);
    });
});

// Repeat the same steps for the tractor owner form element and the match form element, using their respective ids and endpoints

// Select the tractor owner form element by its id
const tractorOwnerForm = document.getElementById('tractor-owner-form');
// Add an event listener to the tractor owner form element for the submit event
tractorOwnerForm.addEventListener('submit', (event) => {
    // Prevent the default behavior of the submit event, which is to reload the page
    event.preventDefault();
    // Get the input values from the tractor owner form element
    const name = tractorOwnerForm.name.value;
    const phone = tractorOwnerForm.phone.value;
    const location = tractorOwnerForm.location.value;
    const tractor_type = tractorOwnerForm.tractor_type.value;
    // Create a data object with the input values as properties
    const data = {name, phone, location, tractor_type};
    // Use the fetch API to send a POST request to the /tractor_owners endpoint with the data object as the body
    fetch('/tractor_owners', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
