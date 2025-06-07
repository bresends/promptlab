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
            // Parse the response to extract just the prompt preview
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newPreview = doc.getElementById('promptPreview');
            if (newPreview) {
                const currentPreview = document.getElementById('promptPreview');
                if (currentPreview) {
                    currentPreview.innerHTML = newPreview.innerHTML;
                    // Re-highlight the syntax after updating content
                    if (typeof Prism !== 'undefined') {
                        Prism.highlightAllUnder(currentPreview);
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

function copyPrompt() {
    const promptPreview = document.getElementById('promptPreview');
    if (!promptPreview) return;

    // Get text content from the code element inside the pre tag
    const codeElement = promptPreview.querySelector('code');
    const promptText = codeElement ? codeElement.textContent : promptPreview.textContent;
    navigator.clipboard.writeText(promptText).then(() => {
        const button = document.getElementById('copyButton');
        if (!button) return;

        const originalText = button.innerHTML;
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
            </svg>
            Copied!
        `;
        button.classList.remove('bg-blue-600', 'hover:bg-blue-700');
        button.classList.add('bg-green-600');

        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('bg-green-600');
            button.classList.add('bg-blue-600', 'hover:bg-blue-700');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const copyButton = document.getElementById('copyButton');
    if (copyButton) {
        copyButton.addEventListener('click', copyPrompt);
    }

    // Initialize Prism highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
});
