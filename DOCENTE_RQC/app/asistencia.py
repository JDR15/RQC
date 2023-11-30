from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistemaEducativo2'

# Conectar a la base de datos
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

def get_db_connection():
    return mysql.connector.connect(
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        host=app.config['MYSQL_HOST'],
        database=app.config['MYSQL_DB']
    )

cursor = db.cursor()

@app.route("/")
def index():
    return render_template('index.html') 


# Rutas de la aplicación
@app.route('/docenteAsistencia')
def docenteAsistencia():
    # Obtener nombres de estudiantes de la base de datos
    cursor.execute("SELECT idUsuario, primerNombre, primerApellido FROM Usuario")
    estudiantes = cursor.fetchall()

    # Obtener datos existentes para las listas desplegables
    cursor.execute("SELECT idMateria, nombreMate FROM Materia")
    materias = cursor.fetchall()

    cursor.execute("SELECT idPeriodo, FechaInicio, FechaCierre FROM periodo")
    periodos = cursor.fetchall()

    return render_template('teacher/attendance.html', estudiantes=estudiantes, materias=materias, periodos=periodos)

@app.route('/nueva_asistencia', methods=['POST'])
def nueva_asistencia():
    idEstudiantes = request.form.getlist('estudiantes')
    idMateriaFK = request.form['materia']
    idPeriodoFK = request.form['periodo']
    fecha = request.form['fecha']
    asistencia = 1 # Por defecto, marcamos asistencia como presente

    # Insertar asistencias en la base de datos para los estudiantes seleccionados
    for idEstudiante in idEstudiantes:
        cursor.execute("INSERT INTO Asistencia (idMateriaFK, idPeriodoFK, fecha, idEstudianteFK, asistencia) VALUES (%s, %s, %s, %s, %s)",
                       (idMateriaFK, idPeriodoFK, fecha, idEstudiante, asistencia))
        db.commit()

    return redirect(url_for('docenteAsistencia'))

@app.route('/actualizar_asistencia', methods=['POST'])
def actualizar_asistencia():
    idEstudiante = request.form['estudiantes']
    idMateriaFK = request.form['materia']
    idPeriodoFK = request.form['periodo']
    fecha = request.form['fecha']
    asistencia = request.form['asistencia']

    # Actualizar la asistencia del estudiante en la base de datos
    cursor.execute("UPDATE Asistencia SET idMateriaFK = %s, idPeriodoFK = %s, fecha = %s, asistencia = %s WHERE idEstudianteFK = %s",
                   (idMateriaFK, idPeriodoFK, fecha, asistencia, idEstudiante))
    db.commit()

    return redirect(url_for('docenteAsistencia'))


# REDIRECCIONES


@app.route('/home/<string:op>')
def home(op):
    if op == 'indexTeacher' :
        return render_template('teacher/indexTeacher.html')
    elif op == 'index':
        return render_template('index.html')
    elif op == 'aboutUs':
        return render_template('aboutUs.html')
    elif op == 'community':
        return render_template('community.html')
    elif op == 'attendance':
        return render_template('teacher/attendance.html')
    elif op == 'schedule':
        return render_template('teacher/schedule.html')
    elif op == 'rating':
        return render_template('teacher/ratings.html')
    
    
    
# CALIFICACIONES

@app.route('/calificaciones')
def calificaciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuario")
    estudiantes = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Materia")
    materias = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Actividades")
    actividades = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Periodo")
    periodos = cursor.fetchall()
    
    # Obtener tipos de nota para el select
    cursor.execute("SELECT * FROM TipoNo")
    tipos_nota = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('teacher/ratings.html', estudiantes=estudiantes, materias=materias, actividades=actividades, periodos=periodos, tipos_nota=tipos_nota)

@app.route('/ingresar_calificacion', methods=['POST'])
def ingresar_calificacion():
    if request.method == 'POST':
        estudiante_id = request.form['estudiante_id']
        materia_id = request.form['materia_id']
        calificacion = request.form['calificacion']
        id_tipo_nota = request.form['id_tipo_nota']
        id_periodo = request.form['id_periodo']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insertar en la tabla Calificacion con todos los campos
        cursor.execute("INSERT INTO Calificacion (idMateriaFK, idEstudianteFK, idTipoNotaFK, idPeriodoFK, nota, fecha) VALUES (%s, %s, %s, %s, %s, NOW())",
                       (materia_id, estudiante_id, id_tipo_nota, id_periodo, calificacion))
        
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('calificaciones'))

@app.route('/consultar_calificaciones')
def consultar_calificaciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Realizar la consulta para obtener las calificaciones
    cursor.execute("SELECT Calificacion.*, Materia.nombreMate, Usuario.primerNombre, Usuario.primerApellido, TipoNo.TipoNota, Periodo.FechaInicio, Periodo.FechaCierre FROM Calificacion "
                   "JOIN Materia ON Calificacion.idMateriaFK = Materia.idMateria "
                   "JOIN Usuario ON Calificacion.idEstudianteFK = Usuario.idUsuario "
                   "JOIN TipoNo ON Calificacion.idTipoNotaFK = TipoNo.idTipoNo "
                   "JOIN Periodo ON Calificacion.idPeriodoFK = Periodo.idPeriodo")
    calificaciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('teacher/consultRaiting.html', calificaciones=calificaciones)

@app.route('/actualizar_calificacion', methods=['POST'])
def actualizar_calificacion():
    if request.method == 'POST':
        id_calificacion = request.form['id_calificacion_actualizar']
        nueva_calificacion = request.form['nueva_calificacion']
        id_tipo_nota_actualizar = request.form['id_tipo_nota_actualizar']
        id_periodo_actualizar = request.form['id_periodo_actualizar']

        print(id_calificacion,nueva_calificacion,id_tipo_nota_actualizar,id_periodo_actualizar)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Realizar la actualización en la tabla Calificacion
        cursor.execute("UPDATE Calificacion SET nota = %s, idTipoNotaFK = %s, idPeriodoFK = %s WHERE idCali = %s",
                       (nueva_calificacion, id_tipo_nota_actualizar, id_periodo_actualizar, id_calificacion))

        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('consultar_calificaciones'))


if __name__ == '__main__':
    app.run(debug=True)