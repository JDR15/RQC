from flask import Flask, render_template, request, redirect, url_for, Response, session
import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
import database as db

#importar Flask, flask-MySQLdb, MySQL, mysql-connector-python, pdfkit y https://wkhtmltopdf.org/downloads.html

template_dir=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir=os.path.join(template_dir, "RQC",'templates')

app= Flask(__name__)

#rutas de la aplicaciones
@app.route('/')
def home():
    session['logueado']=True
    cursor= db.database.cursor()
    cursor.execute("Select * from contenido")
    myresult= cursor.fetchall()
    #Convertir los dato a diccionario
    insertObject= []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    print("Entro")
    return render_template('index.html', data = insertObject)
#vista sobre nosotros
@app.route('/sobreNosotros')
def sobreNosotros():
    return render_template('views/Sobrenosotros.html')
#vista login
@app.route('/login')
def login():
    return render_template('views/login.html')

#Funcion de login
#Validacion del login
@app.route('/validarLogin', methods=["get","post"])
def validarLogin():

    if 'correo' in request.form and 'password' in request.form:
        correo=request.form['correo']
        password=request.form['password']

        cursor= db.database.cursor()
        cursor.execute('select * from Usuario where Correo= %s and contraseña=%s', (correo,password,))
        account = cursor.fetchone()

        cursor.execute("select  idRolFK, count(idUsuario) as numeroEstudiantes from usuario  group by idRolFK;")
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password,))
        myresult2= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject2= []
        columnNames2 = [column[0] for column in cursor.description]
        for record2 in myresult2:
            insertObject2.append(dict(zip(columnNames2, record2)))

        cursor.execute("select count(idMateria) as numeroMaterias from materia;")
        myresult3= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject3= []
        columnNames3 = [column[0] for column in cursor.description]
        for record3 in myresult3:
            insertObject3.append(dict(zip(columnNames3, record3)))
        cursor.close()
    
        if account:
            session['idRolFK'] = account[11] 
            session['logueado']=False
            session['correo2']=account[22]
            session['password2']=account[23]
            session['idRolFK'] = account[25] 

            cursor= db.database.cursor()

            cursor.execute("""SELECT monthname(now()) mes,
                                day(DATE_ADD(CURDATE(), INTERVAL 0-DAYOFWEEK(CURDATE()) DAY)) AS Sabado,
                                day(DATE_ADD(CURDATE(), INTERVAL 1-DAYOFWEEK(CURDATE()) DAY)) AS Domingo,
                                day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,
                                day(DATE_ADD(CURDATE(), INTERVAL 3-DAYOFWEEK(CURDATE()) DAY)) AS Martes,
                                day(DATE_ADD(CURDATE(), INTERVAL 4-DAYOFWEEK(CURDATE()) DAY)) AS Miercoles,
                                day(DATE_ADD(CURDATE(), INTERVAL 5-DAYOFWEEK(CURDATE()) DAY)) AS Jueves,
                                day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes;""")
            dias = cursor.fetchone()


            if session['idRolFK']==1:
                 
                cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));")
                account = cursor.fetchall()
                insertObject6= []
                columnNames = [column[0] for column in cursor.description]
                for record6 in account:
                    insertObject6.append(dict(zip(columnNames, record6)))
                
                return render_template("views/vistaRector.html", data=insertObject, data2=insertObject2, data3=insertObject3, dias=dias, eventos2=insertObject6)
            
            
            elif session['idRolFK']==3:

                cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));")
                account = cursor.fetchall()
                insertObject6= []
                columnNames = [column[0] for column in cursor.description]
                for record6 in account:
                    insertObject6.append(dict(zip(columnNames, record6)))
                 
                return render_template("views/vistaRector.html", data=insertObject, data2=insertObject2, data3=insertObject3, dias=dias, eventos2=insertObject6)
                
        else:

            return render_template("views/login.html", mensaje="Usuario o contraseña incorrectas")   

