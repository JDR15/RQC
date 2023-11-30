function abrirModal(idCalificacion) {
    document.getElementById('modalActualizar').style.display = 'block';
    document.getElementById('id_calificacion_actualizar').value = idCalificacion;
}

function cerrarModal() {
    document.getElementById('modalActualizar').style.display = 'none';
}

function validarFormulario() {
    // Obtén los valores de los campos del formulario
    var id_tipo_nota = document.getElementsByName('id_tipo_nota')[0].value;
    var id_periodo = document.getElementsByName('id_periodo')[0].value;
    var calificacion = document.getElementsByName('calificacion')[0].value;

    // Validación básica, puedes agregar más validaciones según tus requisitos
    if (id_tipo_nota === "" || id_periodo === "" || calificacion === "") {
        // Muestra una notificación si algún campo está vacío
        mostrarNotificacion('Por favor, completa todos los campos antes de guardar.');
        return false; // Evita que el formulario se envíe
    }

    // Muestra una notificación de éxito
    mostrarNotificacion('Calificación ingresada exitosamente');

    return true; // Permite que el formulario se envíe
}

function mostrarNotificacion(mensaje) {
    // Verificar si el navegador es compatible con las notificaciones
    if ('Notification' in window) {
        // Solicitar permisos para mostrar notificaciones
        Notification.requestPermission().then(function(permission) {
            // Verificar si se ha concedido el permiso
            if (permission === 'granted') {
                // Mostrar la notificación
                var options = {
                    icon: '../static/img/logo.png' // Reemplazar con la ruta de tu propio icono
                };

                // Mostrar la notificación
                var notification = new Notification(mensaje, options);
            }
        });
    }
}


function validarFormularioActualizar() {
    // Obtener el formulario y los valores de los campos
    var formulario = document.querySelector('#modalActualizar form');
    var idCalificacion = formulario.querySelector('#id_calificacion_actualizar').value;
    var nueva_calificacion = formulario.querySelector('#nuevaCalificacion').value;
    var id_tipo_nota_actualizar= formulario.querySelector('#tipoNotaActualizar').value;
    var id_periodo_actualizar = formulario.querySelector('#peridoActualizar').value;

    // Validación básica
    if (idCalificacion === "" || nueva_calificacion === "" || id_tipo_nota_actualizar === "" || id_periodo_actualizar === "") {
        mostrarNotificacionActualizar('Por favor, completa todos los campos antes de actualizar.', 'error');
        return false;
    }

    // Muestra una notificación de éxito
    mostrarNotificacionActualizar('Calificacion actualizada exitosamente', 'success');

    return true;
}

function mostrarNotificacionActualizar(mensaje) {
    // Verificar si el navegador es compatible con las notificaciones
    if ('Notification' in window) {
        // Solicitar permisos para mostrar notificaciones
        Notification.requestPermission().then(function(permission) {
            // Verificar si se ha concedido el permiso
            if (permission === 'granted') {
                // Mostrar la notificación
                var options = {
                    icon: '../static/img/logo.png' // Reemplazar con la ruta de tu propio icono
                };

                // Mostrar la notificación
                var notification = new Notification(mensaje, options);
            }
        });
    }
}

