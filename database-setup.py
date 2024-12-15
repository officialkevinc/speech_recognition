import sqlite3

conn = sqlite3.connect('students.db')

cursor = conn.cursor()

cursor.execute("CREATE TABLE students(number integer, first_name text, last_name text, grupo text, boleta integer, estado text)")

#cursor.execute("""INSERT INTO students VALUES ('Kevin Carlos', 'Rojas Miron', '5CV32', '22')""")

#cursor.execute("SELECT * FROM students WHERE grupo='5CV32'")

#print(cursor.fetchall())

alumnos = [
    (1, "Eduardo", "Arellano Ceballos", "5CV32", 2021351122, "Puntual"),
    (2, "Dante Joel", "Cornozado Jimenez", "5CV32", 2022351340, "Puntual"),
    (3, "William", "Cruz Hernandez", "5CV32", 2022350596, "Puntual"),
    (4, "Jordy Alejandro", "Cuellar Bravo", "5CV32", 2021350002, "Puntual"),
    (5, "Kenia", "Godinez Espinoza", "5CV32", 2022350858, "Puntual"),
    (6, "Jose Alberto", "Gonzalez Orta", "5CV32", 2022350192, "Puntual"),
    (7, "Adilenne Guadalupe", "Gonzalez Velazquez", "5CV32", 2022351548, "Puntual"),
    (8, "Jorge Luis", "Guevara Martinez", "5CV32", 2023351344, "Puntual"),
    (9, "Diego Jesus", "Gutierrez Delgado", "5CV32", 2023350018, "Puntual"),
    (10, "Johan Said", "Hernandez Dominguez", "5CV32", 2022351165, "Puntual"),
    (11, "Mario Alberto", "Hurtado Mendoza", "5CV32", 2017351121, "Puntual"),
    (12, "Jesus Emmanuel", "Iriarte Hernandez", "5CV32", 2015351062, "Puntual"),
    (13, "Oasis Zamirah", "Lara Ramirez", "5CV32", 2022350312, "Puntual"),
    (14, "Joan Manuel", "Lopez Hernandez", "5CV32", 2022350423, "Puntual"),
    (15, "Jorge David", "Lopez Martinez", "5CV32", 2021351266, "Puntual"),
    (16, "Jose Armando", "Macias Huerta", "5CV32", 2022350366, "Puntual"),
    (17, "Carlos Alberto", "Maciel Espinosa", "5CV32", 2022351319, "Puntual"),
    (18, "Pablo Jesus", "Martinez Hernandez", "5CV32", 2021350679, "Puntual"),
    (19, "Leonardo", "Perez Cuateta", "5CV32", 2022350448, "Puntual"),
    (20, "Eduardo", "Perez Juarez", "5CV32", 2022351755, "Puntual"),
    (21, "Jose Emilio", "Raymundo Zeferino", "5CV32", 2021350721, "Puntual"),
    (22, "Kevin Carlos", "Rojas Miron", "5CV32", 2016350561, "Puntual"),
    (23, "Emanuel Tristan", "San Pedro Texis", "5CV32", 2022351707, "Puntual"),
    (24, "Erick", "Sanchez Lopez", "5CV32", 2021350775, "Puntual"),
    (25, "Antonio de Jesus", "Torres Martinez", "5CV32", 2023350882, "Puntual")
]

cursor.executemany("INSERT INTO students values (?,?,?,?,?,?)", alumnos)

conn.commit()

conn.close()