#Vista estudiantes
@app.route('/estudiantes', methods=["get"])
def estudiantes():

    logueado2=session['logueado']
    print(logueado2)
    
    
    if logueado2==False:
        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject5= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject5.append(dict(zip(columnNames, record5)))

        if 'curso' in request.form :
            curso=request.form['curso']
            if curso:

                cursor= db.database.cursor()
                cursor.execute("select Numcurso, primerNombre, segundoNombre, primerApellido,segundoApellido, count(idUsuario) from curso inner join usuario on curso.idDocenteFK=usuario.idusuario where Numcurso= %s;", (curso,))
                myresult= cursor.fetchall()
                #Convertir los dato a diccionario
                insertObject= []
                columnNames = [column[0] for column in cursor.description]
                for record in myresult:
                    insertObject.append(dict(zip(columnNames, record)))

                return render_template("views/Estudiantes.html", data=insertObject, data5=insertObject5)

        else :

            cursor= db.database.cursor()
            cursor.execute("select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;")
            myresult= cursor.fetchall()
            #Convertir los dato a diccionario
            insertObject= []
            columnNames = [column[0] for column in cursor.description]
            for record in myresult:
                insertObject.append(dict(zip(columnNames, record)))

            cursor.execute("select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 group by numCursoFK;")
            myresult2= cursor.fetchall()
            #Convertir los dato a diccionario
            insertObject2= []
            columnNames = [column[0] for column in cursor.description]
            for record2 in myresult2:
                insertObject2.append(dict(zip(columnNames, record2)))

            #datos para el formulario de estudiante
            cursor.execute("Select idTipoDoc, tipoDocUsu from tipoDoc where estado='Activo'")
            myresult3= cursor.fetchall()
            #Convertir los dato a diccionario
            insertObject3= []
            columnNames = [column[0] for column in cursor.description]
            for record3 in myresult3:
                insertObject3.append(dict(zip(columnNames, record3)))

            cursor.execute("Select idUsuario ,primerNombre, segundoNombre, primerApellido,segundoApellido, estadoUsu from usuario where idRolFK=3 and estadoUsu='Activo';")
            myresult4= cursor.fetchall()
            #Convertir los dato a diccionario
            insertObject4= []
            columnNames = [column[0] for column in cursor.description]
            for record4 in myresult4:
                insertObject4.append(dict(zip(columnNames, record4)))
            cursor.close()

            return render_template("views/Estudiantes.html", data=insertObject, data2=insertObject2, data3=insertObject3 , data4=insertObject4, data5=insertObject5)

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")   
#Vista docentes
@app.route('/docentes', methods=["get"])
def docentes():
    logueado2=session['logueado']
    print(logueado2)
    
    
    if logueado2==False:
        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject5= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject5.append(dict(zip(columnNames, record5)))

        cursor= db.database.cursor()
        cursor.execute("select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;")
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select * from Usuario where idRolFK=3; ")
        account = cursor.fetchall()
        insertObject2= []
        columnNames = [column[0] for column in cursor.description]
        for record2 in account:
            insertObject2.append(dict(zip(columnNames, record2)))

        cursor.execute("Select idTipoDoc, tipoDocUsu from tipoDoc where estado='Activo'")
        myresult3= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject3= []
        columnNames = [column[0] for column in cursor.description]
        for record3 in myresult3:
            insertObject3.append(dict(zip(columnNames, record3)))

        return render_template('views/ListDocentes.html', data5=insertObject5, data=insertObject, data3=insertObject3, data2=insertObject2)

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion") 
#visualiazar por docente
@app.route('/vistaPorDocente/<string:idUsuario>')
def vistaPorDocente(idUsuario):

    logueado2=session['logueado']

    if logueado2==False:
        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject5= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject5.append(dict(zip(columnNames, record5)))

        cursor.execute("select * from usuario where idUsuario=%s;",(idUsuario,))
        account = cursor.fetchall()
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in account:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select * from materia where idDocenteFK=%s;",(idUsuario,))
        account = cursor.fetchall()
        insertObject2= []
        columnNames = [column[0] for column in cursor.description]
        for record2 in account:
            insertObject2.append(dict(zip(columnNames, record2)))

        cursor.execute("Select idTipoDoc, tipoDocUsu from tipoDoc where estado='Activo';")
        myresult3= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject3= []
        columnNames = [column[0] for column in cursor.description]
        for record3 in myresult3:
            insertObject3.append(dict(zip(columnNames, record3)))

        cursor= db.database.cursor()
        cursor.execute("select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;")
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject4= []
        columnNames = [column[0] for column in cursor.description]
        for record4 in myresult:
            insertObject4.append(dict(zip(columnNames, record4)))

        cursor.execute("select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 group by numCursoFK;")
        myresult2= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject6= []
        columnNames = [column[0] for column in cursor.description]
        for record6 in myresult2:
            insertObject6.append(dict(zip(columnNames, record6)))

        return render_template('views/infoDocente.html', data5=insertObject5, data=insertObject, data2=insertObject2, data3=insertObject3, data4=insertObject4, data6=insertObject6)

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion") 

