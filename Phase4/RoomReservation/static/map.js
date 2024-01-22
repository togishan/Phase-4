document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([39.891745, 32.783641], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
});