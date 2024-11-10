import time
import datetime
import os.path
import sqlite3
import mouse
import customtkinter
from tabulate import tabulate

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageColor


caja1 = None
nombre_enc = None
ganancia = 0
#!!!!!!!!!!!!!1  FUNCIONES !!!!!!!!!!!!!!!!!!!!

#controlo que se ingrese un texto NO vacio, no se número, ni caracter especial
def validar_texto(entrada):
    # Verifica si la entrada contiene solo letras (sin números ni caracteres especiales)
    return entrada.isalpha() or " " in entrada

#Controlo si confirma o no el pedido.
def confirma_pedido(conf):
    while  conf != "s" and conf != "n":
        print("    Debe ingresar una S o una N")
        print("")
        conf = input("Intente nuevamente: ")
        conf = conf.lower()
    return conf
    
    
#controlo que el dato se pueda pasar a entero
def verif_entero(nro):
    while nro.isdecimal() == False:
        print("Debe ingresar solo números enteros, intente nuevamente...")
        print("")
        nro = input("ingrese un número: ")
    nro = int(nro)
    return nro

#Controlo que el dinero con el que pague no sea menos que el gasto
def verifica_vuelto(ab,tot):
    calculo = ab - tot
    while calculo < 0:
        cal = calculo * -1
        print(f"Para completar el pago le faltan {cal} usd\n")
        ab = verif_entero(input("ingrese nuevamente el monto con el que abona el pedido: "))
        calculo = ab - tot
    return calculo

def Encargado():
    global nombre_enc
    
    nombre_enc = caja1.get()
    caja1.delete(0, tk.END)
	#caja1.delete(1, tk.END)
	#print(nombre)
	#print("Hola mundo",nombre)
	#etiqueta_saludo.config(text="Hola " + nombre_enc)
    registro_emple_db(nombre_enc,1,0)
    ganancia = 0
    return nombre_enc

#función para registrar los movimientos de encargad@s
def registro_emple_db(nom,turno,recaudacion):
    global etiqueta2
    # Define los valores de la hora y dia con formto de sqllite3 (el anterior de datitime me tiraba que estaba viejo)
    match turno:
        case 1:
            conn = sqlite3.connect("comercio.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT datetime('now')")
            hora = cursor.fetchone()[0]  # guardo el valor de la consulta de la hora y dia
            evento = "ingresa"
            # Crea la tabla "registro" y verifica si aún no existe
            cursor.execute("CREATE TABLE IF NOT EXISTS registro(reg_id INTEGER PRIMARY KEY AUTOINCREMENT, encargado VARCHAR(50), hora_registro VARCHAR(20), evento VARCHAR(10), caja INTEGER)") 
            cursor.execute("INSERT INTO registro VALUES (NULL, ?, ?, ?, ?)", (nom, hora, evento, recaudacion)) 
            conn.commit() 
            conn.close() 
            
            messagebox.showinfo("Encargad@s", f"Ingreso de encargad@ guardado con exito, ya puede tomar pedidos nuevos desde el menú principal.", parent=ventana)
            caja1.delete(0, tk.END)
            opcion_menu1.entryconfigure("Nuevo", state="normal")
            etiqueta2=tk.Label(ventana, text=f"{nom}: recuerda, siempre hay que recibir al cliente con una sonrisa.", bg = "black", fg = "white",font=("Papyrus", 24), justify="center")# bg="#fa7785")
            etiqueta2.place(relx=0.5, y=710, anchor="center")
           
            #etiqueta_saludo.config(text="Ingreso de encargad@ guardado con exito. ")
            # 
            ##etiqueta_saludo.config(bg = "black", fg = "red",font=("Arial Balck", 18), text=f"El encargad@ registrado es:  {nom}")
            #ventana.update()
        case _:
            conn = sqlite3.connect("comercio.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT datetime('now')")
            hora = cursor.fetchone()[0]  # guardo el valor de la consulta de la hora y dia
            evento = "egresa"
            cursor.execute("CREATE TABLE IF NOT EXISTS registro (reg_id INTEGER PRIMARY KEY AUTOINCREMENT, encargado VARCHAR(50), hora_registro VARCHAR(20), evento VARCHAR(10), caja INTEGER)")
            cursor.execute("INSERT INTO registro VALUES (NULL, ?, ?, ?, ?)", (nom, hora, evento, recaudacion))
            conn.commit()
            conn.close()
            etiqueta2.place_forget()
            messagebox.showinfo("Encargad@s", f"Egreso de encargad@ guardado con exito,  Ingrese el nombre del encargad@ entrante.", parent=ventana)
            #etiqueta_saludo.config(text="Ingreso de encargad@ guardado con exito. ")