#agregar estudiante
@app.route('/addEstudiante', methods=["post"])
def addEstudiante():
    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:
        #Datos del estudiante
        primerNombre=request.form['primerNombre']
        segundoNombre=request.form['segundoNombre']
        primeraApellido=request.form['primerApellido']
        segundoApellido=request.form['segundoApellido']
        genero=request.form['genero']
        nacimiento=request.form['nacimiento']
        municipioNaci=request.form['municipioNaci']
        FechaNaci=request.form['FechaNaci']
        edad=request.form['edad']
        tipoDoc=request.form['tipoDoc']
        numberDocu=request.form['numberDocu']
        barrio=request.form['barrio']
        estrato=request.form['estrato']
        direccion=request.form['direccion']
        numeroF=request.form['numeroF']
        numeroC=request.form['numeroC']
        afiliacion=request.form['afiliacion']
        eps=request.form['eps']
        LugarA=request.form['LugarA']
        rh=request.form['RH']
        curso=request.form['curso']
        Correo=request.form['Correo']
        contraseña=request.form['contraseña']
        estado='Activo'
        idRolFK=1

        if primerNombre and segundoNombre and primeraApellido and segundoApellido and genero and nacimiento and municipioNaci and FechaNaci and edad and tipoDoc and numberDocu and barrio and estrato and direccion and numeroC and eps and LugarA and rh and curso and Correo and contraseña and estado and idRolFK:
            cursor= db.database.cursor()
            cursor.execute("insert into Usuario ( primerNombre, segundoNombre, primerApellido, segundoApellido, genero, DepNacimiento, municipioNaci,FechaNaci, edad, tipoDocUsuFK, numberDocu, barrio, estrato, direccion, numeroF, numeroC, afiliacion, eps, LugarA, RH, numCursoFK, Correo, contraseña, estadoUsu, idRolFK)  values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s);",(primerNombre,segundoNombre,primeraApellido,segundoApellido,genero,nacimiento,municipioNaci,FechaNaci,edad,tipoDoc,numberDocu,barrio,estrato,direccion,numeroF,numeroC,afiliacion,eps,LugarA,rh,curso,Correo,contraseña,estado,idRolFK))
            db.database.commit()


            return redirect(url_for('estudiantes' ))

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")  

#agregar docente
@app.route('/addDocentes', methods=["post"])
def addDocente():
    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:
        #Datos del docente
        primerNombre=request.form['primerNombre']
        segundoNombre=request.form['segundoNombre']
        primeraApellido=request.form['primerApellido']
        segundoApellido=request.form['segundoApellido']
        genero=request.form['genero']
        nacimiento=request.form['nacimiento']
        municipioNaci=request.form['municipioNaci']
        FechaNaci=request.form['FechaNaci']
        edad=request.form['edad']
        tipoDoc=request.form['tipoDoc']
        numberDocu=request.form['numberDocu']
        barrio=request.form['barrio']
        estrato=request.form['estrato']
        direccion=request.form['direccion']
        numeroF=request.form['numeroF']
        numeroC=request.form['numeroC']
        Correo=request.form['Correo']
        contraseña=request.form['contra']
        estado='Activo'
        idRolFK=3

        if primerNombre and segundoNombre and primeraApellido and segundoApellido and genero and nacimiento and municipioNaci and FechaNaci and edad and tipoDoc and numberDocu and barrio and estrato and direccion and numeroC and Correo and contraseña and estado and idRolFK:
            cursor= db.database.cursor()
            cursor.execute("insert into Usuario ( primerNombre, segundoNombre, primerApellido, segundoApellido, genero, DepNacimiento, municipioNaci,FechaNaci, edad, tipoDocUsuFK, numberDocu, barrio, estrato, direccion, numeroF, numeroC, Correo, contraseña, estadoUsu, idRolFK)  values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s);",(primerNombre,segundoNombre,primeraApellido,segundoApellido,genero,nacimiento,municipioNaci,FechaNaci,edad,tipoDoc,numberDocu,barrio,estrato,direccion,numeroF,numeroC, Correo,contraseña,estado,idRolFK))
            db.database.commit()


            return redirect(url_for('docentes' ))
        
        else:
            return redirect(url_for('docentes'))

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")  

