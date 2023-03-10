// LOG IN AND REGISTRER FORM POP UP
var login = document.getElementById('login');
var register = document.getElementById('register');

window.onclick = function(event) {
    if (event.target == login || event.target == register) {
        login.style.display = "none";
        register.style.display = "none";
    }
}



// PASSWORD
const togglePassword = document.querySelector("#togglePassword");

const password = document.querySelector("#password");

togglePassword.addEventListener("click", function () {
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);

    this.classList.toggle("bi-eye");
});