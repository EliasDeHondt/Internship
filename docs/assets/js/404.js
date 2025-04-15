/**
    * @author  EliasDH Team
    * @see https://eliasdh.com
    * @since 01/01/2025
**/

document.addEventListener("DOMContentLoaded", function() {
    const startDate = new Date("2025-03-29T00:00:00");
    const endDate = new Date("2025-06-07T23:59:59");
    const progressBar = document.getElementById("progressBar");

    function updateProgressBar() {
        const currentDate = new Date();
        const totalTime = endDate - startDate;
        const elapsedTime = currentDate - startDate;
        let progressPercentage = (elapsedTime / totalTime) * 100;

        progressPercentage = Math.min(Math.max(progressPercentage, 0), 100);
        progressBar.style.width = progressPercentage.toFixed(4) + "%";
        progressBar.textContent = progressPercentage.toFixed(4) + "% Completed";
    }
    updateProgressBar();
    setInterval(updateProgressBar, 1000);
});