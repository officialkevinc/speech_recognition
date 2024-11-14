import speech_recognition as sr
import openpyxl
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# Clear console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Crear un reconocedor
r = sr.Recognizer()

def pase_lista():
    
    # Usar el micrófono como fuente de audio
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.record(source, duration=5)

        try:
            # Reconocer el audio usando Google Web Speech API
            text = r.recognize_google(audio, language="es-ES")
            print("Oración reconocida: " + text)

            # Dividir el texto en palabras
            palabras = text.split()

            # Números del 1 al 25 en texto y su valor numérico
            numeros_texto = {
                "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
                "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
                "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25
            }

            # Arreglo para guardar 'Puntual' o 'Retardo'
            numeros = ['Retardo'] * 25

            # Comprobar si el número aparece como palabra o como número
            for i, numero in enumerate(numeros_texto):
                if numero in palabras:
                    numeros[i] = 'Puntual'
                elif str(numeros_texto[numero]) in palabras:
                    numeros[i] = 'Puntual'

            # Imprimir los resultados
            print("Resultados:", numeros)

        except sr.UnknownValueError:
            print("No se pudo entender el audio. Por favor revisa que su micrófono esté conectado.")
        except sr.RequestError as e:
            print("No se pudo solicitar resultados; {0}".format(e))

    # Crear un nuevo libro de trabajo y una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"

    # Fecha y hora actual
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Agregar datos a la hoja
    column_heading = ["Numero de Lista", "Nombre", current_date]
    ws.append(column_heading)
    for k in range(no_alumnos):
        data = [
            [k+1, alumnos_sort[k], numeros[k]]
        ]
        for row in data:
            ws.append(row)

    # Definir el rango de la tabla
    tab = Table(displayName="Tabla1", ref="A1:C26")

    # Agregar estilo a la tabla
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True
    )
    tab.tableStyleInfo = style

    # Agregar la tabla a la hoja
    ws.add_table(tab)

    # Guardar el archivo
    wb.save("Lista.xlsx")

i = 0
opcion = 0
alumnos = []
# Read current contents of the file
try:
    with open("alumnos_raw.txt", "r") as file:
        existing_strings = set(file.read().splitlines())  # Store current lines in a set
        no_alumnos = len(existing_strings)  # Counts the number of lines
except FileNotFoundError:
    existing_strings = set()  # If file doesn't exist, start with an empty set

while opcion != 4:
    print("Selecciona una opcion\n1.- Crear Lista\n2.- Iniciar Pase de Lista\n3.- Cargar Contenido\n4.- Salir")
    opcion = int(input("\nSeleccione una opcion: "))
    if opcion == 1:
        clear()
        print("Has seleccionado la opcion 1. Escriba 'stop' para temrinar de agregar alumnos")
        no_alumnos = int(input("Numero de alumnos que desea agregar: "))
        for i in range(no_alumnos):
            iteracion = str(i+1)
            print("Nombre del alumno " + iteracion + ": ")
            user_input = str(input())
            if user_input == 'stop':
                quit()
            alumnos.append(user_input)
        alumnos_sort = sorted(alumnos)
        print(alumnos_sort)
        with open("alumnos_nuevo.txt", "w") as file:
            for string in alumnos_sort:
                file.write(string + "\n")
        print("Los alumnos han sido guardados dentro de alumnos_raw.txt")
    elif opcion == 2:
        clear()
        print("Has seleccionado la opcion 2")
        pase_lista()
    elif opcion == 3:
        clear()
        print("Cargar Contenido de alumnos_raw.txt")
        print("Numero de alumnos en el archivo: ", no_alumnos)
        alumnos_sort = sorted(existing_strings)
        for lista in alumnos_sort:
            print("Alumnos Ordenados:", lista)
    elif opcion == 4:
        quit()
    else:
        clear()
        print("Opcion no valida. Intente de nuevo.\n")