def cambio_de_turno():
    global ganancia
    registro_emple_db(nombre_enc,2,ganancia)
    
    ganancia = 0
    #ventana.update()



# Función para calcular el total	
#def calcular_total():
  #  total = 0
   # total = (caja_simple.get() * 5) + (caja_doble.get() * 6) + (caja_triple.get() * 7) + (caja_postre.get() * 2)

    #messagebox.showinfo("Total", f"El total de su pedido es ${total:.2f}")

def pedidos_nuevos():
    global ganancia
    
    # Función para calcular el total    
    def calcular_total():
        global ganancia
        try:
            # Obtener los valores de las cajas de entrada como números
            simple = int(caja_simple.get())
            doble = int(caja_doble.get())
            triple = int(caja_triple.get())
            postre = int(caja_postre.get())
            cbos = simple * 5
            cbod = doble * 6
            cbot = triple * 7
            pos = postre * 2

            # Calcular el total
            total = (simple * 5) + (doble * 6) + (triple * 7) + (postre * 2)

            # Mostrar el total en un cuadro de diálogo
            messagebox.showinfo("Total", f"El total de su pedido es ${total:.2f}", parent=ventana_ped)
            # Crear un nuevo label y una caja de entrada para el monto a pagar
            label_pago = tk.Label(frame, text="Ingrese con cuantos usd abona el cliente:", bg="black", fg="orange", font=("Arial Black", 12), justify="left")
            label_pago.grid(row=8, column=0, sticky="e", padx=5, pady=7)

            caja_pago = tk.Entry(frame, font=("Arial", 12), justify="center")
            caja_pago.grid(row=8, column=1, padx=5, pady=7)

            #Controlo que el dinero con el que pague no sea menos que el gasto
            def verifica_vuelto():
                global ganancia
                try:
                    abona = int(caja_pago.get())
                    calculo = 0

                    calculo = abona - total
                    if calculo < 0:
                        cal = calculo * -1
                        messagebox.showwarning("Abona", f"!Atencion! Para completar el pago le faltan {cal:.2f} usd.", parent=ventana_ped)
                    else:
                        messagebox.showinfo("Abona", f"El vuelto sera de: {calculo:.2f} usd.", parent=ventana_ped)

                        def registra_ventas_db():
                            global ganancia
                            conn = sqlite3.connect("comercio.sqlite")
                            cursor = conn.cursor()
                            cursor.execute("SELECT datetime('now')")
                            hora_vtas = cursor.fetchone()[0]  # guardo el valor de la consulta de la hora y dia
                            evento = "ingresa"
                            var_cliente = caja_cliente.get()
                            # Crea la tabla "registro" y verifica si aún no existe
                            cursor.execute("CREATE TABLE IF NOT EXISTS ventas (vtas_id INTEGER PRIMARY KEY AUTOINCREMENT, cliente VARCHAR(30), hora_venta VARCHAR(20), combo_simple INTEGER, combo_doble INTEGER, combo_triple INTEGER, postres INTEGER, recardacion INTEGER, encargado VARCHAR(50))")
                            cursor.execute("INSERT INTO ventas VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",(var_cliente, hora_vtas, cbos, cbod, cbot, pos, total, nombre_enc))
                            conn.commit()
                            conn.close()
                            messagebox.showinfo("Venta", f"Pedido guardado y en proceso...", parent=ventana_ped)
                            ganancia = ganancia + total

                            ventana_ped.destroy()
                            pedidos = pedidos_nuevos()
                            return ganancia


                        label_confirma = tk.Label(frame, text="¿Confirma el pedido?", bg="black", fg="#39ff14", font=("terminal", 12), justify="center")
                        label_confirma.grid(row=10, column=0, sticky="e", padx=10, pady=7)
                        boton_confirma = tk.Button(frame, text="Guardar & Generar Pedido", bg="#39ff14", font=("terminal", 12), justify="center", command=registra_ventas_db)
                        boton_confirma.grid(row=10, column=1, columnspan=2, padx=10, pady=10)

                except ValueError:
                    # Manejar errores si los valores no son números válidos
                   messagebox.showerror("Error", "Ingrese valores válidos en las cajas de entrada.", parent=ventana_ped)

            boton_vuelto = tk.Button(frame, text="Calcular Vuelto", bg="orange", font=("terminal", 12), justify="center", command=verifica_vuelto)
            boton_vuelto.grid(row=9, column=1, columnspan=2, padx=10, pady=10)



        except ValueError:
            # Manejar errores si los valores no son números válidos
            messagebox.showerror("Error", "Ingrese valores numéricos válidos en las cajas de entrada.", parent=ventana_ped)

        
    ventana_ped = tk.Toplevel(ventana)
    ventana_ped.geometry("800x650+100+55") #con esto arran bien arriba y bien a la izquierda
    ventana_ped.config(bg="black")
    ventana_ped.title("Hamburguesería Pennywise - Tomá de Pedidos")
    ventana_ped.iconbitmap("penny.ico")
    ventana_ped.resizable(width=False, height=False)
   # Cargar la imagen de fondo
    imagen_fondo = Image.open("hamb_penny.png")
    imagen_fondo = imagen_fondo.resize((201, 205), Image.LANCZOS)
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    frame = tk.Frame(ventana_ped, bg="black")
    frame.grid(row=0, column=0, sticky="nsew")  # Centra el marco en la ventana

    # Crear un Canvas para la imagen de fondo
    canvas_fondo = tk.Canvas(frame, width=201, height=205)
    canvas_fondo.grid(row=0, column=0, columnspan=1, padx=15, pady=15 )#, rowspan=2)  # Coloca la imagen debajo de la grilla

    # Mostrar la imagen de fondo en el Canvas
    canvas_fondo.create_image(0, 0, anchor="nw", image=imagen_fondo) 
    #frame.grid(row=0, column=0, padx=10, pady=10) 
    

    #ventana_ped.grid_rowconfigure(0, weight=1)  # Ajusta el tamaño de la fila
    #ventana_ped.grid_columnconfigure(0, weight=1)  # Ajusta el tamaño de la columna

   


    def validate_entry(text):
        return text.isalpha()

    # Variables
    #var_hamburguesa = tk.StringVar(value="Clásica")
    var_cliente = tk.StringVar()
    var_simple = tk.IntVar()
    var_doble = tk.IntVar()
    var_triple = tk.IntVar()
    var_postre = tk.IntVar()

    # Texto para el menú
    texto_menu = """    ••• Menú •••
    ● Combo Simple (Hamburguesa Simple) costo 5 usd.
    ●● Combo Doble (Hamburguesa Doble) costo 6 usd.
    ●●● Combo Triple (Hamburguesa Triple) costo 7 usd.

    ••• Postre •••
    ● McFlurby (Helado de dulce de leche) costo 2 usd.

    >  Todos los combos traen Bebida + papas fritas.  <"""

    # Crear el Label con el texto del menú #fc4b08
    label_menu = tk.Label(frame, text=texto_menu, font=("System", 11), wraplength=600, fg="white", justify="left", bg="black")
    label_menu.grid(row=0, column=1, columnspan=1, padx=1, pady=10)


    label_cliente = tk.Label(frame, text="Ingrese el nombre del cliente:", bg="black", fg="orange", font=("Arial Black", 14), justify="left")
    label_cliente.grid(row=2, column=0, sticky="e", padx=5, pady=5)
   
    # Entrada para el nombre del cliente
    caja_cliente = tk.Entry(frame, font=("Arial", 12), justify="center",bg="light yellow", validate="key", validatecommand=(ventana.register(validate_entry), "%S"))
    caja_cliente.grid(row=2, column=1, padx=6, pady=10)

    label_simple = tk.Label(frame, text="Ingrese la cantidad de combos simples:", bg="black", fg="yellow", font=("Arial Black", 12), justify="left")
    label_simple.grid(row=3, column=0, sticky="e", padx=5, pady=5)
    # Entrada para el nombre del cliente
    caja_simple = tk.Entry(frame, font=("Arial", 12), justify="center",bg="light yellow")
    caja_simple.grid(row=3, column=1, padx=5, pady=10)

    label_doble = tk.Label(frame, text="Ingrese la cantidad de combos dobles:", bg="black", fg="yellow", font=("Arial Black", 12), justify="left")
    label_doble.grid(row=4, column=0, sticky="e", padx=5, pady=5)
    # Entrada para el nombre del cliente
    caja_doble = tk.Entry(frame, font=("Arial", 12), justify="center",bg="light yellow")
    caja_doble.grid(row=4, column=1, padx=5, pady=10)

    label_triple = tk.Label(frame, text="Ingrese la cantidad de combos triples:", bg="black", fg="yellow", font=("Arial Black", 12), justify="left")
    label_triple.grid(row=5, column=0, sticky="e", padx=5, pady=5)
    # Entrada para el nombre del cliente
    caja_triple = tk.Entry(frame, font=("Arial", 12), justify="center",bg="light yellow")
    caja_triple.grid(row=5, column=1, padx=5, pady=10)

    label_postre = tk.Label(frame, text="Ingrese la cantidad de postres:", bg="black", fg="yellow", font=("Arial Black", 12), justify="left")
    label_postre.grid(row=6, column=0, sticky="e", padx=5, pady=5)
    # Entrada para el nombre del cliente
    caja_postre = tk.Entry(frame, font=("Arial", 12), justify="center",bg="light yellow")
    caja_postre.grid(row=6, column=1, padx=5, pady=10)
    #var_postre = caja_postre.get() * 2

    boton_tot = tk.Button(frame, text="Calcular Total", bg="yellow", font=("terminal", 12), justify="center", command=calcular_total)
    #label_muestra = tk.Label(frame, text=var_simple, font=("Arial", 12), wraplength=600, justify="left", bg="light blue")
    boton_tot.grid(row=7, column=1, columnspan=2, padx=10, pady=10)


    

    """
    # Cargar la imagen de fondo
    imagen_fondo = Image.open("hamb_penny.png")
    imagen_fondo = imagen_fondo.resize((800, 550), Image.LANCZOS)
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear un Canvas para la imagen de fondo
    canvas_fondo = tk.Canvas(frame, width=800, height=550)
    canvas_fondo.grid(row=10, column=0, columnspan=2)  # Coloca la imagen debajo de la grilla

    # Mostrar la imagen de fondo en el Canvas
    canvas_fondo.create_image(0, 0, anchor="nw", image=imagen_fondo)    
    #blanco = tk.Label(frame)
    #blanco.pack()
    """
    """
    texto_simple = tk.Label(frame,text="Ingrese la cantidad deel nombre del cliente que realiza el pedido:", bg = "black", fg = "yellow", font=("Arial", 14), justify="left")
   # cliente.place(x=20, y=380)
    cliente.pack()
    caja_cliente = tk.Entry(frame, font=("Arial", 14), justify="center")
   # caja_cliente.place(x=70, y=240, width=560, height=20)
    caja_cliente.pack()
    blanco = tk.Label(frame)
    blanco.pack()
    """
    # Ejecutar la aplicación
    ventana_ped.mainloop()


