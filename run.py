import speech_recognition as sr
import openpyxl
import os
import customtkinter
from datetime import datetime
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

#Clear console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Crear un reconocedor
r = sr.Recognizer()

i = 0
opcion = 0
alumnos = []
#Read current contents of the file
try:
    with open("alumnos_raw.txt", "r") as file:
        existing_strings = set(file.read().splitlines())  #Cargar lineas en un set
        no_alumnos = len(existing_strings)  #Cuenta el numero de lineas
except FileNotFoundError:
    existing_strings = set()  #Si no existe el archivo, crear un nuevo set
alumnos_sort = sorted(existing_strings)


def pase_lista():
    # Usar el micrófono como fuente de audio
    with sr.Microphone() as source:
        textbox.insert("0.0", "Escuchando...")
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

def salir_programa():
    quit()

def cargar_lista():
    for lista in alumnos_sort:
        textbox.insert("0.0", lista + "\n")
        print("Alumnos Ordenados:", lista)

app = customtkinter.CTk()
app.title("Speech Recognition App")
app.geometry("600x500")

sidebar = customtkinter.CTkFrame(master=app, fg_color="#0C2D48")
sidebar.pack(padx=0, pady=0, fill="y", side="left")
#sidebar.pack(padx=20, pady=20, expand=True)

main_frame = customtkinter.CTkFrame(master=app, fg_color="#FFFFFF")
main_frame.pack(padx=0, pady=0, expand=True, side="right", fill="both")

button = customtkinter.CTkButton(master=sidebar, text="Ver Lista", corner_radius=5, fg_color="#145DA0", command=cargar_lista)
button.pack(padx=20, pady=20)

button2 = customtkinter.CTkButton(master=sidebar, text="Pasar Lista", corner_radius=5, fg_color="#145DA0", command=pase_lista)
button2.pack(padx=20, pady=20)

button3 = customtkinter.CTkButton(master=sidebar, text="Salir", corner_radius=5, fg_color="#145DA0", command=salir_programa)
button3.pack(padx=20, pady=20)

textbox = customtkinter.CTkTextbox(master=main_frame, fg_color="white", text_color="black")
textbox.configure(font=('Roboto', 20))
textbox.pack(expand=True, side="right", fill="both")

app.mainloop()


#while opcion != 4:
#    print("Selecciona una opcion\n1.- Crear Lista\n2.- Iniciar Pase de Lista\n3.- Cargar Contenido\n4.- Salir")
#    opcion = int(input("\nSeleccione una opcion: "))
#    if opcion == 1:
#        clear()
#        print("Has seleccionado la opcion 1. Escriba 'stop' para temrinar de agregar alumnos")
#        no_alumnos = int(input("Numero de alumnos que desea agregar: "))
#        for i in range(no_alumnos):
#            iteracion = str(i+1)
#            print("Nombre del alumno " + iteracion + ": ")
#            user_input = str(input())
#            if user_input == 'stop':
#                quit()
#            alumnos.append(user_input)
#        alumnos_sort = sorted(alumnos)
#        print(alumnos_sort)
#        with open("alumnos_nuevo.txt", "w") as file:
#            for string in alumnos_sort:
#                file.write(string + "\n")
#        print("Los alumnos han sido guardados dentro de alumnos_raw.txt")

