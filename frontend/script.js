const registrationForm = document.getElementById('registrationForm');
const loginForm = document.getElementById('loginForm');
const showRegister = document.getElementById('showRegister');
const showLogin = document.getElementById('showLogin');

showRegister.addEventListener('click', () => {
    registrationForm.style.display = 'block';
    loginForm.style.display = 'none';
});

showLogin.addEventListener('click', () => {
    registrationForm.style.display = 'none';
    loginForm.style.display = 'block';
});

// Student Registration
registrationForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const data = {
                name: document.getElementById('name').value,
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                lat: position.coords.latitude,
                lon: position.coords.longitude
            };
            const res = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            alert(result.message);
        });
    } else {
        alert("Geolocation not supported!");
    }
});

// Student Login
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('loginUsername').value,
        password: document.getElementById('loginPassword').value
    };
    const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await res.json();
    alert(result.message);
});

// Load event background dynamically
async function loadEvent(eventId) {
    const res = await fetch(`/event/${eventId}`);
    const event = await res.json();
    if(event.background_image){
        document.body.style.backgroundImage = `url(${event.background_image})`;
    } else {
        document.body.style.backgroundImage = "url('background.png')";
    }
}
