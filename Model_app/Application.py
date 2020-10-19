# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:27:40 2020

@author: Григорий
"""
import sys

from PyQt5.QtWidgets import QApplication
from UI import DemoWindow as UI
from Model import Model
from Modem import Modem
from Line import CommLine
from Controller import Controller

Modem = Modem()

Modem.signal.time = 16
Modem.signal.amplitude = 1
Modem.signal.dots_per_osc = 50
Modem.signal.frequency = 1
Modem.signal.phase = 0

Modem.number = 2
Modem.unit_time = 2/Modem.signal.frequency

NKP = CommLine()

mode = int(input("1. Графический режим\n2. Текстовый режим\n"))

if mode == 1:
	app = QApplication(sys.argv)
	ui = UI()

	manage = Controller(ui, Modem, NKP)
	ui.button_panel.plot_button.clicked.connect(manage.plot_view)
	ui.line_panel.combobox.activated.connect(manage.show_param)

	ui.show()
	sys.exit(app.exec_())

else:
	#Modem.PM()
	#Modem.APM()
	Modem.FM()
	# Model.signal.Plot()
	#Model.signal.Simple()

	# Обертка канала связи
	NKP.change_parameters(input_signal = Model.signal, 
      				  	type_of_line = 'gauss', dispersion = 1, mu = 0)
	Model.signal = NKP.signal

	# Просто дебаг информация
	print(NKP.get_input())
