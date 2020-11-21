# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:08:55 2020

@author: Григорий
"""

# =============================================================================
# Класс сигнал - используется для формирования сигнала с заданными 
# параметрами.

# Возможно формирование как единственной точки (Метод Point),
# так и целого отрезка (Метод Unit). Для формирования отрезка требуется указать
# длительность сигнала (self.time).

# Метод Point возвращает точку [value, argument], точка также
# добавляется в соответствующие переменные экземпляра!!!
# =============================================================================

from math import pi, sin, cos
import numpy as np
from matplotlib import pyplot
from Convolution import Convolution

###############################################################################

class Signal():
  
  def __init__(self):

# Параметры точки сигнала:
      self.phase = 0                            # Начальная фаза
      self.frequency = 0                        # Частота
      self.amplitude = 1                        # Амплитуда    

# Параметры времени сигнала:
      self.time = 0                             # Длительность сигнала 
      self.dots = 0                             # Количество точек сигнала
      self.dots_per_osc = 50                    # Количество точек на колебание
      
# Сигнал:
      self.value = []                           # Значение сигнала
      self.argument = []                        # Аргумент сигнала
      self.data = np.zeros((2, 0))

# Текущий момент времени ед.времени:
      self.now = lambda x: x*self.time/self.dots
      
# Количество точек времени x:
      self.dots_num = lambda x: int(self.dots_per_osc * x * self.frequency)

#------------------------------------------------------------------------------
# Инициализация:
  def Init(self):
    
    self.Clear()
    self.dots = self.dots_num(self.time)

#------------------------------------------------------------------------------
# Очистка значений и аргументов сигнала:
      
  def Clear(self):                              

    self.argument.clear()
    self.value.clear()
    self.data = np.zeros((2, 0))

#------------------------------------------------------------------------------
# Расчет значения сигнала в точке time:
     
  def Point(self, now, phase_shift = 0, amp_inc = [1,1], freq_dev = 0):    
                                                 
    w0 = 2*pi*self.frequency
    w = 2*pi*freq_dev
    i_amp = self.amplitude * amp_inc[0]
    q_amp = self.amplitude * amp_inc[1]
    
    I = i_amp*cos(w * now + self.phase + phase_shift)
    Q = q_amp*sin(w * now + self.phase + phase_shift)
    S = I*sin(w0 * now) - Q*cos(w0 * now)

    self.value.append(S)
    self.argument.append(now)
    self.data = np.append(self.data, [[S], [now]], axis = 1)
    
    return([S, now])

#------------------------------------------------------------------------------
# Расчет отрезка self.time:
  
  def Unit(self, unit = None, phase_shift = 0, amp_inc = [1,1], freq_dev = 0):
    
    if unit != None:
      self.time = unit
      
    for i in range(0, self.dots):
      self.Point(self.now(i), phase_shift, amp_inc, freq_dev)

#------------------------------------------------------------------------------
# Отрисовка:  
      
  def Plot(self):                                
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (10,5))
    ax1.plot(self.argument, self.value)
     
#==============================================================================
# Отладка сигнала:
#
  def Test(self, phs = 0):
    
    self.phase = 0
    self.amplitude = 1
    self.frequency = 1
    self.time = 5
    
    self.Init()
    self.Unit(phase_shift = phs)
    
#=============================================================================
# Нахождение средней мощности сигнала
#

  def dispersion(self):
    return np.sum(self.data[0]**2)/self.data[0].size
    
#==============================================================================


class Garmonic():
    def __init__(self, in_i = 0, in_q = None, in_f = 0, in_phase = 0, in_time = 0, in_dev = 0):

        self.__I = in_i
        self.__var = 0
        if in_q != None:
            self.__Q = in_q
            self.__var = 1
        self.__w0 = 2*pi*in_f
        self.__phase = in_phase
        self.__time = np.array(in_time)
        self.__devia = 2*pi*in_dev

    def calc(self):

        if self.__var == 0:
            I = self.__I * np.cos(self.__devia * self.__time + self.__phase)
            Q = self.__I * np.sin(self.__devia * self.__time + self.__phase)
            return (I * np.sin(self.__w0 * self.__time)) - (Q * np.cos(self.__w0 * self.__time))
        else:
            return (self.__I * np.sin(self.__w0 * self.__time + self.__phase)) - \
                   (self.__Q * np.cos(self.__w0 * self.__time + self.__phase))

    def calc_with_time(self):
        return np.vstack((self.calc(), self.__time))
