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

const mainContent = document.querySelector("main");
const deviceStatus = document.getElementById("deviceStatus");
const deviceContainer = deviceStatus.querySelector(".device-container");

const devices = [
    { name: "Switch 1", status: "up" },
    { name: "Switch 2", status: "up" },
    { name: "Switch 3", status: "down" },
    { name: "Switch 4", status: "down" },
    { name: "Ap305-MT-G09", status: "up" },
    { name: "Ap305-MT-G05", status: "up" },
    { name: "Ap305-MT-G01", status: "up" },
    { name: "Ap305-MT-G24", status: "up" },
    { name: "Ap305-MT-G29", status: "up" },
    { name: "Ap305-MT-L42", status: "up" },
    { name: "Ap305-MT-L38", status: "up" },
    { name: "Ap305-MT-L48", status: "up" },
    { name: "Ap305-MT-L52", status: "up" },
    { name: "Ap305-MT-L57", status: "up" },
    { name: "Ap305-MT-LSTAIR", status: "up" },
    { name: "Ap305-MT-F64", status: "up" },
    { name: "Ap305-MT-CON", status: "up" },
    { name: "Ap305-MT-RSTNT", status: "up" },
    { name: "HP PC MPC001", status: "down" },
    { name: "HP PC MPC002", status: "down" },
    { name: "HP PC MPC003", status: "down" },
    { name: "HP PC MPC004", status: "down" },
    { name: "HP PC MPC005", status: "down" },
    { name: "TV Restaurant", status: "unknown" },
    { name: "Door_ACL", status: "up" },
    { name: "Ap305-MT-KITCHEN", status: "up" },
    { name: "HIKvision recorder", status: "up" }
];


function renderDevices() {
    deviceContainer.innerHTML = "";
    devices.forEach(device => {
        const el = document.createElement("div");
        el.classList.add("device", device.status);

        el.innerHTML = `${device.name} <br><br> ${device.status.toUpperCase()}`;
        deviceContainer.appendChild(el);
    });
}

function toggleView() {
    mainContent.style.display = "none";
    deviceStatus.style.display = "block";
    renderDevices();

    setTimeout(() => {
        mainContent.style.display = "table";
        deviceStatus.style.display = "none";
    }, 15000);
}

toggleView();
setInterval(toggleView, 60000);