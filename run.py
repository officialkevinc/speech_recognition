import speech_recognition as sr
import openpyxl
import os
import customtkinter
import time
import pyttsx3
from datetime import datetime
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from threading import Thread

#Clear console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Crear un reconocedor
r = sr.Recognizer()

i = 0
alumnos = []

#Cargar archivo de alumnos
try:
    with open("alumnos_raw.txt", "r") as file:
        existing_strings = set(file.read().splitlines())  #Cargar lineas en un set
        no_alumnos = len(existing_strings)  #Cuenta el numero de lineas
except FileNotFoundError:
    existing_strings = set()  #Si no existe el archivo, crear un nuevo set
alumnos_sort = sorted(existing_strings)

def thread_start(textbox):
    t = Thread(target=pase_lista, args=(textbox,), daemon=True)
    t.start()

def thread_retardos(textbox, numeros):
    t = Thread(target=retardos, args=(textbox, numeros,), daemon=True)
    t.start()

def thread_countdown(textbox, numeros, alumnos_sort):
    t = Thread(target=countdown, args=(textbox, numeros, alumnos_sort), daemon=True)
    t.start()

def pase_lista(textbox):
    #Números del 1 al 25 en texto y su valor numérico
    numeros_texto = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
        "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25
    }

    count=0
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)

    # Arreglo para guardar 'Puntual' o 'Retardo'
    numeros = ['Falta'] * 25
    
    #Colores para cada estado de asistencia
    textbox.tag_config('puntual', foreground="#45CE30")
    textbox.tag_config('warning', foreground="yellow")
    textbox.tag_config('falta', foreground="red")

    #Comienza pase de lista
    #no_alumnos
    while count<2:
        try:
            alumno_loop = str(count+1)
            print("Alumno actual: " + alumno_loop)

            engine.say("Number " + alumno_loop)
            engine.runAndWait()

            textbox.insert("end", "Escuchando a Numero " + alumno_loop + "...\n\n")
            print("Escuchando...")
            
            with sr.Microphone() as source:
                
                #r.adjust_for_ambient_noise(source)
                audio = r.record(source, duration=5)

                # Reconocer el audio usando Google Web Speech API
                text = r.recognize_google(audio, language="es-ES")
                print("Oración reconocida: " + text)

                # Dividir el texto en palabras
                palabras = text.split()

                #Comprobar si el número aparece como palabra o como número
                for i, numero in enumerate(numeros_texto):
                    if numero in palabras:
                        numeros[i] = 'Puntual'
                        engine.say("Number " + alumno_loop + ", Check")
                        engine.runAndWait()
                    elif str(numeros_texto[numero]) in palabras:
                        numeros[i] = 'Puntual'
                        engine.say("Number " + alumno_loop + ", Check")
                        engine.runAndWait()

                textbox.delete("0.0", "end")

                #Imprimir los resultados
                print("Resultados:", numeros)
                for j in range(no_alumnos):
                    alumno_actual = str(alumnos_sort[j])
                    numero_asistencia = str(j+1)
                    if numeros[j] == 'Puntual':
                        start_index = textbox.index("end")
                        textbox.insert("end", numero_asistencia + ".- " + alumno_actual + " - ")
                        textbox.insert("end", "Puntual\n", "puntual")
                        end_index = textbox.index("end")
                    else:
                        start_index = textbox.index("end")
                        textbox.insert("end", numero_asistencia + ".- " + alumno_actual + " - ")
                        textbox.insert("end", "Retardo\n", "warning")
                        end_index = textbox.index("end")
                    #textbox.insert("0.0", numero_asistencia + ".- " + alumno_actual + " - " + numeros[j] + "\n")
        except sr.UnknownValueError:
            print("No se pudo entender el audio. Por favor revisa que su micrófono esté conectado.")
            textbox.insert("end", "No se reconoció asistencia para este número. Pasando al siguiente.\n\n")
            count = count+1
            continue
        except sr.RequestError as e:
            print("No se pudo solicitar resultados; {0}".format(e))
        count = count+1
    thread_retardos(textbox, numeros)
    thread_countdown(textbox, numeros, alumnos_sort)

