// Interactive Prompt JavaScript
let updateTimeout;

function updatePrompt() {
    // Debounce updates to avoid too many requests
    clearTimeout(updateTimeout);
    updateTimeout = setTimeout(() => {
        const form = document.getElementById('promptForm');
        if (!form) return;

        const formData = new FormData(form);

        fetch(window.location.href, {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Parse the response to extract the prompt previews
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Update system prompt preview (preserve the copy button)
            const newSystemPreview = doc.getElementById('systemPromptPreview');
            if (newSystemPreview) {
                const currentSystemPreview = document.getElementById('systemPromptPreview');
                if (currentSystemPreview) {
                    // Extract the new content (everything except the button)
                    const newSystemContent = newSystemPreview.querySelector('pre');
                    const currentSystemContent = currentSystemPreview.querySelector('pre');
                    if (newSystemContent && currentSystemContent) {
                        currentSystemContent.innerHTML = newSystemContent.innerHTML;
                        if (typeof Prism !== 'undefined') {
                            Prism.highlightAllUnder(currentSystemContent);
                        }
                    }
                }
            }
            
            // Update user prompt preview (preserve the copy button)
            const newUserPreview = doc.getElementById('userPromptPreview');
            if (newUserPreview) {
                const currentUserPreview = document.getElementById('userPromptPreview');
                if (currentUserPreview) {
                    // Extract the new content (everything except the button)
                    const newUserContent = newUserPreview.querySelector('pre');
                    const currentUserContent = currentUserPreview.querySelector('pre');
                    if (newUserContent && currentUserContent) {
                        currentUserContent.innerHTML = newUserContent.innerHTML;
                        if (typeof Prism !== 'undefined') {
                            Prism.highlightAllUnder(currentUserContent);
                        }
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error updating prompt:', error);
        });
    }, 300); // 300ms debounce
}

function clearForm() {
    const form = document.getElementById('promptForm');
    if (!form) return;

    const textareas = form.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.value = '';
    });
    updatePrompt();
}

function copySystemPrompt() {
    const systemPreview = document.getElementById('systemPromptPreview');
    if (!systemPreview) return;

    const codeElement = systemPreview.querySelector('code');
    const promptText = codeElement ? codeElement.textContent : systemPreview.textContent;
    copyToClipboard(promptText, 'copySystemButton');
}

function copyUserPrompt() {
    const userPreview = document.getElementById('userPromptPreview');
    if (!userPreview) return;

    const codeElement = userPreview.querySelector('code');
    const promptText = codeElement ? codeElement.textContent : userPreview.textContent;
    copyToClipboard(promptText, 'copyUserButton');
}

function copyBothPrompts() {
    const systemPreview = document.getElementById('systemPromptPreview');
    const userPreview = document.getElementById('userPromptPreview');
    if (!systemPreview || !userPreview) return;

    const systemCode = systemPreview.querySelector('code');
    const userCode = userPreview.querySelector('code');
    const systemText = systemCode ? systemCode.textContent : systemPreview.textContent;
    const userText = userCode ? userCode.textContent : userPreview.textContent;
    
    // Format for Claude web UI
    const combinedText = `${systemText.trim()}\n\n${userText.trim()}`;
    copyToClipboard(combinedText, 'copyBothButton');
}

function copyToClipboard(text, buttonId) {
    navigator.clipboard.writeText(text).then(() => {
        const button = document.getElementById(buttonId);
        if (!button) return;

        const originalHTML = button.innerHTML;
        
        // Show checkmark for clipboard icons or "Copied!" for the main button
        if (buttonId === 'copyBothButton') {
            button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
                Copied!
            `;
        } else {
            // For clipboard icons, show a thin checkmark
            button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                </svg>
            `;
            button.classList.add('text-green-600');
        }

        setTimeout(() => {
            button.innerHTML = originalHTML;
            if (buttonId !== 'copyBothButton') {
                button.classList.remove('text-green-600');
            }
        }, 1500);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for copy buttons
    const copySystemButton = document.getElementById('copySystemButton');
    if (copySystemButton) {
        copySystemButton.addEventListener('click', copySystemPrompt);
    }

    const copyUserButton = document.getElementById('copyUserButton');
    if (copyUserButton) {
        copyUserButton.addEventListener('click', copyUserPrompt);
    }

    const copyBothButton = document.getElementById('copyBothButton');
    if (copyBothButton) {
        copyBothButton.addEventListener('click', copyBothPrompts);
    }

    // Initialize Prism highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
});
