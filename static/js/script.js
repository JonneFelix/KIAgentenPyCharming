// Wait for the entire DOM to load before running the script
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('[data-collapse-toggle="mobile-menu"]');
    const menu = document.querySelector('#mobile-menu');
    // toggle if the button is hidden
    toggleButton.addEventListener('click', () => {
        if (menu.classList.contains('hidden')) {
            menu.classList.remove('hidden');
        } else {
            menu.classList.add('hidden');
        }
    });
// get references to DOM elements
    const proceedButton = document.getElementById('proceed-button');
    const landingPage = document.getElementById('landing-page');
    const mainInterface = document.getElementById('main-interface');

    // Add event to the procceed button
    proceedButton.addEventListener('click', () => {
        landingPage.classList.add('hidden');
        mainInterface.classList.remove('hidden');
    });
});