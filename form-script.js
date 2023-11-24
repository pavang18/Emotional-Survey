document.getElementById('myForm').addEventListener('submit', function(event) {
    // alert("Audio added");
    event.preventDefault(); // Prevent form submission from reloading the page

    const form = event.target;
    const formData = new FormData(form);

    // Capture the audio files and append them to the FormData
    const audioFiles = document.querySelectorAll('input[type="file"]');
    audioFiles.forEach(fileInput => {
        const file = fileInput.files[0];
        formData.append(fileInput.name, file);
    });
    // alert("Audio added");

    // Make an HTTP POST request to the Flask backend
    fetch('/submit-data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(responseText => {
        console.log(responseText); // Log the response from Flask (optional)
        // Add any additional logic or UI updates as needed after the response
    })
    .catch(error => {
        console.error('Error sending data to Flask:', error);
        // Handle any error that occurs during the request
    });
});
