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
from Processor import Processor

#------------------------------------------------------------------------------
# Текстовый режим
#------------------------------------------------------------------------------
# Создание объектов Model:

Modem = Modem()
Processor = Processor()

#------------------------------------------------------------------------------
# Ввод параметров сигнала:
# TODO Закоментировано всё от чего параметры несущего сигнала не зависят

# Model.signal.time = 10
# Model.signal.amplitude = 1
# Model.signal.dots_per_osc = 50
Model.signal.frequency = 1
# Model.signal.phase = 0

# Модулятор тоже выключил так, как все равно сигнал измениться в любом режиме работы
# Modem.number = 4
# Modem.code_type = "full"
# Предлагаю задать длительность символа константой, и варировать ее от частоты несущей
# Modem.unit_time = 2/Modem.signal.frequency

NKP = CommLine()

if int(input("1. Графический режим\r\n2. Текстовый режим\n")) == 1:
    app = QApplication(sys.argv)
    ui = UI()

    manage = Controller(ui, Modem, NKP, Processor)
    ui.button_panel.plot_button.clicked.connect(manage.plot_view)
    ui.line_panel.combobox.activated.connect(manage.show_param)
    ui.error_panel.combobox.activated.connect(manage.show_error)
    # ui.show_panel.fft.toggled.connect(manage.show_fft)

    ui.show()
    sys.exit(app.exec_())

else:
    Modem.number = 4
    Modem.code_type = "full"
    Modem.PM()
    Model.signal.Plot()
    #Model.signal.Simple()

    # Обертка канала связи
    NKP.change_parameters(input_signal = Model.signal, 
                        type_of_line = 'gauss', dispersion = 1, mu = 0)
    Model.signal = NKP.signal

    Processor.Init(Modem)
    # Тут преобразования сигнала до приема
    Processor.Receive()
    Processor.ConvolutionPlot()
    # Просто дебаг информация
    print(NKP.get_input())