#Agregar curso
@app.route('/addCurso', methods=["post"])
def addCurso():

    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:
        #Datos del curso
        DirecCurso=request.form['direcCurso']
        Ccurso=request.form['Ccurso']
        Cantidad=request.form['cantidad']

        if DirecCurso and Ccurso and Cantidad:
            cursor= db.database.cursor()
            cursor.execute("insert into curso values(%s, %s, %s)",(Ccurso, DirecCurso,  Cantidad))
            db.database.commit()
            return redirect(url_for('estudiantes'))

    else:
        return render_template("views/login.html", mensaje="Bebes iniciar Sesion") 

#Visualizar curso y sus estudiantes
@app.route('/vistaPorCurso/<string:numCurso>')
def vistaPorCurso(numCurso):

    logueado2=session['logueado']
    print(logueado2)


    if logueado2==False:
        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject5= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject5.append(dict(zip(columnNames, record5)))

        cursor= db.database.cursor()
        cursor.execute("select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido, nombreMate from curso inner join usuario on curso.idDocenteFK=usuario.idusuario inner join materia on materia.numCursoFK=curso.numCurso where numCurso=%s group by numCurso;",(numCurso,))
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 and numCursoFK=%s;",(numCurso,))
        myresult2= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject2= []
        columnNames = [column[0] for column in cursor.description]
        for record2 in myresult2:
            insertObject2.append(dict(zip(columnNames, record2)))

        cursor.execute("select idUsuario, tipoDocUsu, numberDocu, primerNombre, segundoNombre, primerApellido,segundoApellido,  genero, DepNacimiento, municipioNaci,FechaNaci, edad, tipoDocUsuFK, numberDocu, barrio, estrato, direccion, numeroF, numeroC, afiliacion, eps, LugarA, RH, numCursoFK, Correo, contraseña,estadoUsu, rol from usuario as u inner join rol as r on u.idRolFK=r.idRol inner join tipoDoc as t on u.tipoDocUsuFK=t.idTipoDoc where numCursoFK=%s;",(numCurso,))
        myresult3= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject3= []
        columnNames = [column[0] for column in cursor.description]
        for record3 in myresult3:
            insertObject3.append(dict(zip(columnNames, record3)))


        return render_template('views/vistaPorCurso.html', data=insertObject, data2=insertObject2, data3=insertObject3, data5=insertObject5)

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion") 

#Cambiar estado de estudiantes
@app.route('/cambiarEstado/<string:idUsuario>')
def cambiarEstado(idUsuario):
        
    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:
        print(idUsuario)
        cursor= db.database.cursor()
        cursor.execute("select numCursoFK, estadoUsu, idRolFK from usuario where idUsuario=%s",(idUsuario,))
        myresult= cursor.fetchone()

        if myresult[2]==1:

            if myresult[1]=='Activo':
                sql = "update usuario set estadoUsu='Inactivo' where idUsuario=%s"
                data=(idUsuario, )
                cursor.execute(sql, data)
                db.database.commit()
                return redirect(url_for('vistaPorCurso', numCurso=myresult[0]))
            else:
                sql = "update usuario set estadoUsu='Activo' where idUsuario=%s"
                data=(idUsuario, )
                cursor.execute(sql, data)
                db.database.commit()
                return redirect(url_for('vistaPorCurso', numCurso=myresult[0]))
            
        elif myresult[2]==3:
                return redirect(url_for('inicio'))


    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion") 

