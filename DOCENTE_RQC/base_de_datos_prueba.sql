create database sistemaEducativo2;
use sistemaEducativo2;

-------------- Creacion de tablas-------------------------------------------------------------------------
create table Rol(
idRol int primary key auto_increment,
rol varchar(30),
estadoRol varchar(20)
);


create table Usuario(
idUsuario int primary key auto_increment,
primerNombre varchar(50) not null,
segundoNombre varchar(50) not null,
primerApellido varchar(50) not null,
segundoApellido varchar(50) not null,
genero varchar(20) not null, 
DepNacimiento varchar(20) not null,
municipioNaci varchar(20) not null,
FechaNaci date not null,
edad int not null,
tipoDocUsuFK int not null,
numberDocu int not null,
barrio varchar(20) not null,
estrato int not null,
direccion varchar(50) not null,
numeroF int null,
numeroC int null,
afiliacion varchar(20) not null,
eps varchar(20) not null, 
LugarA varchar(20) not null,
RH varchar(20) not null, 
numCursoFK int,
Correo varchar(50) not null,
contraseña varchar(50) not null,
estadoUsu varchar(20) not null,
idRolFK int not null);

create table tipoDoc(
idTipoDoc int primary key auto_increment,
tipoDocUsu varchar(50) not null,
estado varchar(20)
);

create table Curso(
NumCurso int primary key,
idDocenteFK int not null,
Numero_Estudiantes int not null
);

create table Materia(
idMateria int primary key auto_increment,
nombreMate varchar(30) not null,
idDocenteFK int not null,
numCursoFK int not null
);


create table Asistencia (
idAsistencia int primary key auto_increment,
idMateriaFK int not null,
idPeriodoFK int not null,
fecha date not null,
idEstudianteFK int not null,
asistencia boolean not null
);

create table Calificacion(
idCali int primary key auto_increment,
idMateriaFK int not null,
idEstudianteFK int not null,
idTipoNotaFK int not null,
idPeriodoFK int not null,
nota float not null,
fecha date not null
);


create table Actividades(
idActividad int primary key auto_increment,
idMateriaFK int null,
idTipoAcFK int not null,
TituloActividad varchar(50) not null,
descripcionActividad varchar(150)  not null,
fechaInicio datetime  not null,
fechaCierre datetime  not null
);


create table periodo(
idPeriodo int primary key auto_increment,
FechaInicio date not null,
FechaCierre date not null
);


create table TipoActividad(
idTipoAc int primary key auto_increment,
tipoActividad  varchar(50) not null,
estado varchar(30)
);

create table TipoNo(
idTipoNo int primary key auto_increment,
TipoNota  varchar(50) not null,
porcentaje int,
estado varchar(30)
);

create table observaciones(
idObservacion int primary key auto_increment,
idMateriaFK int not null,
idTipoObFK int not null,
descripcion varchar(200) not null
);

create table TipoObservacion(
idTipoOb int primary key auto_increment,
TipoObservacion enum('Debilidades','Fortalezas') not null,
estado varchar(30)
);



------------- Relaciones entre tablas-----------------------------

------------ Curso -------------------
alter table Curso add constraint CursoDocente
foreign key(idDocenteFK) references Usuario(idUsuario);

------------- Materia--------------------
alter table Materia add constraint MateriaUsuario
foreign key(idDocenteFK) references Usuario(idUsuario);

alter table Materia add constraint MateriaCurso
foreign key(numCursoFK) references Curso(numCurso);

------------ Asisencia-----------------------
alter table Asistencia add constraint AsistenciaMateria
foreign key(idMateriaFK) references Materia(idMateria);

alter table Asistencia add constraint AsistenciaUsuario
foreign key(idEstudianteFK) references Usuario(idUsuario);

alter table Asistencia add constraint AsistenciaPeriodo
foreign key(idPeriodoFK) references periodo(idPeriodo);

----------- Calificacion------------------------------------
alter table Calificacion add constraint CalificacionMateria
foreign key(idMateriaFK) references Materia(idMateria);

alter table Calificacion add constraint CalificacionEstudiante
foreign key(idEstudianteFK) references Usuario(idUsuario);

