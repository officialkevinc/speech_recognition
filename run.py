import speech_recognition as sr
import openpyxl
import os
import customtkinter
import time
import pyttsx3
import threading
import re
import json
import pyaudio
from datetime import datetime
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from threading import Thread
from playsound3 import playsound as play
from PIL import Image, ImageTk, ImageDraw
from vosk import Model, KaldiRecognizer

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"variables": {}, "array": [], "image_path": "default_image.png"}

def save_config(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

config_file = "config.json"
config_data = load_config(config_file)

def update_variable(key, value):
    config_data["variables"][key] = value #Dentro del grupo variables, en el parametro x, agrega
    save_config(config_file, config_data)

#Clear console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Crear un reconocedor
r = sr.Recognizer()
model = Model("model-es-small")
recognizer = KaldiRecognizer(model, 16000)

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

exit_event = threading.Event()
exit_event_retardos = threading.Event()

def thread_start(textbox, button_continuar):
    t = Thread(target=pase_lista, args=(textbox, button_continuar,), daemon=True)
    t.start()

def thread_retardos(textbox, numeros, button_continuar):
    t = Thread(target=retardos, args=(textbox, numeros, button_continuar,), daemon=True)
    t.start()

def thread_countdown(textbox, numeros, alumnos_sort):
    t = Thread(target=countdown, args=(textbox, numeros, alumnos_sort,), daemon=True)
    t.start()

def thread_hora_actual():
    t = Thread(target=tiempo_actual, daemon=True)
    t.start()

def tiempo_actual():
    hora_actual_label = None
    while True:
        hora = datetime.now().strftime("%H:%M:%S")
        if hora_actual_label:
            hora_actual_label.destroy()
        hora_actual_label = customtkinter.CTkLabel(master=main_frame_top_bar, text=hora, text_color="#75003E", font=("Roboto Regular", 16, "bold"))
        hora_actual_label.pack(padx=10, pady=3, side="right", expand=True)
        time.sleep(1)

def pase_lista(textbox, button_continuar):
    #Números del 1 al 25 en texto y su valor numérico
    numeros_texto = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
        "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25
    }

    # Arreglo para guardar 'Puntual' o 'Retardo'
    numeros = ['Falta'] * no_alumnos
    
    #Colores para cada estado de asistencia
    textbox.tag_config('puntual', foreground="#45CE30")
    textbox.tag_config('warning', foreground="#F3B63A")
    textbox.tag_config('falta', foreground="red")
    button_continuar.configure(command=lambda:[thread_retardos(textbox, numeros, button_continuar), thread_countdown(textbox, numeros, alumnos_sort), exit_event.set()])

    #Comienza pase de lista

    #Start audio stream
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    textbox.insert("end", "Escuchando...", "puntual")
    print("Escuchando...")
    
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        #textbox.delete("0.0", "end")
        
        if recognizer.AcceptWaveform(data):
            result = recognizer.FinalResult()
            palabras = str(result)
            cleaned_str = re.sub('["{}:"]|text', '', palabras)
            #cleaned_str = ' '.join(cleaned_str.split())
            cleaned_str = cleaned_str.split()
            print("Oración Reconocida: ", cleaned_str)

            #Comprobar si el número aparece como palabra o como número
            for i, numero in enumerate(numeros_texto):
                if numero in cleaned_str or str(numeros_texto[numero]) in cleaned_str:
                    print(numero)
                    print(cleaned_str)
                    print(str(numeros_texto[numero]))
                    textbox.delete("0.0", "end")
                    textbox.insert("end", "Registrando Asistencia...")
                    if i < len(numeros): 
                        numeros[i] = 'Puntual'
                        play("./assets/sounds/puntual.mp3")
            
            #textbox.delete("0.0", "end")
            #Imprimir los resultados
            print("Resultados:", numeros)
            textbox.delete("0.0", "end")
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
            
            textbox.insert("end", "Escuchando...", "puntual")
                    #textbox.insert("0.0", numero_asistencia + ".- " + alumno_actual + " - " + numeros[j] + "\n")
                    #textbox.delete("0.0", "end")
            if exit_event.is_set():
                print("Thread Pase Lista Terminado")
                break
        else:
            result = recognizer.PartialResult()
            continue
    #thread_retardos(textbox, numeros)
    #thread_countdown(textbox, numeros, alumnos_sort)

