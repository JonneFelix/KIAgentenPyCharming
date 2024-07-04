// Wait for the entire DOM to load before running the script
document.addEventListener('DOMContentLoaded', () => {

     // Get references to DOM elements
    const pdfUpload = document.getElementById('pdf-upload');
    const proceedButton = document.getElementById('proceed-button');

    // Initially disable the proceed button
    proceedButton.disabled = true;
    proceedButton.classList.add('disabled');

     // Add an event listener to the PDF upload input
    pdfUpload.addEventListener('change', (event) => {
        // Get the selected file and check if it is a PDF
        const file = event.target.files[0];
        if (file && file.type === 'application/pdf') {
            const formData = new FormData();

            // Get the selected chunk size from the dropdown menu
            var selectElement = document.getElementById('chunk-size');
            var chunk_size = selectElement.value;
            console.log(chunk_size);

            // Append the file and chunk size information to the FormData object
            formData.append('file', file);
            formData.append('chunk_size', chunk_size);

             // Send the FormData object to the server via a POST request
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server error: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.filename) {
                    proceedButton.dataset.filename = data.filename;
                    proceedButton.disabled = false;
                    proceedButton.classList.remove('disabled');
                    proceedButton.classList.add('shake-animation');
                    setTimeout(() => {
                        proceedButton.classList.remove('shake-animation');
                    }, 1000);
                } else {
                    alert('File upload failed');
                }
            })
            .catch(error => {
                console.error('Error uploading file:', error);
                alert('An error occurred while uploading the file.');
            });
        } else {
            alert('Please upload a valid PDF file.');
        }
    });

    // Add an event listener to the proceed button for the click event
    proceedButton.addEventListener('click', () => {
        const filename = proceedButton.dataset.filename;
        if (filename) {
            window.location.href = `/chat?pdf=${encodeURIComponent(filename)}`;
        }
    });
});