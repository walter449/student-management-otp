const API_URL = "http://localhost:8000/auth";

document.getElementById("send-btn").addEventListener("click", sendOTP);

document.getElementById("verify-btn").addEventListener("click", verifyOTP);

function sendOTP() {

    const email = document.getElementById("email").value;

    fetch(`${API_URL}/send-otp`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert("Error enviando OTP");
    });
}

function verifyOTP() {

    const email = document.getElementById("email").value;

    const otp = document.getElementById("otp").value;

    fetch(`${API_URL}/verify-otp`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, otp })
    })
    .then(response => response.json())
    .then(data => {

        if (data.success) {

            alert("Login exitoso");

            window.location.href = "./index.html";

        } else {

            alert(data.message);
        }
    })
    .catch(error => {
        alert("Error verificando OTP");
    });
}