def retardos(textbox, numeros, button_continuar):
    time.sleep(3)
    #tiempo_tolerancia=20
    #Inicia tiempo de tolerancia para retardos

    #Números del 1 al 25 en texto y su valor numérico
    numeros_texto = {
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
        "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
        "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25
    }

    #Colores para cada estado de asistencia
    textbox.tag_config('puntual', foreground="#45CE30")
    textbox.tag_config('warning', foreground="#F3B63A")
    textbox.tag_config('falta', foreground="red")
    button_continuar.configure(command=lambda:[guardar_lista(textbox, numeros, alumnos_sort), exit_event_retardos.set()], text="Terminar")

    #Start audio stream
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Escuchando...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        #textbox.delete("0.0", "end")
        
        if recognizer.AcceptWaveform(data):
            result = recognizer.FinalResult()
            palabras = str(result)
            cleaned_str = re.sub('["{}:"]|text', '', palabras)
            #cleaned_str = ' '.join(cleaned_str.split())
            cleaned_str = cleaned_str.split()
            print("Oración Reconocida: ", cleaned_str)

            #Comprobar si el número aparece como palabra o como número
            for i, numero in enumerate(numeros_texto):
                if numero in cleaned_str or str(numeros_texto[numero]) in cleaned_str:
                    if i < len(numeros): 
                        numeros[i] = 'Retardo'
                        play("./assets/sounds/continue_2.mp3")

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
            textbox.insert("end", "Escuchando...", "puntual")
            if exit_event_retardos.is_set():
                print("Thread Retardos Terminado")
                break
        else:
            result = recognizer.PartialResult()
            continue

def countdown(textbox, numeros, alumnos_sort):
    tiempo_tolerancia = int(config_data["variables"]["tiempo_tolerancia"]) * 60 #Carga el parametro tiempo_tolerancia y lo convierte a int
    textbox.delete("0.0", "end")
    textbox.configure(font=('Roboto', 20), width=700, height=600)
    textbox.insert("end", "Comienzan a Contar Retardos\n")
    time.sleep(5)
    countdown_label = None
    while tiempo_tolerancia:
        mins, secs = divmod(tiempo_tolerancia, 60)
        timer_tolerancia = mins
        timer = '{:02d}:{:02d}'.format(mins, secs)
        if timer_tolerancia <= (1):
            time_running_out = "red"
        else:
            time_running_out = "#45CE30"
        if countdown_label:  # Si ya existe, destruir el label previo antes de crear uno nuevo
            countdown_label.destroy()
        countdown_label = customtkinter.CTkLabel(master=main_frame, text=timer, text_color=time_running_out, font=("Roboto Regular", 80, "bold"))
        countdown_label.place(relx=0.5, rely=0.5, anchor="center")
        time.sleep(1) 
        tiempo_tolerancia -= 1
        if tiempo_tolerancia < 1:
            exit_event_retardos.set()
            if exit_event_retardos.is_set():
                print("Thread Retardos Terminado")
                break
    if countdown_label:  # Si ya existe, destruir el label previo antes de crear uno nuevo
            countdown_label.destroy()
    time.sleep(5)
    guardar_lista(textbox, numeros, alumnos_sort)

def guardar_lista(textbox, numeros, alumnos_sort):
    #exit_event_retardos.set()
    time.sleep(1)
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
    current_date = datetime.now().strftime("%d-%m-%Y %H-%M")
    custom_workbook.save(f"Lista {current_date}.xlsx")

def salir_programa():
    quit()