alter table Calificacion add constraint CalificacionTipoNo
foreign key(idTipoNotaFK) references TipoNo(idTipoNo);

alter table Calificacion add constraint CalificacionPeriodo
foreign key(idPeriodoFK) references periodo(idPeriodo);



----------- Usuario-------------------------------------------
alter table Usuario	 add constraint UsuarioCurso
foreign key(numCursoFK) references Curso(numCurso);

alter table Usuario	 add constraint UsuarioRol
foreign key(idRolFK) references Rol(idRol);

alter table Usuario	 add constraint UsuarioTipoDoc
foreign key(tipoDocUsuFK) references TipoDoc(idTipoDoc);


---------- Actividades-------------------------------------------
alter table Actividades add constraint ActividadesMateria
foreign key(idMateriaFK) references Materia(idMateria);

alter table Actividades add constraint ActividadesTipoActividad
foreign key(idTipoAcFK) references TipoActividad(idTipoAc);

--------- observaciones-----------------------------------------
alter table observaciones add constraint obsevacionesMateria
foreign key(idMateriaFK) references Materia(idMateria);

alter table observaciones add constraint obsevacionesTipoObservacion
foreign key(idTipoObFK) references TipoObservacion(idTipoOb);

-------- tablla para los contenidos -------------------------------
create table contenido(
idcont int,
titulo varchar(200),
descripcion varchar(200)
);

insert into contenido values(1,"Colegio Naciones Unidas", null);
insert into contenido values(2,"Coro", "¡Somos jóvenes, miembros activos, base prima de la sociedad, en camino de lucha vivimos, fundamento para progresar! Estrofas I Competentes, capaces, creativos, en el trabajo en equipo es acción.");
insert into contenido values(2,"Estrofa III", "Al colegio Naciones Unidas le debemos una gran lealtad, lucharemos por el bien de la patria a favor de nuestra comunidad. Estrofa IV Los principios se enmarcan seguidos de actitudes que infunden valor, la enseñanza será compromiso, La certeza de un mundo mejor");
insert into contenido values(2,"Estrofa I", "Competentes, capaces, creativos, en el trabajo en equipo es acción, forjaremos por siempre en las almas, a que viva en nosotros la unión.");
insert into contenido values(2,"Estrofa IV", "Los principios se enmarcan seguidos de actitudes que infunden valor, la enseñanza será compromiso, La certeza de un mundo mejor");
insert into contenido values(2,"Estrofa II", "Esperanza, liderazgo y vida, las primicias de la juventud, presurosa siguiendo la línea Invariable de la rectitud.");
insert into contenido values(3,"Educación, Ciencia, Cultura y deporte para trascender", "Somos la familia naciones unidas");

-- inserciones

insert into rol values(1,'Estudiante','Activo');
insert into rol values(2,'Coordinador','Activo');
insert into rol values(3,'Docente','Activo');

insert into tipoDoc values(1,'Tarjeta de identidad','Activo');
insert into tipoDoc values(2,'Cedula de ciudadania','Activo');
insert into tipoDoc values(3,'Pasaporte','Activo');
insert into tipoDoc values(4,'registro Civil','Activo');

insert into TipoActividad values(1, 'Trabajo en clase', 'Activo');
insert into TipoActividad values(2, 'Izada de bandera', 'Activo');
insert into TipoActividad values(3, 'Salida Pedagogica', 'Activo');

insert into TipoObservacion values(1, 'Fortalezas', 'Activo');
insert into TipoObservacion values(2, 'Debilidades', 'Activo');


insert into TipoNo values(1, "Primera Evaluacion Trimestral", 35, 'Activo');
insert into TipoNo values(2, "Segunda Evaluacion Trimestral", 35, 'Activo');
insert into TipoNo values(3, "TRabajo en clase", 25, 'Activo');
insert into TipoNo values(4, "Autoevaluación", 5, 'Activo');

insert into periodo values(1, '2023-02-20','2023-05-20');
insert into periodo values(2, '2023-05-21','2023-08-20');
insert into periodo values(3, '2023-08-22','2023-11-22');

select * from curso;