def retardos(textbox, numeros):
    time.sleep(3)
    tiempo_tolerancia=15
    #Inicia tiempo de tolerancia para retardos

    #Números del 1 al 25 en texto y su valor numérico
    numeros_texto = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
        "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25
    }

    engine = pyttsx3.init()
    engine.setProperty('rate', 110)

    #Colores para cada estado de asistencia
    textbox.tag_config('puntual', foreground="#45CE30")
    textbox.tag_config('warning', foreground="yellow")
    textbox.tag_config('falta', foreground="red")

    while True:
        try:
            with sr.Microphone() as source:
                    
                #r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.record(source, duration=tiempo_tolerancia)

                # Reconocer el audio usando Google Web Speech API
                text = r.recognize_google(audio, language="es-ES")
                print("Oración reconocida: " + text)

                # Dividir el texto en palabras
                palabras = text.split()

                #Comprobar si el número aparece como palabra o como número
                for i, numero in enumerate(numeros_texto):
                    if numero in palabras:
                        numeros[i] = 'Retardo'
                    elif str(numeros_texto[numero]) in palabras:
                        numeros[i] = 'Retardo'

                textbox.delete("0.0", "end")

                #Imprimir los resultados
                print("Resultados:", numeros)
                for j in range(no_alumnos):
                    alumno_actual = str(alumnos_sort[j])
                    numero_asistencia = str(j+1)
                    if numeros[j] == 'Puntual':
                        start_index = textbox.index("end")
                        textbox.insert("end", numero_asistencia + ".- " + alumno_actual + " - ")
                        textbox.insert("end", "Puntual\n", "puntual")
                        end_index = textbox.index("end")
                    elif numeros[j] == 'Retardo':
                        start_index = textbox.index("end")
                        textbox.insert("end", numero_asistencia + ".- " + alumno_actual + " - ")
                        textbox.insert("end", "Retardo\n", "warning")
                        end_index = textbox.index("end")
                    else:
                        numeros[j] = 'Falta'
                        start_index = textbox.index("end")
                        textbox.insert("end", numero_asistencia + ".- " + alumno_actual + " - ")
                        textbox.insert("end", "Falta\n", "falta")
                        end_index = textbox.index("end")
        except sr.UnknownValueError:
            print("No se pudo entender el audio. Por favor revisa que su micrófono esté conectado.")
            textbox.insert("end", "No se pudo entender el audio. Por favor revise que su micrófono esté conectado.\n\n")
            continue
        except sr.RequestError as e:
            print("No se pudo solicitar resultados; {0}".format(e))

def countdown(textbox, numeros, alumnos_sort):
    tiempo_tolerancia=15
    textbox.delete("0.0", "end")
    textbox.insert("end", "Comienzan a Contar Retardos\n")
    time.sleep(5)
    while tiempo_tolerancia:
        mins, secs = divmod(tiempo_tolerancia, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs)
        textbox.delete("0.0", "end")
        textbox.insert("end", timer + "\n")
        time.sleep(1) 
        tiempo_tolerancia -= 1
    guardar_lista(textbox, numeros, alumnos_sort)

