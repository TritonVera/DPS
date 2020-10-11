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
from math import pi, sqrt
from Line import CommLine, FindStar
import numpy as np

app = QApplication(sys.argv)
ui = UI()

def close(): #Закрыть

    sys.exit()


def plot_view(): #Построить

    change_modul()
    change_line()
    stars = FindStar(input_signal = NKP.signal).stars()

    ui.plot_panel.draw_plot(NKP.signal.data)
    ui.star_panel.draw_plot(stars)

def change_modul():
    
    Model.signal.phase = 0
    Model.signal.frequency = ui.signal_panel.freq_spinbox.value()
    Model.signal.time = ui.signal_panel.time_spinbox.value()
    if ui.modul_panel.combobox.currentText() == "BPSK":
        Modem.number = 2
        Modem.PM()
    elif ui.modul_panel.combobox.currentText() == "QPSK":
        Modem.number = 4
        Modem.PM()
    elif ui.modul_panel.combobox.currentText() == "8-PSK":
        Modem.number = 8
        Modem.PM()
    elif ui.modul_panel.combobox.currentText() == "QPSK со сдвигом":
        Model.signal.phase = pi/4
        Modem.number = 4
        Modem.PM()
    elif ui.modul_panel.combobox.currentText() == "APM8":
        Modem.number = 8
        Modem.APM()
    elif ui.modul_panel.combobox.currentText() == "APM16":
        Modem.number = 16
        Modem.APM()
    elif ui.modul_panel.combobox.currentText() == "FM":
        Modem.number = 2
        Modem.FM()

def change_line():

    ui.nf_panel.setVisible(1)
    if ui.line_panel.combobox.currentText() == "Канал без искажений":
        ui.nf_panel.setVisible(0)
        NKP.change_parameters(input_signal = Modem.signal, type_of_line = '')
    elif ui.line_panel.combobox.currentText() == "Гауссовская помеха":
        NKP.change_parameters(input_signal = Modem.signal, type_of_line = 'gauss', 
            dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Релеевская помеха":
        NKP.change_parameters(input_signal = Modem.signal, type_of_line = 'relei', 
            dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Гармоническая помеха":
        NKP.change_parameters(input_signal = Modem.signal, type_of_line = 'garmonic', 
            dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Линейные искажения":
        NKP.change_parameters(input_signal = Modem.signal, type_of_line = 'line_distor', 
            dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)

#Привязка кнопок
ui.button_panel.plot_button.clicked.connect(plot_view)
ui.line_panel.combobox.activated.connect(change_line)

# Конфигурирование модулятора
Modem = Modem()

Model.signal.time = ui.signal_panel.time_spinbox.value()
Model.signal.amplitude = 1
Model.signal.dots_per_osc = 50
Model.signal.frequency = ui.signal_panel.freq_spinbox.value()
Model.signal.phase = 0

Modem.number = 2
Modem.unit_time = 1/Model.signal.frequency

# Конфигурирование канала связи
NKP = CommLine()
""" Конец реализации конструктора """

ui.show()
sys.exit(app.exec_())
