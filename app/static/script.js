document.addEventListener('DOMContentLoaded', function() {
    // Add any client-side functionality here
    console.log("Fake News Detector loaded");
    
    // Example: Add loading spinner during form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
                submitBtn.disabled = true;
            }
        });
    });
});