def guardar_lista(textbox, numeros, alumnos_sort):
    time.sleep(3)
    textbox.delete("0.0", "end")
    textbox.insert("end", "Guardando Lista\n")
    
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M")

    custom_workbook = openpyxl.load_workbook("./assets/Lista de Asistencia.xlsx")
    sheet = custom_workbook.active

    sheet['B4'] = "ESCUELA SUPERIOR DE INGENIERÍA MECÁNICA Y ELECTRÍCA UNIDAD CULHUACÁN"
    sheet['B5'] = "NOMBRE DEL DOCENTE: CABRERA TEJEDA JUAN JOSÉ"
    sheet['C6'] = current_date

    dia_actual = datetime.now().day
        
    columnas = list(range(4, 34))  #D es la columna 4 y AH es la columna 34

    #Imprimir los nombres
    fila_inicio = 8
    for i, alumno in enumerate(alumnos_sort):
        if fila_inicio + i <= 42:  # Para no exceder la fila 42
            sheet.cell(row=fila_inicio + i, column=3).value = alumno

    # Verificar si la celda de la fila 7 contiene el día actual
    for col in columnas:
        celda = sheet.cell(row=7, column=col)
        if celda.value == dia_actual:
            # Si se encuentra la columna con el día actual, escribir la información de numeros[]
            for i, asistencia in enumerate(numeros):
                if fila_inicio + i <= 42:  # Para no exceder la fila 42
                    if asistencia == 'Puntual':
                        shortener = 'P'
                        sheet.cell(row=fila_inicio + i, column=col).value = shortener
                        sheet.cell(row=fila_inicio + i, column=col).fill = PatternFill(start_color='019031', end_color='019031', fill_type='solid')
                        sheet.cell(row=fila_inicio + i, column=col).font = Font(color='FFFFFF')
                        print(f"Escribiendo en fila {fila_inicio + i}, columna {col}: {shortener}")
                    elif asistencia == 'Retardo':
                        shortener = 'R'
                        sheet.cell(row=fila_inicio + i, column=col).value = shortener
                        sheet.cell(row=fila_inicio + i, column=col).fill = PatternFill(start_color='F3B431', end_color='F3B431', fill_type='solid')
                        sheet.cell(row=fila_inicio + i, column=col).font = Font(color='FFFFFF')
                        print(f"Escribiendo en fila {fila_inicio + i}, columna {col}: {shortener}")
                    else:
                        shortener = 'F'
                        sheet.cell(row=fila_inicio + i, column=col).value = shortener
                        sheet.cell(row=fila_inicio + i, column=col).fill = PatternFill(start_color='B83227', end_color='B83227', fill_type='solid')
                        sheet.cell(row=fila_inicio + i, column=col).font = Font(color='FFFFFF')
                        print(f"Escribiendo en fila {fila_inicio + i}, columna {col}: {shortener}")
            break  # Salir del bucle una vez que se escribe en la columna correcta

    custom_workbook.save("Lista.xlsx")

def salir_programa():
    quit()

def cargar_lista(textbox):
    counter = 1
    for lista in alumnos_sort:
        count = str(counter)
        start_index = textbox.index("end")
        textbox.insert("end", count + ".- " + lista + "\n")
        print("Alumnos Ordenados:", lista)
        counter += 1

app = customtkinter.CTk()
app.title("Speech Recognition App")
app.geometry("900x600")

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def ver_lista_page():
    delete_pages()
    ver_lista_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#07131d")
    ver_lista_frame.pack_propagate(True)
    ver_lista_frame.pack(padx=0, pady=0, fill="both")

    textbox = customtkinter.CTkTextbox(master=ver_lista_frame, fg_color="transparent", text_color="white")
    textbox.configure(font=('Roboto', 20), height=600)
    textbox.pack(expand=True, side="right", fill="both")
    cargar_lista(textbox)
    

def pasar_lista_page():
    delete_pages()
    pasar_lista_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#07131d")
    pasar_lista_frame.pack_propagate(True)
    pasar_lista_frame.pack(padx=0, pady=0, fill="both")
    textbox = customtkinter.CTkTextbox(master=pasar_lista_frame, fg_color="transparent", text_color="white")
    textbox.configure(font=('Roboto', 20), height=600)
    textbox.pack(expand=True, side="right", fill="both")
    thread_start(textbox)
    

sidebar = customtkinter.CTkFrame(master=app, fg_color="#131E29")
sidebar.pack_propagate(False)
sidebar.pack(padx=0, pady=0, side=customtkinter.LEFT, fill="y")
sidebar.configure(width=200)
#sidebar.pack(padx=20, pady=20, expand=True)

main_frame = customtkinter.CTkFrame(master=app, fg_color="#07131d")
main_frame.pack(padx=0, pady=0, expand=True, side="right", fill="both")

button = customtkinter.CTkButton(master=sidebar, text="Ver Lista", corner_radius=5, fg_color="#145DA0", command=ver_lista_page)
button.pack(padx=20, pady=20)

button2 = customtkinter.CTkButton(master=sidebar, text="Pasar Lista", corner_radius=5, fg_color="#145DA0", command=pasar_lista_page)
button2.pack(padx=20, pady=20)

button3 = customtkinter.CTkButton(master=sidebar, text="Salir", corner_radius=5, fg_color="#145DA0", command=salir_programa)
button3.pack(padx=20, pady=20)

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