def apaga_sistema():
    ventana.quit()
    ventana.destroy()
    exit()

#crear la ventana
ventana = tk.Tk()
ventana.geometry("1024x768+0+0") #con esto arran bien arriba y bien a la izquierda
ventana.resizable(width=False, height=False)
#ventana.attributes("-topmost", True) #esto hace que siempre se ejecuta arriba de las demas ventanas
#Establecer un titulo de la ventana
ventana.title("Hambrgueseria PennyWise")
#cambio el icono de la ventana
ventana.iconbitmap("penny.ico")
#creo una imagen de fondo
imagen_de_fondo = tk.PhotoImage(file="Penny_fondo_hamb.png") 
label_fondo_inicio = tk.Label(ventana, image=imagen_de_fondo, anchor="center")
label_fondo_inicio.pack()
#tamaño de ventana
ventana.config(width=1024, height=768, bg="black")
#canvas = tk.Canvas(ventana, width=1024, height=640)
#canvas.pack()
# Agregar la imagen de fondo al widget Canvas
#canvas.create_image(0, 0, anchor=tk.NW, image=imagen_de_fondo)
#creo barra de menú
barra_menu = Menu(ventana)
ventana.config(menu=barra_menu)


def validate_entry(text):
    return text.isalpha()

#------- SOLAPA - INICIO -------##########
#creación de etiqueta 

