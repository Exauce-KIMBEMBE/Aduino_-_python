#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   * e-mail : openprogramming32@gmail.com
   * gitHub : https://github.com/RS-malik-el
   * Donation : paypal.me/RachelSysteme
   *
   * @AUTEUR : EXAUCE KIMBEMBE / @OpenProgramming
   * DATE : 23/06/2023
   *
   * Testé sous Windows, ce code a pour but de créer une petite interface 
   * qui transmet les données via le port série.
"""

import tkinter as tk
import threading
import serial

PORT     = "COM5" # Remplacer par le port valide
BAUDRATE = 9600   # Remplacer par baudrate utilisé
TIMEOUT  = 1      # Délais d'attente
NB_CHAR  = 30     # Nombre maximun des caractères à saisir
FONT     = ("Arial","12", "bold") 

# Limitation du nombre des caractères
def LimitChar():
	global saisie
	
	entree = str(saisie.get())
	saisie.set(entree[:NB_CHAR])

# Fermeture de la fenêtre
def close():
	global stop_thread, autoUpdateRoutine, arduino, app
	
	stop_thread.set() # Déclenche l'événement sur le thread pour lui mettre fin. 
	autoUpdateRoutine.join() # Attente que le thread prenne fin
	arduino.close()
	app.destroy()

# Transfert des données via le port série
def sendData(master=None):
	global arduino, saisie, run

	if run == True:
		try:
			arduino.flushOutput()
			if str(saisie.get()) != "":
				arduino.write(str(saisie.get()).encode("utf-8"))
				print("Data send ---> {}".format(str(saisie.get())))
				saisie.set("")
		except serial.serialutil.SerialException:
			print("Port indisponible")
			close()

# Reception des données via le port série
def reception():
	global stop_thread, arduino, run

	if run == True:
		# S'exécute tant qu'aucun événement, c'est produit dans le thread
		while not stop_thread.is_set():
			try:	
				data = arduino.readline()
				data = str(data.decode("utf-8"))

				if data != "":
					print("Data receive ---> {}".format(data))
			except serial.serialutil.SerialException:
				print("Port indisponible")
				break;


# Tentative d'établissement de la connexion série
try:
	arduino = serial.Serial(port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
	print("Connecté : port valide")	
	run = True
	autoUpdateRoutine = threading.Thread(target=reception)
	"""un objet Event() est un mécanisme simple pour la synchronisation entre threads. 
	   Il est généralement utilisé pour signaler à un ou plusieurs threads qu'un événement s'est produit.
	"""
	stop_thread = threading.Event()
	autoUpdateRoutine.start()
except serial.serialutil.SerialException:
	print("Non connecté : port non valide")		
	run = False

# Création de l'interface
if run == True:
	app = tk.Tk()
	app.geometry("480x50")
	app.title("Serial send data")
	app.resizable(width=False, height=False)
	
	saisie = tk.StringVar()	
	frame = tk.Frame(app).grid(row=1, column=3, columnspan=3)
	tk.Label(frame, text="Saisie :", width=8, relief=tk.FLAT, font=FONT).grid(row=0,column=0)
	tk.Entry(frame, textvariable=saisie, width=NB_CHAR, font=FONT, fg="blue").grid(padx=10, pady=15, row=0, column=1)
	tk.Button(frame, text="Entrée", width=7, relief=tk.GROOVE,command=sendData, font=FONT).grid(row=0, column=2)
	# Limitation du nombre des caractères a saisir
	saisie.trace("w", lambda *args: LimitChar())

	#
	app.protocol("WM_DELETE_WINDOW", close) 
	app.mainloop()