#Editar usuario
@app.route('/edit/<string:idUsuario>', methods=["post"])
def edit(idUsuario):

    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:

        cursor= db.database.cursor()
        cursor.execute("select idRolFK from usuario where idUsuario=%s;",(idUsuario,))
        myresult= cursor.fetchone()
        
        primerNombre=request.form['primerNombre']
        segundoNombre=request.form['segundoNombre']
        primeraApellido=request.form['primerApellido']
        segundoApellido=request.form['segundoApellido']
        genero=request.form['genero']
        nacimiento=request.form['nacimiento']
        municipioNaci=request.form['municipioNaci']
        FechaNaci=request.form['FechaNaci']
        edad=request.form['edad']
        tipoDoc=request.form['tipoDoc']
        numberDocu=request.form['numberDocu']
        barrio=request.form['barrio']
        estrato=request.form['estrato']
        direccion=request.form['direccion']
        numeroF=request.form['numeroF']
        numeroC=request.form['numeroC']
        Correo=request.form['Correo']
        contraseña=request.form['contraseña']

        if myresult[0]==1:
            curso=request.form['curso']

            cursor= db.database.cursor()
            sql = "update Usuario set primerNombre=%s, segundoNombre=%s, primerApellido=%s, segundoApellido=%s, genero=%s, DepNacimiento=%s, municipioNaci=%s, FechaNaci=%s, edad=%s, tipoDocUsuFK=%s, numberDocu=%s, barrio=%s, estrato=%s, direccion=%s, numeroF=%s, numeroC=%s, numCursoFK=%s, Correo=%s, contraseña=%s where idUsuario=%s"
            data=(primerNombre,segundoNombre,primeraApellido,segundoApellido,genero,nacimiento,municipioNaci,FechaNaci,edad,tipoDoc,numberDocu,barrio,estrato,direccion,numeroF,numeroC,curso,Correo,contraseña, idUsuario)
            cursor.execute(sql, data)
            db.database.commit()

            cursor.execute("select numCursoFK from usuario where idUsuario=%s",(idUsuario,))
            myresult2= cursor.fetchone()
            
            return redirect(url_for('vistaPorCurso', numCurso=myresult2[0]))
        
        elif myresult[0]==3:
                    
                    cursor= db.database.cursor()
                    sql = "update Usuario set primerNombre=%s, segundoNombre=%s, primerApellido=%s, segundoApellido=%s, genero=%s, DepNacimiento=%s, municipioNaci=%s, FechaNaci=%s, edad=%s, tipoDocUsuFK=%s, numberDocu=%s, barrio=%s, estrato=%s, direccion=%s, numeroF=%s, numeroC=%s, Correo=%s, contraseña=%s where idUsuario=%s"
                    data=(primerNombre,segundoNombre,primeraApellido,segundoApellido,genero,nacimiento,municipioNaci,FechaNaci,edad,tipoDoc,numberDocu,barrio,estrato,direccion,numeroF,numeroC,Correo,contraseña, idUsuario)
                    cursor.execute(sql, data)
                    db.database.commit()
                    
                    return redirect(url_for('vistaPorDocente', idUsuario=idUsuario))
 

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion") 


@app.route('/inicio')
def inicio():

    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:
    
        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)
        idRol=session['idRolFK']

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject2= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject2.append(dict(zip(columnNames, record5)))

        cursor.execute("select  idRolFK, count(idUsuario) as numeroEstudiantes from usuario  group by idRolFK;")
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select count(idMateria) as numeroMaterias from materia;")
        myresult3= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject3= []
        columnNames3 = [column[0] for column in cursor.description]
        for record3 in myresult3:
            insertObject3.append(dict(zip(columnNames3, record3)))
        


        cursor.execute("""SELECT monthname(now()) mes,
                            day(DATE_ADD(CURDATE(), INTERVAL 0-DAYOFWEEK(CURDATE()) DAY)) AS Sabado,
                            day(DATE_ADD(CURDATE(), INTERVAL 1-DAYOFWEEK(CURDATE()) DAY)) AS Domingo,
                            day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,
                            day(DATE_ADD(CURDATE(), INTERVAL 3-DAYOFWEEK(CURDATE()) DAY)) AS Martes,
                            day(DATE_ADD(CURDATE(), INTERVAL 4-DAYOFWEEK(CURDATE()) DAY)) AS Miercoles,
                            day(DATE_ADD(CURDATE(), INTERVAL 5-DAYOFWEEK(CURDATE()) DAY)) AS Jueves,
                            day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes;""")
        dias = cursor.fetchone()

        if idRol==1:

            cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));")
            account = cursor.fetchall()
            insertObject6= []
            columnNames = [column[0] for column in cursor.description]
            for record6 in account:
                insertObject6.append(dict(zip(columnNames, record6)))
            
            return render_template("views/vistaRector.html", data=insertObject, data2=insertObject2, data3=insertObject3, dias=dias, eventos2=insertObject6)
            
        elif idRol==2:

            cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));")
            account = cursor.fetchall()
            insertObject6= []
            columnNames = [column[0] for column in cursor.description]
            for record6 in account:
                insertObject6.append(dict(zip(columnNames, record6)))
            
            return render_template("views/vistaRector.html", data=insertObject, data2=insertObject2, data3=insertObject3, dias=dias, eventos2=insertObject6)
        

        else:
            cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));")
            account = cursor.fetchall()
            insertObject6= []
            columnNames = [column[0] for column in cursor.description]
            for record6 in account:
                insertObject6.append(dict(zip(columnNames, record6)))
            
            return render_template("views/vistaRector.html", data=insertObject, data2=insertObject2, data3=insertObject3, dias=dias, eventos2=insertObject6)
            
        cursor.close()
    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")

