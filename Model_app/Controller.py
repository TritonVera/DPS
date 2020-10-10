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

    if ui.modul_panel.combobox.currentText() == "APM":
        Modem.APM()
    elif ui.modul_panel.combobox.currentText() == "FM":
        Modem.FM()
    else:
        Modem.PM()
    NKP.change_parameters(input_signal = Modem.signal)
    Modem.signal.value = NKP.output.tolist()
    stars = FindStar(input_signal = Modem.signal).stars()

    ui.plot_panel.draw_plot(NKP.output)
    ui.star_panel.draw_plot(stars[0, :], stars[1, :])

def change_modul():
    
    Model.signal.phase = 0
    if ui.modul_panel.combobox.currentText() == "BPSK":
        Modem.number = 2
    elif ui.modul_panel.combobox.currentText() == "QPSK":
        Modem.number = 4
    elif ui.modul_panel.combobox.currentText() == "8-PSK":
        Modem.number = 8
    elif ui.modul_panel.combobox.currentText() == "QPSK со сдвигом":
        Model.signal.phase = pi/4
        Modem.number = 4

def change_line():

    ui.nf_panel.setVisible(1)
    if ui.line_panel.combobox.currentText() == "Канал без искажений":
        ui.nf_panel.setVisible(0)
        NKP.change_parameters(type_of_line = '')
    elif ui.line_panel.combobox.currentText() == "Гауссовская помеха":
        NKP.change_parameters(type_of_line = 'gauss', dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Релеевская помеха":
        NKP.change_parameters(type_of_line = 'relei', dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Гармоническая помеха":
        NKP.change_parameters(type_of_line = 'garmonic', dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)
    elif ui.line_panel.combobox.currentText() == "Линейные искажения":
        NKP.change_parameters(type_of_line = 'line_distor', dispersion = sqrt(0.707/ui.nf_panel.noise_factor_spinbox.value()), mu = 0)

#Привязка кнопок
ui.modul_panel.combobox.activated.connect(change_modul)
ui.line_panel.combobox.activated.connect(change_line)
ui.nf_panel.noise_factor_spinbox.valueChanged.connect(change_line)
ui.button_panel.plot_button.clicked.connect(plot_view)
# ui.button_panel.exit_button.clicked.connect(close)


# Конфигурирование модулятора
Modem = Modem()

Model.signal.time = 100
Model.signal.amplitude = 1
Model.signal.dots_per_osc = 50
Model.signal.frequency = 0.5
Model.signal.phase = 0

Modem.number = 2
Modem.unit_time = 1/Model.signal.frequency

# Конфигурирование канала связи
NKP = CommLine()
""" Конец реализации конструктора """

ui.show()
sys.exit(app.exec_())