def cargar_lista(textbox):
    counter = 1
    countdown_label = None
    if countdown_label:  # Si ya existe, destruir el label previo antes de crear uno nuevo
            countdown_label.destroy()
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
    ver_lista_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#FFFFFF")
    ver_lista_frame.pack_propagate(True)
    ver_lista_frame.pack(padx=0, pady=0, fill="both")

    textbox = customtkinter.CTkTextbox(master=ver_lista_frame, fg_color="transparent", text_color="#404040")
    textbox.configure(font=('Roboto', 20), height=400)
    textbox.pack(expand=True, side="right", fill="both")

    #button_agregar_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#FFE3F3")
    #button_agregar_frame.pack(expand=True, side="bottom", fill="both")
    cargar_lista(textbox)
    

def pasar_lista_page():
    delete_pages()
    pasar_lista_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#FFFFFF")
    pasar_lista_frame.pack_propagate(False)
    pasar_lista_frame.pack(padx=0, pady=0, fill="both")

    textbox = customtkinter.CTkTextbox(master=pasar_lista_frame, fg_color="transparent", text_color="#404040")
    textbox.configure(font=('Roboto', 20), height=600)
    textbox.pack(expand=True, side="right", fill="both")

    detener_paso_lista_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#FFE3F3")
    detener_paso_lista_frame.pack_propagate(False)
    detener_paso_lista_frame.pack(padx=0, pady=0, expand=False, side="bottom", fill="x")
    detener_paso_lista_frame.configure(height=120)

    button_continuar = customtkinter.CTkButton(master=detener_paso_lista_frame,
                                            fg_color="#75003E",
                                            compound="left",
                                            text="Comenzar Retardos",
                                            text_color="#FFFFFF",
                                            font=("Roboto Regular", 16, "bold"),
                                            corner_radius=5,
                                            width=160,
                                            height=40)
    button_continuar.place(relx=0.35, rely=0.3)
    thread_start(textbox, button_continuar)

def config_page():
    delete_pages()
    config_page_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#F4F4F4")
    config_page_frame.pack(padx=0, pady=0, expand=True, side="top", fill="both")

    config_page_button_frame = customtkinter.CTkFrame(master=main_frame, fg_color="#FFE3F3")
    config_page_button_frame.pack(padx=0, pady=0, expand=False, side="bottom", fill="x")
    config_page_button_frame.configure(height=120)

    # Cambiar variables

    #Nombre
    nombre_label = customtkinter.CTkLabel(master=config_page_frame, text="Nombre de Bienvenida", text_color="black", font=("Roboto Regular", 16, "bold"))
    nombre_label.pack()
    nombre_entry = customtkinter.CTkEntry(master=config_page_frame)
    nombre_entry.insert(0, str(config_data["variables"].get("nombre", "")))
    nombre_entry.pack()

    #Tolerancia
    tolerancia_label = customtkinter.CTkLabel(master=config_page_frame, text="Tolerancia (mins)", text_color="black", font=("Roboto Regular", 16, "bold"))
    tolerancia_label.pack()
    tolerancia_entry = customtkinter.CTkEntry(master=config_page_frame)
    tolerancia_entry.insert(0, str(config_data["variables"].get("tiempo_tolerancia", "")))
    tolerancia_entry.pack()

    #Seleccionar Grupos
    grupos_label = customtkinter.CTkLabel(master=config_page_frame, text="Seleccionar Grupo", text_color="black", font=("Roboto Regular", 16, "bold"))
    grupos_label.pack()
    grupos_dropdown = customtkinter.CTkComboBox(master=config_page_frame,
                                                values=["Grupo 1",
                                                        "Grupo 2"])
    grupos_dropdown.pack()

    #Agregar Grupos
    grupos_label = customtkinter.CTkLabel(master=config_page_frame, text="Agregar un Grupo", text_color="black", font=("Roboto Regular", 16, "bold"))
    grupos_label.pack()
    grupos_entry = customtkinter.CTkEntry(master=config_page_frame)
    grupos_entry.insert(0, str(config_data["grupos"].get("grupo1", "")))
    grupos_entry.pack()

    #Modelo de Reconocimiento
    modelo_label = customtkinter.CTkLabel(master=config_page_frame, text="Seleccionar Modelo", text_color="black", font=("Roboto Regular", 16, "bold"))
    modelo_label.pack()
    modelo_dropdown = customtkinter.CTkComboBox(master=config_page_frame,
                                                values=["Español (Light)",
                                                        "Español (Full)",
                                                        "English (Light)",
                                                        "English (Full)"])
    modelo_dropdown.pack()

    button_actualizar = customtkinter.CTkButton(master=config_page_button_frame,
                                                fg_color="#75003E",
                                                compound="left",
                                                text="Guardar Cambios",
                                                text_color="#FFFFFF",
                                                font=("Roboto Regular", 16, "bold"),
                                                corner_radius=5,
                                                width=160,
                                                height=40,
                                                command=lambda:
                                                [   
                                                    update_variable("nombre", nombre_entry.get()),
                                                    update_variable("tiempo_tolerancia", tolerancia_entry.get()),
                                                 
                                                ])
    button_actualizar.place(relx=0.5, rely=0.5)

