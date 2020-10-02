#!/usr/bin/env bash
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 21:21:17 2020

@author: Григорий
@author: Ivan
"""
import sys  # System function
# import math

from PyQt5.QtWidgets import QApplication
from UI import DemoWindow as UI  # User interface classes
from Model import Model
from Modem import Modem
from math import pi
from Line import CommLine

app = QApplication(sys.argv)
ui = UI()

def close(): #Закрыть

    sys.exit()


def plot_view(): #Построить

    ui.plot_panel.draw_plot(NKP.output)

def bpsk():
    
    Modem.FM()

def qpsk():

	pass

def no_line():

	NKP.change_parameters(input_signal = Model.signal.value, type_of_line = '')

def gauss_line():

	NKP.change_parameters(input_signal = Model.signal.value, type_of_line = 'gauss', dispersion = 0.1, mu = 0)


#Привязка кнопок
ui.modul_panel.bpsk_radiobutton.clicked.connect(bpsk)
ui.modul_panel.qpsk_radiobutton.clicked.connect(qpsk)
ui.line_panel.no_noise_radiobutton.clicked.connect(no_line)
ui.line_panel.gauss_radiobutton.clicked.connect(gauss_line)
ui.button_panel.plot_button.clicked.connect(plot_view)
ui.button_panel.exit_button.clicked.connect(close)


# Конфигурирование модулятора
Modem = Modem()

Model.signal.time = 10
Model.signal.amplitude = 1
Model.signal.dots_per_osc = 50
Model.signal.frequency = 0.5
Model.signal.phase = 0

Modem.number = 2
Modem.unit_time = 1/Model.signal.frequency
Modem.FM()

# Конфигурирование канала связи
NKP = CommLine(input_signal = Model.signal.value)
""" Конец реализации конструктора """

ui.show()
sys.exit(app.exec_())