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
      self.value_i = []                         # Значение сигнала
      self.value_q = []                         # Значение сигнала
      self.value = []                           # Значение сигнала
      self.argument = []                        # Аргумент сигнала

# Текущий момент времени ед.времени:
      self.now = lambda x: x*self.time/self.dots
      
# Количество точек времени x:
      self.dots_num = lambda x: int(self.dots_per_osc * x * self.frequency)

#------------------------------------------------------------------------------
# Инициализация:
  def Init(self):
    
    self.Clear()
    self.Dots()

#------------------------------------------------------------------------------
# Очистка значений и аргументов сигнала:
      
  def Clear(self):                              

    self.argument.clear()
    self.value.clear()
    self.value_i.clear()
    self.value_q.clear()

#------------------------------------------------------------------------------
# Расчет количества точек сигнала:
    
  def Dots(self):                               
    
    self.dots = self.dots_num(self.time)

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

    self.value_i.append(I)
    self.value_q.append(Q)
    self.value.append(S)
    self.argument.append(now)
    
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
    
# =============================================================================
#s1 = Signal()
#s2 = Signal()
#s1.Test()
#s2.Test(1*pi/4)
#
#mult = lambda x,y: [x[i]*y[i] for i in range(0, len(x))] 
#
#value1 = Convolution(s1.value, s1.value)
#value2 = Convolution(s1.value, s2.value)
#
#a = s1.value.copy()
#b = s2.value.copy()
#b.reverse()
#
#value3 = np.cumsum([mult(a,b)])
#
#argument1 = [i for i in range(0, len(value1))]
#argument2 = [i for i in range(0, len(value3))]
#
#fig,(ax1, ax2, ax3) = pyplot.subplots(3,1, figsize = (10,20))
#ax1.plot(s1.argument, s1.value)
#ax1.plot(s2.argument, s2.value)
#ax2.plot(argument1, value1)
#ax2.plot(argument1, value2)
#ax3.plot(argument2, value3)
# =============================================================================

    