insert into Usuario ( primerNombre, segundoNombre, primerApellido, segundoApellido, genero, DepNacimiento, municipioNaci, FechaNaci, edad, tipoDocUsuFK, numberDocu, barrio, estrato, direccion, numeroC, afiliacion, eps, LugarA, RH, Correo, contraseña, estadoUsu, idRolFK) 
values ('Yeison','David','Rodriguez','Rodriguez','Masculino','Cundinamarca','Bogota','2005-08-20',18,2,1014859746,'Bellavista',3,'Carrera 68b #70-33',3138718238,'Si','Capital Salud','Hospital de la 80','O+','Yeison@gmail.com','Yeison','Activo',3);


insert into Curso values(601, 1,30);
insert into Curso values(701, 1,30);
insert into Curso values(801, 1,30);
insert into Curso values(901, 1,30);
insert into Curso values(1001,1 ,30);
insert into Curso values(1101,1 ,30);


insert into Usuario ( primerNombre, segundoNombre, primerApellido, segundoApellido, genero, DepNacimiento, municipioNaci,FechaNaci, edad, tipoDocUsuFK, numberDocu, barrio, estrato, direccion, numeroC, afiliacion, eps, LugarA, RH, Correo, contraseña, estadoUsu, idRolFK) 
values ('Juan','Camilo','Rodriguez','Rodriguez','Masculino','Cundinamarca','Bogota','2003-07-27',20,2,1014859746,'Bellavista',3,'Carrera 68b #70-33',3138718238,'Si','Capital Salud','Hospital de la 80','O+','Camilo@gmail.com','Camilo','Activo',3);

insert into materia values (1, 'Matematicas', 1, 1101);
insert into materia values (2, 'Matematicas', 2, 801);
insert into materia values (3, 'Matematicas', 1, 701);
insert into materia values (4, 'Matematicas', 2, 601);
insert into materia values (5, 'Matematicas', 1, 1001);
insert into materia values (6, 'Matematicas', 2, 1101);
insert into materia values (7, 'Matematicas', 11, 901);
insert into materia values (8, 'Español', 1, 601);

select * from materia;

select * from usuario;
select m.numCursoFK, primerNombre, segundoNombre, primerApellido, segundoApellido, (select count(idUsuario) from usuario  where idRolFK=1 group by numCursoFK) as numeroEstudiantes from materia as m
inner join curso on m.numCursoFK=curso.numCurso inner join usuario on curso.idDocenteFK=usuario.idUsuario where  idUsuario=2;
select * from materia where idDocenteFK=2;
select Numcurso, idUsuario, primerNombre, segundoNombre, primerApellido,segundoApellido from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;
select * from materia where idDocenteFK=1;
select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 group by numCursoFK;
select idRolFK from usuario where idUsuario=2;

insert into asistencia values(1, 1, 1, '2023-03-20', 3, 0);
insert into asistencia values(2, 2, 2, '2023-05-23', 3, 1);
insert into asistencia values(3, 3, 3, '2023-09-20', 3, 0);
insert into asistencia values(4, 4, 1, '2023-03-13', 3, 1);
insert into asistencia values(5, 5, 2, '2023-07-23', 3, 0);


insert into Actividades values(1, 1, 1, "Trabajo en clase", "Se hara un trabajo acerca de ecuaciones lineales", '2023-05-20 12:00:00', '2023-05-20 14:00:00');
insert into Actividades values(2, 2, 1, "Trabajo en clase", "Se hara un trabajo acerca de ecuaciones diferenciales", '2023-05-20 08:30:00', '2023-05-20 10:30:00');
insert into Actividades values(3, 3, 2, "Izada de bandera", "Se premiaran a los estudiante que son lo mejor de lo mejor :v", '2023-05-23 12:00:00', '2023-05-23 14:00:00');
insert into Actividades values(4, 4, 3, "Salida al salitre magico", "Se hara una salida al salitre magico", '2023-05-20 8:00:00', '2023-05-20 13:00:00');
insert into Actividades values(5, 5, 1, "Trabajo en clase", "Se hara un trabajo acerca de ecuaciones lineales", '2023-05-20 12:00:00', '2023-05-20 14:00:00');