etiqueta1=tk.Label(text="Coloque el nombre del encargad@ que ingresa: ", bg = "black", fg = "yellow",font=("Papyrus", 20), justify="center")# bg="#fa7785")
etiqueta1.place(relx=0.5, y=500, anchor="center")

# Crear la caja de texto para ingresar el nombre
caja1 = tk.Entry(font=("Arial", 20), justify="center", validate="key", validatecommand=(ventana.register(validate_entry), "%S"))
caja1.place(relx=0.5, y=570, width=410, height=40, anchor="center")


#crear un botón para interactuar
boton1=tk.Button(text="Guardar Nombre", bg="yellow", font=("terminal", 14), justify="center", command=Encargado)
#le doy un tamaño y una posición (xq sino TK no sabe donde colocarlo)
boton1.place(relx=0.5, y=650, width=180, height=35, anchor="center")




#etiqueta_error=tk.Label()
#etiqueta_error.place(x=40, y=500)


#######  CREACION DE OPCIONES DE MENÚ ########################

opcion_menu = Menu(barra_menu, tearoff=False)
opcion_menu.add_separator()
barra_menu.add_cascade(label="Inicio", menu=opcion_menu)
opcion_menu.add_command(label="Cambio de turno", command=cambio_de_turno)
ventana.update()
opcion_menu.add_separator()
opcion_menu.add_command(label="Registro encargad@s")
#---------------------------------------------------------------------
opcion_menu1 = Menu(barra_menu, tearoff=False)
barra_menu.add_cascade(label="Pedidos", menu=opcion_menu1)

opcion_menu1.add_command(label="Nuevo", command=pedidos_nuevos)
opcion_menu1.entryconfigure("Nuevo", state="disabled")
opcion_menu1.add_separator()
opcion_menu1.add_command(label="Registros pedidos")
#---------------------------------------------------------------------
opcion_menu2 = Menu(barra_menu, tearoff=False)
barra_menu.add_cascade(label="Salir", menu=opcion_menu2)
opcion_menu2.add_command(label="Apagar sistema", command=apaga_sistema)
#---------------------------------------------------------------------



#








#mostrar la ventana permanentemente
ventana.mainloop()

#command=lambda: cambiar_fondo("Pedidos")
