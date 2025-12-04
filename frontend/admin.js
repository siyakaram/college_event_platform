const adminRegisterForm = document.getElementById('adminRegisterForm');
const adminLoginForm = document.getElementById('adminLoginForm');
const dashboard = document.getElementById('dashboard');
const createEventForm = document.getElementById('createEventForm');

// Admin registration
adminRegisterForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('regUsername').value,
        password: document.getElementById('regPassword').value,
        secret_key: document.getElementById('regSecretKey').value
    };
    const res = await fetch('/admin/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message);
});

// Admin login
adminLoginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('adminUsername').value,
        password: document.getElementById('adminPassword').value
    };
    const res = await fetch('/admin/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message);
    if(result.success){
        dashboard.style.display = 'block';
    }
});

// Google Map
let map, marker;
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 5
    });
    map.addListener("click", (e) => {
        placeMarker(e.latLng);
    });
}
function placeMarker(location) {
    if (marker) marker.setMap(null);
    marker = new google.maps.Marker({
        position: location,
        map: map
    });
    document.getElementById("selectedLat").textContent = location.lat().toFixed(6);
    document.getElementById("selectedLon").textContent = location.lng().toFixed(6);
}
window.initMap = initMap;
window.addEventListener('load', initMap);

// Create event
createEventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", document.getElementById('eventName').value);
    formData.append("eligibility", document.getElementById('eventEligibility').value);
    formData.append("lat", parseFloat(document.getElementById("selectedLat").textContent));
    formData.append("lon", parseFloat(document.getElementById("selectedLon").textContent));
    formData.append("radius", document.getElementById('eventRadius').value);
    formData.append("certificate_template", document.getElementById('certTemplate').files[0]);
    const bgFile = document.getElementById('bgImage').files[0];
    if(bgFile) formData.append("background_image", bgFile);
    const res = await fetch('/admin/event/create', {
        method: 'POST',
        body: formData
    });
    const result = await res.json();
    alert(result.message);
});