select * from actividades;
select  monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad from Actividades where monthname(fechaInicio)='May' and day(fechaInicio)=20;
select day(now()) as dia, month('May') as mes;

    
insert into observaciones values(1, 1, 1, "Es muy bueno");
insert into observaciones values(2, 1, 2, "Se le dificulta mucho la materia");
insert into observaciones values(3, 2, 1, "Es muy bueno en la materia2");
insert into observaciones values(4, 2, 2, "Se le dificulta mucho la materia2");
insert into observaciones values(5, 3, 1, "Es muy bueno");
insert into observaciones values(6, 3, 2, "Se le dificulta mucho la materia3");
insert into observaciones values(7, 4, 1, "Es muy bueno");
insert into observaciones values(8, 4, 2, "Se le dificulta mucho la materia3");
insert into observaciones values(9, 8, 1, "Es muy bueno en la materia8");
insert into observaciones values(10, 8, 2, "Se le dificulta mucho la materia8");


insert into calificacion values(1, 1, 4, 1, 1, 3.5, '2023-05-10');
insert into calificacion values(2, 2, 4, 3, 1, 4.0, '2023-08-10');
insert into calificacion values(3, 3, 4, 1, 1, 3.5, '2023-05-10');
insert into calificacion values(4, 4, 4, 2, 2, 4.5, '2023-05-10');
insert into calificacion values(5, 5, 4, 1, 1, 3.8, '2023-05-10');

	create View DiasMeses
	(Dia, Mes)
	As
	 SELECT distinct
		DAYOFMONTH(DATE_ADD(LAST_DAY(CONCAT(YEAR(NOW()), '-', m.month, '-01')), INTERVAL n DAY)) AS Dia,
		MONTHNAME(CONCAT(YEAR(NOW()), '-', m.month, '-01')) AS Mes
	FROM
		(SELECT 1 AS month
		 UNION ALL SELECT 2
		 UNION ALL SELECT 3
		 UNION ALL SELECT 4
		 UNION ALL SELECT 5
		 UNION ALL SELECT 6
		 UNION ALL SELECT 7
		 UNION ALL SELECT 8
		 UNION ALL SELECT 9
		 UNION ALL SELECT 10
		 UNION ALL SELECT 11
		 UNION ALL SELECT 12) AS m
	JOIN
		(SELECT 0 AS n
		 UNION ALL SELECT 1
		 UNION ALL SELECT 2
		 UNION ALL SELECT 3
		 UNION ALL SELECT 4
		 UNION ALL SELECT 5
		 UNION ALL SELECT 6
		 UNION ALL SELECT 7
		 UNION ALL SELECT 8
		 UNION ALL SELECT 9
		 UNION ALL SELECT 10
		 UNION ALL SELECT 11
		 UNION ALL SELECT 12
		 UNION ALL SELECT 13
		 UNION ALL SELECT 14
		 UNION ALL SELECT 15
		 UNION ALL SELECT 16
		 UNION ALL SELECT 17
		 UNION ALL SELECT 18
		 UNION ALL SELECT 19
		 UNION ALL SELECT 20
		 UNION ALL SELECT 21
		 UNION ALL SELECT 22
		 UNION ALL SELECT 23
		 UNION ALL SELECT 24
		 UNION ALL SELECT 25
		 UNION ALL SELECT 26
		 UNION ALL SELECT 27
		 UNION ALL SELECT 28
		 UNION ALL SELECT 29
		 UNION ALL SELECT 30) AS Numbers
	WHERE
		DAYOFMONTH(DATE_ADD(LAST_DAY(CONCAT(YEAR(NOW()), '-', m.month, '-01')), INTERVAL n DAY)) <= DAY(LAST_DAY(CONCAT(YEAR(NOW()), '-', m.month, '-01')))
	ORDER BY
		Mes, Dia;

