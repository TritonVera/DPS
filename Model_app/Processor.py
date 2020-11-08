# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:10:40 2020

@author: Григорий
"""

# =============================================================================
# Класс - процессор
# =============================================================================

from Model import Model
from Convolution import Convolution
from matplotlib import pyplot

###############################################################################

class Processor(Model):
  
  def __init__(self):
 
  # Атрибуты процессора:
    self.raw_signal = []                                   # Исследуемый сигнал
    self.support_signal = []                               # Опорный сигнал
    self.convolution = []                                  # Результат свертки

#------------------------------------------------------------------------------  
# Инициализация:
  
  def Init(self, Modem):
    
    self.support_signal.append(self.signal.value.copy())
    self.support_signal.append(self.signal.value_i.copy())
    self.support_signal.append(self.signal.value_q.copy())
    
    self.argument = self.signal.argument.copy()
    self.number = Modem.number
    self.unit_dots = Modem.unit_dots
    
#------------------------------------------------------------------------------  
# Прием:
    
  def Receive(self):
    
    self.raw_signal = self.signal.value.copy()    
 
    temp = self.support_signal[0][:self.unit_dots].copy()
    temp.reverse()
    self.convolution.append(Convolution(temp, self.raw_signal))
    
#------------------------------------------------------------------------------
# Отрисовка результата свертки:
    
  def ConvolutionPlot(self):
    
    
    in1 = self.support_signal[0][:self.unit_dots]
    in2 = self.convolution[0]
    
    argument1 = self.argument[:self.unit_dots]
    argument2 = [i for i in range(0, len(in2))]
    
    fig,(ax2, ax3) = pyplot.subplots(2,1, figsize = (10,10))
    ax2.plot(argument1, in1)
    ax3.plot(argument2, in2)

