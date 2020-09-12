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
from Radiopulse import *
from ExciterObj import SignalCl
from math import pi

app = QApplication(sys.argv)
ui = UI()

def close(): #Закрыть

    sys.exit()


def plotb(): #Построить

    if ui.choose_panel.radio_radiobutton.isChecked():
        ui.plot_panel.draw_plot(radio.xpoints, radio.Ipoints, radio.Qpoints, radio.Zpoints)
    elif (ui.choose_panel.nlchm_radiobutton.isChecked() or ui.choose_panel.lchm_radiobutton.isChecked()):
        ui.plot_panel.draw_plot(radio_mod.Time, radio_mod.I, radio_mod.Q, radio_mod.Signal)
        ui.plot_panel.draw_addPlot(radio_mod.Time, radio_mod.Wt)


def radio_push():
    if ui.choose_panel.radio_radiobutton.isChecked():
        ui.plot_panel.add_plot.setVisible(0)

        ui.time_panel.time_stop_spinbox.setValue(20)
        ui.time_panel.time_stop_spinbox.setEnabled(1)
        ui.time_panel.time_start_spinbox.setValue(0)
        ui.time_panel.time_start_spinbox.setEnabled(1)
        ui.time_panel.auto_button.setEnabled(1)
        ui.time_panel.auto_spinbox.setEnabled(1)

        ui.setup_panel.time_spinbox.setVisible(1)
        ui.setup_panel.time_label.setVisible(1)
        ui.setup_panel.number_spinbox.setVisible(1)
        ui.setup_panel.number_label.setVisible(1)
        ui.setup_panel.phase_spinbox.setVisible(1)
        ui.setup_panel.phase_label.setVisible(1)

        ui.setup_panel.f_spinbox.setRange(0.1, 10)
        ui.setup_panel.f_spinbox.setDecimals(1)
        ui.setup_panel.f_spinbox.setValue(2)
        ui.setup_panel.f_spinbox.setSingleStep(0.1)

        ui.setup_panel.period_spinbox.setRange(0.1, 200)
        ui.setup_panel.period_spinbox.setValue(4)
        ui.setup_panel.period_spinbox.setSingleStep(0.1)

        ui.setup_panel.pulse_spinbox.setRange(0.01, 200)
        ui.setup_panel.pulse_spinbox.setValue(2)
        ui.setup_panel.pulse_spinbox.setSingleStep(0.1)

        ui.setup_panel.ku_i_label.setVisible(0)
        ui.setup_panel.ku_i_spinbox.setVisible(0)

        plotb()


def N_LNF(): #Н_ЛЧМ
    if ui.choose_panel.nlchm_radiobutton.isChecked():
        radio_mod.type_of_signal = "NLNF"
        ui.plot_panel.add_plot.show()
    elif ui.choose_panel.lchm_radiobutton.isChecked():
        radio_mod.type_of_signal = "LNF"
        ui.plot_panel.add_plot.show()

    ui.setup_panel.phase_spinbox.setVisible(0)
    ui.setup_panel.phase_label.setVisible(0)
    ui.setup_panel.ku_i_label.setVisible(0)
    ui.setup_panel.ku_i_spinbox.setVisible(0)

    ui.setup_panel.time_spinbox.setVisible(0)
    ui.setup_panel.time_label.setVisible(0)
    ui.setup_panel.number_spinbox.setVisible(0)
    ui.setup_panel.number_label.setVisible(0)

    ui.time_panel.time_stop_spinbox.setEnabled(1)
    ui.time_panel.time_stop_spinbox.setValue(100)
    ui.time_panel.time_start_spinbox.setEnabled(1)
    ui.time_panel.time_start_spinbox.setValue(0)
    ui.time_panel.auto_button.setEnabled(1)
    ui.time_panel.auto_spinbox.setEnabled(1)


    ui.setup_panel.f_spinbox.setRange(0.0001,1)
    ui.setup_panel.f_spinbox.setDecimals(4)
    ui.setup_panel.f_spinbox.setValue(0.1)
    ui.setup_panel.f_spinbox.setSingleStep(0.0001)

    ui.setup_panel.pulse_spinbox.setRange(0.01,200)
    ui.setup_panel.pulse_spinbox.setValue(100)

    ui.setup_panel.period_spinbox.setRange(0.01,2000)
    ui.setup_panel.period_spinbox.setSingleStep(0.01)
    ui.setup_panel.period_spinbox.setValue(1000)

    radio_mod.Configure_values(F = ui.setup_panel.f_spinbox.value())
    redraw_plot_time()
    
    

def redraw_plot_time():
    ui.time_panel.time_start_spinbox.setMaximum(ui.time_panel.time_stop_spinbox.value() - 0.1)
    ui.time_panel.time_stop_spinbox.setMinimum(ui.time_panel.time_start_spinbox.value() + 0.1)
    if (ui.time_panel.auto_button.isChecked() == 0):
        start = ui.time_panel.time_start_spinbox.value()
        stop = ui.time_panel.time_stop_spinbox.value()
        if (stop > start):
            if ui.choose_panel.radio_radiobutton.isChecked():
                radio.time_configure(start_time = start, end_time = stop)
            else:
                radio_mod.Configure_time(Start = start, Stop = stop)
            plotb()