select * from usuario;
select Numcurso, nombreUsu, apellidoUsu from curso inner join usuario on curso.idDocenteFK=usuario.idusuario;
Select idUsuario ,nombreUsu, apellidoUsu, estadoUsu from usuario where idRolFK=3 and estadoUsu='Activo';
use sistemaeducativo2;
select Numcurso, idUsuario, nombreUsu, apellidoUsu, nombreMate from curso inner join usuario on curso.idDocenteFK=usuario.idusuario inner join materia on materia.numCursoFK=curso.numCurso where numCurso=1101 group by numCurso;
select numCursoFK, count(idUsuario) as numeroEstudiantes from usuario  where idRolFK=1 and numCursoFK=1101;


select idUsuario, tipoDocUsu, numDocUsu, nombreUsu, apellidoUsu, telefonoUsu, direccionUsu, numCursoFK, correoUsu, ClaveUsuario, estadoUsu, rol from usuario as u 
inner join rol as r on u.idRolFK=r.idRol inner join tipoDoc as t on u.tipoDocUsuFK=t.idTipoDoc where numCursoFK=601;
update usuario set ClaveUsuario='oscarin' where idUsuario=8;
-- select idRolFK, count(idUsuario) as numeroEstudiantes from usuario group by idRolFK;
-- select rol, idRolFK, count(idUsuario) as numeroEstudiantes from usuario inner join rol on usuario.idRolFK=rol.idRol group by idRolFK;
-- select rol, nombreUsu from Usuario inner join rol on usuario.idRolFK=rol.idRol where correoUsu= "yeisonrodrigueznacun@gmail.com" and ClaveUsuario="Yeisonxd:v";
-- select * from usuario;
-- select * from materia;
-- select count(idMateria) from materia;
use sistemaeducativo2;

select * from Actividades;
insert into Actividades (idTipoAcFK, TituloActividad, descripcionActividad, fechaInicio, fechaCierre) values ();
select idActividad, monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, tipoActividad, time(fechaInicio) as inicio, time(fechaCierre) as cierre from Actividades inner join TipoActividad as t on Actividades.idTipoAcFK=t.idTipoAc  where idTipoAcFK in (2,3);
select tipoActividad, idTipoAc from tipoActividad where idTipoAc in (2,3);

select * from asistencia;
select * from observaciones;
select * from calificacion;
select * from tipoNo;
select * from materia;
select * from usuario;

insert into calificacion values(1, 1, 3, 1, 1, 5, '2023-05-10');
insert into calificacion values(2, 1, 3, 2, 1, 5, '2023-08-10');
insert into calificacion values(3, 1, 3, 3, 1, 5, '2023-05-10');
insert into calificacion values(4, 1, 3, 3, 1, 5, '2023-05-10');
insert into calificacion values(5, 1, 3, 4, 1, 5, '2023-05-10');

