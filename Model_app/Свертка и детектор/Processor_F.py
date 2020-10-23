# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 00:00:52 2020

@author: Григорий
"""

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
      
  def ConvolutionPlot(self, parametr = None ):
    
    in1 = self.support_signal
    in2 = self.raw_signal
    
    if parametr == "self":
      in2 = in1
      
    value = self.Convolution(in1, in2)
    argument = [i for i in range(0, len(value))]
    
    pyplot.plot(argument, value)

#------------------------------------------------------------------------------

  def __LRConvolution(self, in1, in2):
    
    value1 = []
    value2 = []
  
    for i in range(0, len(in1)):
      temp1 = 0
      temp2 = 0
      for j in range(0, i):
        if in1[-i+j] == in2[j]:
          temp1 = temp1 + 1
        if in1[j] == in2[-i+j]:
          temp2 = temp2 + 1
    
      temp1 = temp1 - (len(in1) - temp1) + len(in1) - i
      temp2 = temp2 - (len(in1) - temp2) + len(in1) - i
      value1.append(temp1)
      value2.append(temp2)
      
    value2.reverse()
    
    return(value1, value2)
  
#------------------------------------------------------------------------------  
  
  def __CConvolution(self, in1, in2):
    
      value = []
  
      for i in range(0, len(in2)-len(in1) + 1):
        temp = 0
        for j in range(0, len(in1)):
          if in1[j] == in2[i+j]:
            temp = temp + 1
        temp = temp - (len(in1) - temp)    
        value.append(temp)
  
      return(value)
      
#------------------------------------------------------------------------------

  def Convolution(self, in1, in2):
    
    normalisation = lambda x: x/len(in1)
    
    v0, v2 = self.__LRConvolution(in1, in2)
    v1 = self.__CConvolution(in1, in2)

    value = v0 + v1 + v2
      
    value = list(map(normalisation, value))
    self.convolution = value
    
    return(value)
