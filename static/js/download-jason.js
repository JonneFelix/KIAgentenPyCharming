// Wait for the entire DOM to load before running the script
document.addEventListener('DOMContentLoaded', () => {
    // Get reference to the download button
    const downloadButton = document.getElementById('download-button');

    // Add an event listener to the download button for the click event
    downloadButton.addEventListener('click', () => {
        const urlParams = new URLSearchParams(window.location.search);
        const pdfFilename = urlParams.get('pdf');
        
        // Check if a PDF filename is provided in the URL
        if (pdfFilename) {
            // Redirect the user to the download endpoint with the PDF filename as a query parameter
            window.location.href = `/download-json?pdf=${encodeURIComponent(pdfFilename)}`;
        } else {
            // Alert the user if no PDF file is specified in the URL
            alert('No PDF file specified.');
        }
    });
});