insert into calificacion values(6, 2, 4, 1, 1, 4, '2023-05-10');
insert into calificacion values(7, 2, 4, 2, 1, 3, '2023-08-10');
insert into calificacion values(8, 2, 4, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(9, 2, 4, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(10, 2, 4, 4, 1, 5, '2023-05-10');

insert into calificacion values(11, 3, 9, 1, 1, 4, '2023-05-10');
insert into calificacion values(12, 3, 9, 2, 1, 3, '2023-08-10');
insert into calificacion values(13, 3, 9, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(14, 3, 9, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(15, 3, 9, 4, 1, 5, '2023-05-10');

insert into calificacion values(16, 8, 3, 1, 1, 4, '2023-05-10');
insert into calificacion values(17, 8, 3, 2, 1, 3, '2023-08-10');
insert into calificacion values(18, 8, 3, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(19, 8, 3, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(20, 8, 3, 4, 1, 5, '2023-05-10');

insert into calificacion values(21, 4, 3, 1, 1, 4, '2023-05-10');
insert into calificacion values(22, 4, 3, 2, 1, 3, '2023-08-10');
insert into calificacion values(23, 4, 3, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(24, 4, 3, 3, 1, 4.5, '2023-05-10');
insert into calificacion values(25, 4, 3, 4, 1, 5, '2023-05-10');

insert into calificacion values(26, 4, 4, 1, 1, 5, '2023-05-10');
insert into calificacion values(27, 4, 4, 2, 1, 5, '2023-08-10');
insert into calificacion values(28, 4, 4, 3, 1, 5, '2023-05-10');
insert into calificacion values(29, 4, 4, 3, 1, 5, '2023-05-10');
insert into calificacion values(30, 4, 4, 4, 1, 5, '2023-05-10');

insert into calificacion values(31, 8, 4, 1, 1, 5, '2023-05-10');
insert into calificacion values(32, 8, 4, 2, 1, 5, '2023-08-10');
insert into calificacion values(33, 8, 4, 3, 1, 5, '2023-05-10');
insert into calificacion values(34, 8, 4, 3, 1, 5, '2023-05-10');
insert into calificacion values(35, 8, 4, 4, 1, 5, '2023-05-10');

insert into calificacion values(36, 4, 5, 1, 1, 5, '2023-05-10');
insert into calificacion values(37, 4, 5, 2, 1, 5, '2023-08-10');
insert into calificacion values(38, 4, 5, 3, 1, 5, '2023-05-10');
insert into calificacion values(39, 4, 5, 3, 1, 5, '2023-05-10');
insert into calificacion values(40, 4, 5, 4, 1, 5, '2023-05-10');

insert into calificacion values(41, 8, 5, 1, 1, 5, '2023-05-10');
insert into calificacion values(42, 8, 5, 2, 1, 5, '2023-08-10');
insert into calificacion values(43, 8, 5, 3, 1, 5, '2023-05-10');
insert into calificacion values(44, 8, 5, 3, 1, 5, '2023-05-10');
insert into calificacion values(45, 8, 5, 4, 1, 5, '2023-05-10');

insert into calificacion values(46, 4, 6, 1, 1, 5, '2023-05-10');
insert into calificacion values(47, 4, 6, 2, 1, 5, '2023-08-10');
insert into calificacion values(48, 4, 6, 3, 1, 5, '2023-05-10');
insert into calificacion values(49, 4, 6, 3, 1, 5, '2023-05-10');
insert into calificacion values(50, 4, 6, 4, 1, 5, '2023-05-10');

insert into calificacion values(51, 8, 6, 1, 1, 3, '2023-05-10');
insert into calificacion values(52, 8, 6, 2, 1, 2, '2023-08-10');
insert into calificacion values(53, 8, 6, 3, 1, 1, '2023-05-10');
insert into calificacion values(54, 8, 6, 3, 1, 2, '2023-05-10');
insert into calificacion values(55, 8, 6, 4, 1, 2, '2023-05-10');

use sistemaeducativo2


-- Procedimientos almacenados para los reportes --
Delimiter //
create procedure notaDefinitiva
(idPeriodo int, numCurso int, idEstudiante int)
begin
	SELECT
		u.idUsuario,
		u.primerNombre,
		u.segundoNombre,
		u.primerApellido,
		u.segundoApellido,
		u.numCursoFK,
		m.idMateria,
		m.nombreMate,

		round((SELECT (AVG(nota) * 0.25) FROM calificacion AS c1 WHERE c1.idEstudianteFK = u.idUsuario AND c1.idTipoNotaFK = 1 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso),2) AS nota1,
		(SELECT (AVG(nota) * 0.25) FROM calificacion AS c2 WHERE c2.idEstudianteFK = u.idUsuario AND c2.idTipoNotaFK = 2 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) AS nota2,
		(SELECT (AVG(nota) * 0.45) FROM calificacion AS c3 WHERE c3.idEstudianteFK = u.idUsuario AND c3.idTipoNotaFK = 3 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) AS nota3,
		(SELECT (AVG(nota) * 0.05) FROM calificacion AS c4 WHERE c4.idEstudianteFK = u.idUsuario AND c4.idTipoNotaFK = 4 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) AS nota4,
		((SELECT (AVG(nota) * 0.25) FROM calificacion AS c1 WHERE c1.idEstudianteFK = u.idUsuario AND c1.idTipoNotaFK = 1 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) +
		 (SELECT (AVG(nota) * 0.25) FROM calificacion AS c2 WHERE c2.idEstudianteFK = u.idUsuario AND c2.idTipoNotaFK = 2 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) +
		 (SELECT (AVG(nota) * 0.45) FROM calificacion AS c3 WHERE c3.idEstudianteFK = u.idUsuario AND c3.idTipoNotaFK = 3 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso) +
		 (SELECT (AVG(nota) * 0.05) FROM calificacion AS c4 WHERE c4.idEstudianteFK = u.idUsuario AND c4.idTipoNotaFK = 4 and idPeriodoFK=idPeriodo and u.numCursoFK=numCurso)) AS notaFinal
	FROM
		usuario AS u
	INNER JOIN
		calificacion AS c ON c.idEstudianteFK = u.idUsuario
	INNER JOIN
		materia AS m ON c.idMateriaFK = m.idMateria
	where 
		u.numCursoFK=numCurso and m.numCursoFK=numCurso and u.idUsuario=idEstudiante
	group by
		u.idUsuario,
		u.primerNombre,
		u.segundoNombre,
		u.primerApellido,
		u.segundoApellido,	
		m.nombreMate;
    
End;
//
call notaDefinitiva(1,901,3);

select * from calificacion
select * from actividades
    
Delimiter //
create procedure FortalezaMateria
(idMateria2 int)
begin
	select idMateria, nombreMate,  tipoObservacion, descripcion from observaciones as o inner join materia as m on o.idMateriaFK=m.idMateria inner join tipoObservacion as t on o.idTipoObFK=t.idTipoOb where idMateria=idMateria2 and tipoObservacion='Fortalezas';
end;
//
Delimiter //
create procedure DebilidadMateria
(idMateria2 int)
begin
	select idMateria, nombreMate,  tipoObservacion, descripcion from observaciones as o inner join materia as m on o.idMateriaFK=m.idMateria inner join tipoObservacion as t on o.idTipoObFK=t.idTipoOb where idMateria=idMateria2 and tipoObservacion='Debilidades';
end;
//



SELECT WEEK(NOW()) AS SemanaActual;
SELECT monthname(now()) mes,
  day(DATE_ADD(CURDATE(), INTERVAL 0-DAYOFWEEK(CURDATE()) DAY)) AS Sabado,
  day(DATE_ADD(CURDATE(), INTERVAL 1-DAYOFWEEK(CURDATE()) DAY)) AS Domingo,
  day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,
  day(DATE_ADD(CURDATE(), INTERVAL 3-DAYOFWEEK(CURDATE()) DAY)) AS Martes,
  day(DATE_ADD(CURDATE(), INTERVAL 4-DAYOFWEEK(CURDATE()) DAY)) AS Miercoles,
  day(DATE_ADD(CURDATE(), INTERVAL 5-DAYOFWEEK(CURDATE()) DAY)) AS Jueves,
  day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes;

    select * from actividades;
    
    
insert into Actividades values(10, 3, 1, 'Izada de bandera', 'Se premiara a lo estudiante que son lo mejor de lo mejor', '2023-09-18 06:10:00', '2023-09-17 10:10:00');
insert into Actividades values(11, 3, 1, 'Izada de bandera', 'Se premiara a lo estudiante que son lo mejor de lo mejor', '2023-09-18 06:10:00', '2023-09-18 10:10:00');
insert into Actividades values(12, 3, 2, 'Izada de bandera', 'Se premiara a lo estudiante que son lo mejor de lo mejor', '2023-09-18 06:10:00', '2023-09-18 10:10:00');
insert into Actividades values(13, 3, 3, 'Salida al parque Simon Bolivar', 'Se premiara a lo estudiante que son lo mejor de lo mejor', '2023-09-18 06:10:00', '2023-09-18 10:10:00');

    
select monthname(fechaInicio) as mes,day(fechaInicio) as dia, TituloActividad, descripcionActividad, idTipoAcFK, day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) AS Lunes,   day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY)) AS Viernes from Actividades where idTipoAcFK in ('2','3') and day(fechaInicio) BETWEEN day(DATE_ADD(CURDATE(), INTERVAL 2-DAYOFWEEK(CURDATE()) DAY)) and day(DATE_ADD(CURDATE(), INTERVAL 6-DAYOFWEEK(CURDATE()) DAY));