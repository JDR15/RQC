hamburger = document.querySelector(".hamburger");

hamburger.onclick= function(){
    navBar = document.querySelector(".nav-bar")
    navBar.classList.toggle("active")
}


// Función para abrir un modal
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'block';
}

// Función para cerrar un modal
function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'none';
}
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

function toggleMenu() {
    const userMenu = document.querySelector('.usermenu');
    userMenu.classList.toggle('active');
}