#Dia, hora y tiempo del dia
dia_interfaz = datetime.now().strftime("%d/%m/%Y")
hora_interfaz = datetime.now().strftime("%H:%M:%S")
hora_actual = current_date = datetime.now().hour

if hora_actual >= 20:
    hora_actual = "Buenas noches, profesor"
elif hora_actual >= 12:
    hora_actual = "Buenas tardes, profesor"
else:
    hora_actual = "Buenos días, profesor"


ver_lista_icon = customtkinter.CTkImage(light_image=Image.open("./assets/icons/ver_lista.png"), size=(30, 30))
pasar_lista_icon = customtkinter.CTkImage(light_image=Image.open("./assets/icons/pasar_lista.png"), size=(30, 30))
salir_icon = customtkinter.CTkImage(light_image=Image.open("./assets/icons/salir.png"), size=(30, 30))

logo_image = Image.open("./assets/images/logo.png")
logo_image = logo_image.resize((80, 120))
logo_image_tk = ImageTk.PhotoImage(logo_image)

logo_esime = Image.open("./assets/images/esime.png")
logo_esime = logo_esime.resize((50, 50))
logo_esime_tk = ImageTk.PhotoImage(logo_esime)

main_image = Image.open("./assets/images/avatar.png")
main_image = main_image.resize((300, 300))  #Tamaño de la imagen
main_image_tk = ImageTk.PhotoImage(main_image)

#main_bg = Image.open("./assets/images/bg_main.png")
#main_bg = main_bg.resize((300, 300))  #Tamaño de la imagen
#main_bg_tk = ImageTk.PhotoImage(main_bg)

sidebar = customtkinter.CTkFrame(master=app, fg_color="#75003E")
sidebar.pack_propagate(False)
sidebar.pack(padx=0, pady=0, side="left", fill="y", expand=False)
sidebar.configure(width=200)

logo_label = customtkinter.CTkLabel(master=sidebar, image=logo_image_tk, text="")
logo_label.pack(pady=(10, 20))

main_frame = customtkinter.CTkFrame(master=app, fg_color="#FFFFFF")
main_frame.pack(padx=0, pady=0, expand=True, side="right", fill="both")

main_frame_top_bar = customtkinter.CTkFrame(master=main_frame, fg_color="#FFE3F3")
main_frame_top_bar.pack_propagate(False)
main_frame_top_bar.pack(padx=0, pady=0, expand=False, side="top", fill="x")
main_frame_top_bar.configure(height=60)

#Dia actual
hora_label = customtkinter.CTkLabel(master=main_frame_top_bar, text=(dia_interfaz), text_color="#75003E", font=("Roboto Regular", 16, "bold"))
hora_label.pack(padx=10, pady=3, side="left", expand=True)

#Hora actual
thread_hora_actual()

#Logo Esime
logo_esime_label = customtkinter.CTkLabel(master=main_frame_top_bar, image=logo_esime_tk, text="")
logo_esime_label.pack(padx=10, pady=3, side="left", expand=True)

