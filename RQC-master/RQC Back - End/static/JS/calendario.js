
//Funcion para el calendario
const cronograma = document.querySelector('.Cronograma');
const mes = document.querySelector('.mes');


let numero = mes.value -1;
console.log(numero)
const desplazamientoPorcentaje = 8.3333333333333333333333333333333;
const operacion = -desplazamientoPorcentaje * numero;
cronograma.style.transform = `translateX(${operacion}%)`;


function siguienteFunction(){
    numero = numero + 1;
    if (numero > 11) {
        numero = 11;
    }
    const operacion = -desplazamientoPorcentaje * numero;
    cronograma.style.transform = `translateX(${operacion}%)`;
} 

function atrasFunction(){
    numero = numero - 1;
    if (numero < 0) {
        numero = 0;
    }
    const operacion = -desplazamientoPorcentaje * numero;
    cronograma.style.transform = `translateX(${operacion}%)`;
}
