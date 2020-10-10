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


class Garmonic():
    def __init__(self, in_i = 1, in_q = 0, in_w0 = 0, in_phase = 0, in_time = 0, in_dev = 0):

        self.I = in_i
        self.Q = in_q
        self.w0 = 2*pi*in_w0
        self.phase = in_phase
        self.time = np.array(in_time)
        self.dev = 2*pi*in_dev
        self.output = np.array(self.time)

    def calc(self):
        print(self.w0)
        for t in range(self.time.size):
            I = self.I*cos(self.dev * self.time[t] + self.phase)
            Q = self.Q*sin(self.dev * self.time[t] + self.phase)
            self.output.put(t, I*sin(self.w0 * self.time[t]) - Q*cos(self.w0 * self.time[t]))
            print(self.w0 * self.time[t])
        return self.output