def redraw_plot():
    if (ui.choose_panel.radio_radiobutton.isChecked()):
        ui.setup_panel.pulse_spinbox.setMaximum(ui.setup_panel.period_spinbox.value())
        ui.setup_panel.period_spinbox.setMinimum(ui.setup_panel.pulse_spinbox.value())
        ui.setup_panel.period_spinbox.setMaximum(ui.setup_panel.time_spinbox.value() / 
                                                 ui.setup_panel.number_spinbox.value())
        ui.setup_panel.time_spinbox.setMinimum(ui.setup_panel.period_spinbox.value() * 
                                               ui.setup_panel.number_spinbox.value())
        ui.setup_panel.number_spinbox.setMaximum(round(ui.setup_panel.time_spinbox.value() / 
                                                 ui.setup_panel.period_spinbox.value()))
        radio.configure(frequency = ui.setup_panel.f_spinbox.value(), 
                        amplify_i = ui.setup_panel.ku_i_spinbox.value(),
                        amplify_q = ui.setup_panel.ku_i_spinbox.value(),
                        length = ui.setup_panel.pulse_spinbox.value(),
                        period_pulse = ui.setup_panel.period_spinbox.value(),
                        number = ui.setup_panel.number_spinbox.value(),
                        period_packet = ui.setup_panel.time_spinbox.value(),
                        phase = ui.setup_panel.phase_spinbox.value())
        if (ui.time_panel.auto_button.isChecked()):
            ui.time_panel.time_stop_spinbox.setValue(radio.xpoints[-1])
            ui.time_panel.time_start_spinbox.setValue(radio.xpoints[0])
            radio.auto(50, ui.time_panel.auto_spinbox.value())
        else:
            radio.time_configure()
        plotb()

    if (ui.choose_panel.nlchm_radiobutton.isChecked() or ui.choose_panel.lchm_radiobutton.isChecked()):
        radio_mod.Configure_values(Amplify_I = ui.setup_panel.ku_i_spinbox.value(),
                                   Amplify_Q = ui.setup_panel.ku_i_spinbox.value(),
                                   F = ui.setup_panel.f_spinbox.value(),
                                   Imp = ui.setup_panel.pulse_spinbox.value(),
                                   T = ui.setup_panel.period_spinbox.value())
        if (ui.time_panel.auto_button.isChecked()):
            ui.time_panel.time_stop_spinbox.setValue(radio_mod.Time[-1])
            ui.time_panel.time_start_spinbox.setValue(radio_mod.Time[0])
            radio_mod.AutoGen(50, ui.time_panel.auto_spinbox.value())
            plotb()
        else:
            redraw_plot_time()
        

def auto_but():
    if (ui.time_panel.auto_button.isChecked()):
        ui.time_panel.time_stop_spinbox.setEnabled(0)
        ui.time_panel.time_start_spinbox.setEnabled(0)
        ui.timer.start(20)
        ui.time_panel.auto_button.setText("Стоп")
    else:
        ui.timer.stop()
        ui.time_panel.time_stop_spinbox.setEnabled(1)
        ui.time_panel.time_start_spinbox.setEnabled(1)
        ui.time_panel.auto_button.setText("Запуск")

def visible_i():
    if ui.graph_panel.I_box.isChecked():
        ui.plot_panel.i_flag = 1
        plotb()
    else:
        ui.plot_panel.i_flag = 0
        plotb()

def visible_q():
    if ui.graph_panel.Q_box.isChecked():
        ui.plot_panel.q_flag = 1
        plotb()
    else:
        ui.plot_panel.q_flag = 0
        plotb()

def visible_z():
    if ui.graph_panel.Z_box.isChecked():
        ui.plot_panel.z_flag = 1
        plotb()
    else:
        ui.plot_panel.z_flag = 0
        plotb()

#Привязка кнопок
ui.choose_panel.radio_radiobutton.toggled.connect(radio_push)
ui.choose_panel.lchm_radiobutton.toggled.connect(N_LNF)
ui.choose_panel.nlchm_radiobutton.toggled.connect(N_LNF)
ui.button_panel.exit_button.clicked.connect(close)
ui.time_panel.auto_button.toggled.connect(auto_but)
ui.graph_panel.I_box.toggled.connect(visible_i)
ui.graph_panel.Q_box.toggled.connect(visible_q)
ui.graph_panel.Z_box.toggled.connect(visible_z)

#Привязка изменения значения в спинбоксах
ui.setup_panel.phase_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.ku_i_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.f_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.time_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.pulse_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.period_spinbox.valueChanged.connect(redraw_plot)
ui.setup_panel.number_spinbox.valueChanged.connect(redraw_plot)
ui.time_panel.time_stop_spinbox.valueChanged.connect(redraw_plot_time)
ui.time_panel.time_start_spinbox.valueChanged.connect(redraw_plot_time)

# Привязка таймера
ui.timer.timeout.connect(redraw_plot)

radio = Radiopulse()
radio_mod = SignalCl() 
""" Конец реализации конструктора """

ui.show()
sys.exit(app.exec_())