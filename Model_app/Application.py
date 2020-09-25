# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:27:40 2020

@author: Григорий
"""

from Model import Model
from Signal import Signal
from Modem import Modem
from Line import CommLine

Modem = Modem()
NKP = CommLine()

Model.signal.time = 10
Model.signal.amplitude = 1
Model.signal.dots_per_osc = 50
Model.signal.frequency = 0.5
Model.signal.phase = 0

Modem.unit_time = 1

#Model.signal.Simple()
Modem.FM_2()
Model.signal.Plot()

# Обертка канала связи
NKP.change_parameters(input_signal = Model.signal.value, 
      				  type_of_line = 'gauss', dispersion = 1, mu = 0)
Model.signal.value = NKP.output

# Просто дебаг информация
NKP.print_input()
print("\n\n")
NKP.print_output()
