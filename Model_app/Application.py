# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:27:40 2020

@author: Григорий
"""

from Model import Model
from Modem import Modem
from Processor import Processor

#------------------------------------------------------------------------------
# Текстовый режим
#------------------------------------------------------------------------------
# Создание объектов Model:

Modem = Modem()
Processor = Processor()

#------------------------------------------------------------------------------
# Ввод параметров сигнала:

Model.signal.time = 10
Model.signal.amplitude = 1
Model.signal.dots_per_osc = 50
Model.signal.frequency = 5
Model.signal.phase = 0

#------------------------------------------------------------------------------
# Ввод параметров модулятора:

Modem.number = 4
Modem.code_type = "full"

#Modem.unit_time = 20/Modem.signal.frequency

#------------------------------------------------------------------------------
# Расчет:

Modem.PM()
Modem.signal.Plot()
Processor.Init(Modem)
# Тут преобразования сигнала до приема
Processor.Receive()
Processor.ConvolutionPlot()
