# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:10:40 2020

@author: Григорий
"""

# =============================================================================
# Класс имеет три атрибута:
#
#    self.raw_signal      Исследуемый сигнал
#    self.support_signal  Опорный сигнал
#    self.convolution     Результат свертки
#
# Методы класса:
#
#    self.ConvolutionPlot
#    self.Convolution
#    self.SignalCheck
#    self.Detecter
#
# Detecter и Convolution требуют на входе опорный и исследуемый сигналы, 
# результат Convolution записывается в соответствующий атрибут, для Detecter
# длины входных сигнал требуются одинаковыми
# =============================================================================

from matplotlib import pyplot
from math import log10,sqrt

###############################################################################

class Processor():
  
  def __init__(self):
    
    self.raw_signal = []
    self.support_signal = []
    self.convolution = []
    
    self.dB = lambda x: 10*log10(x)

#------------------------------------------------------------------------------  
  
  def SignalCheck(self):
    
    print("")
    
    in1 = self.support_signal
    in2 = self.raw_signal
      
    level = self.Detecter(in1,in2)
    print(" level ",'{0:8.4f}'.format(level), " dB")

#------------------------------------------------------------------------------
  
  def Detecter(self, support, signal):
    
    temp = 0
    for i in range(0, len(signal)):
      temp = temp + signal[i]*support[i]
    
    temp = abs(temp)/self.__norma(support, support)
    return(self.dB(temp))

#------------------------------------------------------------------------------
      
  def ConvolutionPlot(self, parametr = None ):
    
    in1 = self.support_signal
    in2 = self.raw_signal
    
    if parametr == "self":
      in2 = in1
      
    value = self.Convolution(in1, in2)
    argument = [i for i in range(0, len(value))]
    
    pyplot.plot(argument, value)

#------------------------------------------------------------------------------
  
  def __norma(self, in1, in2):

    temp1 = 0
    temp2 = 0
    for j in range(0, max(len(in1), len(in2))):
      if j < len(in1):
        temp1 = temp1 + abs(in1[j])**2
      if j < len(in2):
        temp2 = temp2 + abs(in2[j])**2

    temp = sqrt(temp1*temp2)
    return(temp)

#------------------------------------------------------------------------------

  def __LRConvolution(self, in1, in2):
    
    value1 = []
    value2 = []
  
    for i in range(0, len(in1)):
      temp1 = 0
      temp2 = 0
      for j in range(0, i):
            temp1 = temp1 + in1[-i+j] * in2[j]
            temp2 = temp2 + in1[j] * in2[-i+j]
        
      value1.append(abs(temp1))
      value2.append(abs(temp2))
      
    value2.reverse()
    
    return(value1, value2)
  
#------------------------------------------------------------------------------  
  
  def __CConvolution(self, in1, in2):
    
      value = []
  
      for i in range(0, len(in2)-len(in1) + 1):
        temp = 0
        for j in range(0, len(in1)):
          temp = temp + in1[j]*in2[i+j]    
        value.append(abs(temp))
  
      return(value)
      
#------------------------------------------------------------------------------

  def Convolution(self, in1, in2):
    
    norma = self.__norma(in1,in1)
    normalisation = lambda x: x/norma
    
    v0, v2 = self.__LRConvolution(in1, in2)
    v1 = self.__CConvolution(in1, in2)

    value = v0 + v1 + v2
      
    value = list(map(normalisation, value))
    self.convolution = value
    
    return(value)