#Main image centered
main_image_label = customtkinter.CTkLabel(master=main_frame, image=main_image_tk, text="")
main_image_label.place(relx=0.5, rely=0.5, anchor="center")

#Saludo
main_label = customtkinter.CTkLabel(master=main_frame, text=(hora_actual), text_color="#75003E", font=("Roboto Regular", 40, "bold"))
main_label.pack(pady=20)

#Nombre
profesor_label = customtkinter.CTkLabel(master=main_frame, text="Cabrera Tejeda Juan José", text_color="#75003E", font=("Roboto Regular", 32))
profesor_label.place(relx=0.5, rely=0.83, anchor="center")

buttons_frame = customtkinter.CTkFrame(master=sidebar, fg_color="transparent")
buttons_frame.pack(expand=True, side="top", fill="y")

button = customtkinter.CTkButton(master=buttons_frame,
                                 image=ver_lista_icon,
                                 compound="left",
                                 text="Ver Lista",
                                 text_color="#404040",
                                 font=("Roboto Regular", 16, "bold"),
                                 corner_radius=5,
                                 fg_color="#FFFFFF",
                                 command=ver_lista_page,
                                 width=160,
                                 height=40,
                                 anchor="w")
button.pack(padx=20, pady=20)
button.bind("<Enter>", lambda event: button.configure(text_color="#FFFFFF",
                                                        border_color="#FFFFFF",
                                                        border_width=1,
                                                        fg_color="transparent"))
button.bind("<Leave>", lambda event: button.configure(text_color="#404040",
                                                        fg_color="white"))

button2 = customtkinter.CTkButton(master=buttons_frame,
                                  image=pasar_lista_icon,
                                  compound="left",
                                  text="Pasar Lista",
                                  text_color="#404040",
                                  font=("Roboto Regular", 16, "bold"),
                                  corner_radius=5,
                                  fg_color="#FFFFFF",
                                  width=160,
                                  height=40,
                                  anchor="w",
                                  command=pasar_lista_page)
button2.pack(padx=20, pady=20)
button2.bind("<Enter>", lambda event: button2.configure(text_color="#FFFFFF",
                                                        border_color="#FFFFFF",
                                                        border_width=1,
                                                        fg_color="transparent"))
button2.bind("<Leave>", lambda event: button2.configure(text_color="#404040",
                                                        fg_color="white"))

button_confguracion = customtkinter.CTkButton(master=buttons_frame,
                                  image=salir_icon,
                                  compound="left",
                                  text="Configuración",
                                  text_color="#404040",
                                  font=("Roboto Regular", 16, "bold"),
                                  corner_radius=5,
                                  fg_color="#FFFFFF",
                                  width=160,
                                  height=40,
                                  anchor="w",
                                  command=config_page)
button_confguracion.pack(padx=20, pady=20)
button_confguracion.bind("<Enter>", lambda event: button_confguracion.configure(text_color="#FFFFFF",
                                                        border_color="#FFFFFF",
                                                        border_width=1,
                                                        fg_color="transparent"))
button_confguracion.bind("<Leave>", lambda event: button_confguracion.configure(text_color="#404040",
                                                        fg_color="white"))

button_salir = customtkinter.CTkButton(master=buttons_frame,
                                  image=salir_icon,
                                  compound="left",
                                  text="Salir",
                                  text_color="#404040",
                                  font=("Roboto Regular", 16, "bold"),
                                  corner_radius=5,
                                  fg_color="#FFFFFF",
                                  width=160,
                                  height=40,
                                  anchor="w",
                                  command=salir_programa)
button_salir.pack(padx=20, pady=20)
button_salir.bind("<Enter>", lambda event: button_salir.configure(text_color="#FFFFFF",
                                                        border_color="#FFFFFF",
                                                        border_width=1,
                                                        fg_color="transparent"))
button_salir.bind("<Leave>", lambda event: button_salir.configure(text_color="#404040",
                                                        fg_color="white"))

app.mainloop()

