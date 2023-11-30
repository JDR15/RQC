function marcarTodos() {
    var checkboxes = document.getElementsByName('estudiantes');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = true;
    });
}

function desmarcarTodos() {
    var checkboxes = document.getElementsByName('estudiantes');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });
}

function abrirModal() {
    
    document.getElementById('modal_').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modal_').style.display = 'none';
}


function validarFormulario() {
    // Obtén los valores de los campos del formulario
    var materia = document.getElementById('materia').value;
    var periodo = document.getElementById('periodo').value;
    var fecha = document.getElementById('fecha').value;

    // Validación básica, puedes agregar más validaciones según tus requisitos
    if (materia === "" || periodo === "" || fecha === "") {
        // Muestra una notificación si algún campo está vacío
        mostrarNotificacion('Por favor, completa todos los campos antes de guardar.');
        return false; // Evita que el formulario se envíe
    }

    // Muestra una notificación de éxito
    mostrarNotificacion('Asistencias guardadas exitosamente');

    return true; // Permite que el formulario se envíe
}

// Función para mostrar la notificación
function mostrarNotificacion(mensaje) {
    // Verificar si el navegador es compatible con las notificaciones
    if ('Notification' in window) {
        // Solicitar permisos para mostrar notificaciones
        Notification.requestPermission().then(function(permission) {
            // Verificar si se ha concedido el permiso
            if (permission === 'granted') {
                // Mostrar la notificación
                var notification = new Notification(mensaje, {
                    icon: '../static/img/logo.png' // Reemplaza con la ruta de tu propio icono
                });
            }
        });
    }
}

function validarFormularioActualizar() {
    // Obtener el formulario y los valores de los campos
    var formulario = document.querySelector('#modal_ form');
    var idEstudiante = formulario.querySelector('#modal-idEstudiante').value;
    var materia = formulario.querySelector('#modal-materia').value;
    var periodo = formulario.querySelector('#modal-periodo').value;
    var fecha = formulario.querySelector('#modal-fecha').value;

    // Validación básica
    if (idEstudiante === "" || materia === "" || periodo === "" || fecha === "") {
        mostrarNotificacionActualizar('Por favor, completa todos los campos antes de guardar.', 'error');
        return false;
    }

    // Muestra una notificación de éxito
    mostrarNotificacionActualizar('Asistencias actualizadas exitosamente', 'success');

    return true;
}

function mostrarNotificacionActualizar(mensaje, tipo) {
    // Verificar si el navegador es compatible con las notificaciones
    if ('Notification' in window) {
        // Solicitar permisos para mostrar notificaciones
        Notification.requestPermission().then(function(permission) {
            // Verificar si se ha concedido el permiso
            if (permission === 'granted') {
                // Configurar el estilo de la notificación según el tipo
                var options = {
                    icon: '../static/img/logo.png' // Reemplazar con la ruta de tu propio icono
                };

                // Mostrar la notificación
                var notification = new Notification(mensaje, options);
            }
        });
    }
}
