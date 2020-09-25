# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:08:55 2020

@author: Григорий
"""

from math import pi, sin, cos
from matplotlib import pyplot

class Signal():
  
  def __init__(self):
      
      self.time = 0                              #Длительность сигнала
      self.dots = 0                              #Количество точек сигнала
      self.dots_per_osc = 0                      #Количество точек на колебание
      
      self.phase = 0                             #Начальная фаза
      self.frequency = 0                         #Частота
      self.amplitude = 0                         #Амплитуда

      self.value = []
      self.argument = []
      
  def Dots(self):                                #Расчет dots
    
    self.dots = int(self.dots_per_osc * self.time * self.frequency)
      
  def Point(self, t, phase_shift = 0, amplitude_inc = 1, frequency_deviation = 0):    
                                                 
      w0 = 2*pi*self.frequency
      w = 2*pi*frequency_deviation
      i_amp = self.amplitude * amplitude_inc
      q_amp = self.amplitude * amplitude_inc
      
      I = i_amp*cos(w * t + self.phase + phase_shift)
      Q = q_amp*sin(w * t + self.phase + phase_shift)
      S = I*sin(w0 * t) - Q*cos(w0 * t)
      
      self.value.append(S)
      self.argument.append(t)
      
  def Plot(self):                                #Отладочная отрисовка
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (10,5))
    ax1.plot(self.argument, self.value)