#Cronograma
@app.route('/calendario')
def calendario():

    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:

        cursor= db.database.cursor()


        cursor.execute("select day(now()) as dia, month(now()) as mes, monthname(now()) as nombreMes;")
        account = cursor.fetchone()

        return redirect(url_for("evento",mes=account[2],dia=account[0]))


    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")

#Vizualizar eventos por dia
@app.route('/evento/<string:mes>/<string:dia>', methods=["get"])
def evento(mes, dia):

    correo=session['correo2']
    print(correo)
    password2=session['password2']
    print(password2)

    cursor= db.database.cursor()
    cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
    account = cursor.fetchall()
    insertObject5= []
    columnNames = [column[0] for column in cursor.description]
    for record5 in account:
        insertObject5.append(dict(zip(columnNames, record5)))

    cursor.execute("select * from DiasMeses;")
    account = cursor.fetchall()
    insertObject= []
    columnNames = [column[0] for column in cursor.description]
    for record in account:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.execute("select day(now()) as dia, month(now()) as mes, monthname(now()) as nombreMes;")
    account2 = cursor.fetchone()


    cursor.execute("select idActividad, monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad , idTipoAcFK, time(fechaInicio) as inicio, time(fechaCierre) as cierre, tipoActividad from Actividades inner join TipoActividad as t on Actividades.idTipoAcFK=t.idTipoAc where monthname(fechaInicio)=%s and day(fechaInicio)=%s and idTipoAcFK in ('2','3');",(mes,dia,))
    account = cursor.fetchall()
    insertObject2= []
    columnNames = [column[0] for column in cursor.description]
    for record2 in account:
        insertObject2.append(dict(zip(columnNames, record2)))

    cursor.execute("select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK from Actividades where idTipoAcFK in ('2','3');")
    account = cursor.fetchall()
    insertObject6= []
    columnNames = [column[0] for column in cursor.description]
    for record6 in account:
        insertObject6.append(dict(zip(columnNames, record6)))

    cursor.execute("select tipoActividad, idTipoAc from tipoActividad where idTipoAc in (2,3)")
    account = cursor.fetchall()
    tipoActividad= []
    columnNames = [column[0] for column in cursor.description]
    for record10 in account:
        tipoActividad.append(dict(zip(columnNames, record10)))

    print(insertObject2)

    if insertObject2:
        return render_template('views/Calendario.html', data=insertObject, data2=account2, eventos=insertObject2, data5=insertObject5, mes=mes, dia=dia, eventos2=insertObject6, tipoActividad=tipoActividad)
    else: 
        return render_template('views/Calendario.html', data=insertObject, data2=account2, mensaje="No hay eventos para este dia",data5=insertObject5, mes=mes, dia=dia, eventos2=insertObject6)

#editar evento
@app.route('/editEvent/<string:idActividad>', methods=["post"])
def editEvent(idActividad):

    titulo=request.form['til']
    descripcion=request.form['des']
    tipoActividad=request.form['tip']
    fechaI=request.form['fechaI']
    fechaC=request.form['fechaC']

    print(tipoActividad)

    cursor= db.database.cursor()
    sql = "update Actividades set idTipoAcFK=%s, TituloActividad=%s, descripcionActividad=%s, fechaInicio=%s, fechaCierre=%s where idActividad=%s"
    data=(tipoActividad, titulo, descripcion,fechaI,fechaC,idActividad)
    cursor.execute(sql, data)
    db.database.commit()

    cursor.execute("select day(%s) as dia, month(%s) as mes, monthname(%s) as nombreMes;",(fechaI,fechaI,fechaI))
    account2 = cursor.fetchone()
    cursor.close()

    return redirect(url_for("evento",mes=account2[2],dia=account2[0]))

#eliminar evento
@app.route('/eliminarEvent/<string:idActividad>')
def eliminarEvent(idActividad):

    cursor= db.database.cursor()

    cursor.execute("select day(fechaInicio) as dia, month(fechaInicio) as mes, monthname(fechaInicio) as nombreMes where idActividad=%s;",(idActividad))
    account2 = cursor.fetchone()
    cursor.close()


    cursor.execute("delete from actividades where idActividad=%s", (idActividad,))
    db.database.commit()

    cursor.close()

    return redirect(url_for("evento",mes=account2[2],dia=account2[0]))

