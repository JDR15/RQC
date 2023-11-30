const navegacion = document.querySelector("#menu");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click", () =>{
    navegacion.classList.add("visible");
})

cerrar.addEventListener("click", () =>{
    navegacion.classList.remove("visible");
})

document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector("header");
    // Manejar el evento de scroll
    window.addEventListener("scroll", function () {
        if (window.scrollY > 10) {
            // Si se ha desplazado más de 50 píxeles, aplicar fondo sólido
            header.classList.add("scrolled");
        } else {
            // Si no, aplicar fondo transparente
            header.classList.remove("scrolled");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll(".type-animation");

    elements.forEach((element) => {
        const text = element.textContent;
        element.innerHTML = "";

        for (let i = 0; i < text.length; i++) {
            const span = document.createElement("span");
            span.textContent = text[i];
            span.style.animationDelay = `${i * 0.1}s`;
            element.appendChild(span);
        }

        element.classList.add("reveal");
    });
});

var modal = document.getElementById("modal");
var abrirModal = document.getElementById("abrirModal");
var cerrar2 = document.getElementsByClassName("cerrar")[0];

abrirModal.onclick = function() {
  modal.style.display = "block";
}

cerrar2.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

document.addEventListener('DOMContentLoaded', function() {
    var btnGroup = document.querySelector('.btn-group');
    var dropdownMenu = document.querySelector('.dropdown-menu');

    btnGroup.addEventListener('click', function() {
      dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
    });

    window.addEventListener('click', function(event) {
      if (!btnGroup.contains(event.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  });



