async function startExperience() {
    const button = document.getElementById('startButton');
    const errorMessage = document.getElementById('errorMessage');
    
    try {
        // Disable button while processing
        button.disabled = true;
        button.classList.add('button-disabled');
        errorMessage.classList.add('hidden');

        // Call the face detection script
        const response = await fetch('/run-face');
        const data = await response.json();
        
        if (data.status !== 'success') {
            throw new Error(data.message || 'Failed to start face detection');
        }

        // Re-enable button after a short delay
        setTimeout(() => {
            button.disabled = false;
            button.classList.remove('button-disabled');
        }, 2000);
        
    } catch (error) {
        console.error(error);
        errorMessage.textContent = 'Failed to start the experience. Please try again.';
        errorMessage.classList.remove('hidden');
        button.disabled = false;
        button.classList.remove('button-disabled');
    }
}
