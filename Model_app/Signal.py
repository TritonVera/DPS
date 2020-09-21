# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:08:55 2020

@author: Григорий
"""

from math import pi, sin
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
      
  def Simple(self):                              #Формирование сигнала
                                                 #без модуляции
    self.Dots()
    for i in range(0, self.dots):
      
      now = i*self.time/self.dots
      w = 2*pi*self.frequency
      temp_value = self.amplitude*sin(w*now + self.phase)
      
      self.value.append(temp_value)
      self.argument.append(now)
      
  def PS_Value(self, phase_shift, now):          #Запись единичного значения
                                                 #сигнала с фазовым сдвигом
      w = 2*pi*self.frequency
      temp_value = self.amplitude*sin(w*now + self.phase + phase_shift)
      
      self.value.append(temp_value)
      self.argument.append(now)    
      
  def Plot(self):                                #Отладочная отрисовка
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (10,5))
    ax1.plot(self.argument, self.value)