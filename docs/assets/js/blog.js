/**
    * @author  EliasDH Team
    * @see https://eliasdh.com
    * @since 01/01/2025
**/

document.addEventListener('DOMContentLoaded', function() {
    loadExternalContent("context-menu", "https://eliasdehondt.github.io/Internship/assets/includes/context-menu.html");
    loadExternalContent("footer", "https://eliasdehondt.github.io/Internship/assets/includes/external-footer.html");
});

document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-reveal');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.blog-post').forEach(post => {
        observer.observe(post);
    });
});