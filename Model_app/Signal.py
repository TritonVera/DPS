# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:08:55 2020

@author: Григорий
"""

from math import pi, sin, cos
from matplotlib import pyplot
import numpy as np

class Signal():
  
  def __init__(self):
      
      self.time = 0                              #Длительность сигнала
      self.dots = 0                              #Количество точек сигнала
      self.dots_per_osc = 0                      #Количество точек на колебание
      
      self.phase = 0                             #Начальная фаза
      self.frequency = 0                         #Частота
      self.amplitude = 0                         #Амплитуда

      self.data = np.zeros((2, 1))
      # self.value = []
      # self.argument = []
      
  def clear(self):

    self.data = np.zeros((2, 0))

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
      
      self.data = np.append(self.data, [[S], [t]], axis = 1)
      # self.value.append(S)
      # self.argument.append(t)
      
  def Plot(self):                                #Отладочная отрисовка
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (10,5))
    ax1.plot(self.argument, self.value)


class Garmonic():
    def __init__(self, in_i = 0, in_f = 0, in_phase = 0, in_time = 0, in_dev = 0):

        self.__I = in_i
        self.__w0 = 2*pi*in_f
        self.__phase = in_phase
        self.__time = np.array(in_time)
        self.__devia = 2*pi*in_dev

    def calc(self):

        I = self.__I * np.cos(self.__devia * self.__time + self.__phase)
        Q = self.__I * np.sin(self.__devia * self.__time + self.__phase)
        return (I * np.sin(self.__w0 * self.__time)) - (Q * np.cos(self.__w0 * self.__time))