#agregar evento
@app.route('/addEvent', methods=["post"])
def addEvent():

    titulo=request.form['til']
    descripcion=request.form['des']
    tipoActividad=request.form['tip']
    fechaI=request.form['fechaI']
    fechaC=request.form['fechaC']

    print(tipoActividad)

    cursor= db.database.cursor()
    sql = "insert into Actividades (idTipoAcFK, TituloActividad, descripcionActividad, fechaInicio, fechaCierre) values (%s,%s,%s,%s,%s);"
    data=(tipoActividad, titulo, descripcion,fechaI,fechaC)
    cursor.execute(sql, data)
    db.database.commit()

    cursor.execute("select day(%s) as dia, month(%s) as mes, monthname(%s) as nombreMes;",(fechaI,fechaI,fechaI))
    account2 = cursor.fetchone()
    cursor.close()

    return redirect(url_for("evento",mes=account2[2],dia=account2[0]))

#reportes
@app.route('/reportes')
def reportes():

    logueado2=session['logueado']
    print(logueado2)
    if logueado2==False:

        correo=session['correo2']
        print(correo)
        password2=session['password2']
        print(password2)

        cursor= db.database.cursor()
        cursor.execute("select rol, primerNombre, segundoNombre, primerApellido,segundoApellido from Usuario inner join rol on usuario.idRolFK=rol.idRol where Correo= %s and contraseña=%s; ", (correo,password2,))
        account = cursor.fetchall()
        insertObject5= []
        columnNames = [column[0] for column in cursor.description]
        for record5 in account:
            insertObject5.append(dict(zip(columnNames, record5)))

        cursor.execute("select * from periodo;")
        account = cursor.fetchall()
        periodo= []
        columnNames = [column[0] for column in cursor.description]
        for record in account:
            periodo.append(dict(zip(columnNames, record)))

        cursor.execute("select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;")
        myresult= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record)))

        cursor.execute("select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 group by numCursoFK;")
        myresult2= cursor.fetchall()
        #Convertir los dato a diccionario
        insertObject2= []
        columnNames = [column[0] for column in cursor.description]
        for record2 in myresult2:
            insertObject2.append(dict(zip(columnNames, record2)))


        return render_template('views/ReportesRector.html', data5=insertObject5, periodo=periodo, data=insertObject, data2=insertObject2)

    else:
        return render_template("views/login.html", mensaje="Debes iniciar Sesion")

#generar reporte por curso
@app.route('/reportePorCurso/<string:numCurso>/<string:idPeriodo>')
def reportePorCurso(numCurso, idPeriodo): 
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template('views/plantillaBoletin.html')
    periodo= idPeriodo
    print(periodo)


    cursor= db.database.cursor()

    cursor.execute("select * from usuario where numCursoFK=%s;",(numCurso,))
    myresult2= cursor.fetchall()
    #Convertir los dato a diccionario
    estudiantes= []
    columnNames = [column[0] for column in cursor.description]
    for record2 in myresult2:
        estudiantes.append(dict(zip(columnNames, record2)))

    print(estudiantes)
    print(len(estudiantes))

    for estudiante in range(len(estudiantes)):

        print(estudiantes[estudiante]['idUsuario'])

        cursor.execute("SELECT u.idUsuario, u.primerNombre, u.segundoNombre, u.primerApellido, u.segundoApellido, u.numCursoFK,m.idMateria, m.nombreMate, round((SELECT (AVG(nota) * 0.25) FROM calificacion AS c1 WHERE c1.idEstudianteFK = u.idUsuario AND c1.idTipoNotaFK = 1 and idPeriodoFK=%s and u.numCursoFK=%s),2) AS nota1, round((SELECT (AVG(nota) * 0.25) FROM calificacion AS c2 WHERE c2.idEstudianteFK = u.idUsuario AND c2.idTipoNotaFK = 2 and idPeriodoFK=%s and u.numCursoFK=%s),2) AS nota2, round((SELECT (AVG(nota) * 0.45) FROM calificacion AS c3 WHERE c3.idEstudianteFK = u.idUsuario AND c3.idTipoNotaFK = 3 and idPeriodoFK=%s and u.numCursoFK=%s),2) AS nota3, round((SELECT (AVG(nota) * 0.05) FROM calificacion AS c4 WHERE c4.idEstudianteFK = u.idUsuario AND c4.idTipoNotaFK = 4 and idPeriodoFK=%s and u.numCursoFK=%s),2) AS nota4, round(((SELECT (AVG(nota) * 0.25) FROM calificacion AS c1 WHERE c1.idEstudianteFK = u.idUsuario AND c1.idTipoNotaFK = 1 and idPeriodoFK=%s and u.numCursoFK=%s) + (SELECT (AVG(nota) * 0.25) FROM calificacion AS c2 WHERE c2.idEstudianteFK = u.idUsuario AND c2.idTipoNotaFK = 2 and idPeriodoFK=%s and u.numCursoFK=%s) + (SELECT (AVG(nota) * 0.45) FROM calificacion AS c3 WHERE c3.idEstudianteFK = u.idUsuario AND c3.idTipoNotaFK = 3 and idPeriodoFK=%s and u.numCursoFK=%s) + (SELECT (AVG(nota) * 0.05) FROM calificacion AS c4 WHERE c4.idEstudianteFK = u.idUsuario AND c4.idTipoNotaFK = 4 and idPeriodoFK=%s and u.numCursoFK=%s)),2) AS notaFinal FROM usuario AS u INNER JOIN calificacion AS c ON c.idEstudianteFK = u.idUsuario INNER JOIN materia AS m ON c.idMateriaFK = m.idMateria where  u.numCursoFK=%s and m.numCursoFK=%s and u.idUsuario=%s group by u.idUsuario, u.primerNombre, u.segundoNombre, u.primerApellido, u.segundoApellido, m.nombreMate;",(periodo,numCurso,periodo,numCurso,periodo,numCurso,periodo,numCurso,periodo,numCurso,periodo,numCurso,periodo,numCurso,periodo,numCurso,numCurso, numCurso, estudiantes[estudiante]['idUsuario']))
        account = cursor.fetchall()
        insertObject= []
        columnNames = [column[0] for column in cursor.description]
        for record in account:
            insertObject.append(dict(zip(columnNames, record)))

        contenido={
            'idUsuario':estudiantes[estudiante]['idUsuario'],
            'primerNombre':estudiantes[estudiante]['primerNombre'],
            'segundoNombre':estudiantes[estudiante]['segundoNombre'],
            'primerApellido':estudiantes[estudiante]['primerApellido'],
            'segundoApellido':estudiantes[estudiante]['segundoApellido'],
            'curso': numCurso,
            'periodo':periodo
        }
        
        insertObject2= []
        for insertObj in range(len(insertObject)):

            if insertObject[insertObj]['notaFinal'] is not None and insertObject[insertObj]['notaFinal']>4:
                cursor.execute("select idMateria, nombreMate,  tipoObservacion, descripcion from observaciones as o inner join materia as m on o.idMateriaFK=m.idMateria inner join tipoObservacion as t on o.idTipoObFK=t.idTipoOb where idMateria=%s and tipoObservacion='Fortalezas';",(insertObject[insertObj]['idMateria'],))

                observaciones= cursor.fetchall()
                #Convertir los dato a diccionario
                columnNames = [column[0] for column in cursor.description]
                for record2 in observaciones:
                    insertObject2.append(dict(zip(columnNames, record2)))  
            else:
                cursor.execute("select idMateria, nombreMate,  tipoObservacion, descripcion from observaciones as o inner join materia as m on o.idMateriaFK=m.idMateria inner join tipoObservacion as t on o.idTipoObFK=t.idTipoOb where idMateria=%s and tipoObservacion='Debilidades';",(insertObject[insertObj]['idMateria'],))

                observaciones= cursor.fetchall()
                #Convertir los dato a diccionario
                columnNames = [column[0] for column in cursor.description]
                for record2 in observaciones:
                    insertObject2.append(dict(zip(columnNames, record2)))  

            html = template.render(contenido, materias=insertObject, observaciones=insertObject2)

            pdf_filename = f'{estudiantes[estudiante]["idUsuario"]}_{estudiantes[estudiante]["primerNombre"]}_{estudiantes[estudiante]["segundoNombre"]}_reporte.pdf'
            
            options={
                'page-size':'A5',
                'margin-top':'0.1in',
                'margin-right':'0.1in',
                'margin-bottom':'0.1in',
                'margin-left':'0.1in'
            }

            pdfkit.from_string(html, pdf_filename, options=options)

    cursor.close()
    return redirect(url_for('reportes'))



@app.route('/cerrarSesion')
def cerrarSesion():

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.secret_key='123456'
    app.run(debug=True )
