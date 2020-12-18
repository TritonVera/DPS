# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 21:10:40 2020

@author: Григорий
"""

# =============================================================================
# Класс - процессор, требует инициализации (self.Init) сразу после
# применения модулятора. Накапливает сигнал посимвольно.
# =============================================================================

from Model import Model
from Signal import Garmonic  # TODO Копирую для своей функции
import numpy as np
from matplotlib import pyplot

###############################################################################

class Processor(Model):
  
  def __init__(self):
 
  # Атрибуты процессора:
    self.raw_signal = []                                  # Исследуемый сигнал
    self.support_signal = []                              # Опорный сигнал
    self.convolution = []                                 # Результат свертки
    self.sgn_mul = []                                     # Перемножение сигналов
    self.convolution_Q = []
    self.sgn_mul_Q = []
    self.number = 0                                       # Количесвто символов
    self.unit_dots = 0                                    # Точек на символ
  
  # Перемножение двух массивов  
    self.mult = lambda x,y: [x[i]*y[i] for i in range(0, len(x))]  

#------------------------------------------------------------------------------  
# Инициализация:
# Должна происходить сразу после применения модулятора, т.к в качестве опорного
# сигнала записывается сигнала с модулятора до искажений..

# TODO Предлагаю записывать в опорный только часть сигнала (5 первых отсчетов, 
# как в старой программе), чтобы выводить корреляцию только для первых 5 символов.
# Остальные символы будем использовать для созвездия и вероятности ошибки
   
  def Init(self, Modem):
      
    self.number = Modem.number
    self.unit_dots = Modem.unit_dots
    self.vis_symbol = Modem.sym_number
    
    self.support_signal = self.signal.value
    self.time = self.signal.data[1, 0:int(self.unit_dots)]  # Для некогерентого приемника
    self.convolution = []
    self.sgn_mul = []
    self.convolution_Q = []
    self.sgn_mul_Q = []
    self.data = []
    # self.support_signal = self.signal.value.copy()                             # Записываем опорный сигнал

#------------------------------------------------------------------------------  
# Прием: TODO Приемник для ФМ-2 таким образом не срабатывает, я написал по аналогии
# свою функцию.
    
  def Receive(self, sign = []):
    
    # TODO Блок проверки наличия входных парметров, так как линия не наследуется
    if sign == []:
      self.raw_signal = self.signal.value.copy()
    else:
      self.raw_signal = sign
 
    for i in range(0, self.vis_symbol):                                             # Цикл по символам
      n = self.unit_dots
      temp0 = self.support_signal[i * n: (i + 1)*n]                             # Отсчеты одного символа
      temp1 = self.raw_signal[i * n: (i + 1)*n]
      temp = self.mult(temp0, np.flip(temp1))                                   # Кумулятивная сумма по символу

      self.convolution = np.append(self.convolution, np.cumsum(temp))        # Запись результата накопления символа
      self.sgn_mul = np.append(self.sgn_mul, temp)                           # Результат перемножения
    
#------------------------------------------------------------------------------
# TODO Моя аналогичная функция приёмника

  def ReceiveV2(self, sgn = [], dev = 0, phase = 0):
      
    # Блок проверки наличия входных парметров, так как линия не наследуется
    if sgn == []:
      self.raw_signal = self.signal.data[0]
    else:
      self.raw_signal = sgn

    # Предлагаю сгенирировать 2 сигнала для I и Q компоненты и их сравнивать с сырым
    I = Garmonic(in_i = 1, in_f = (1 + dev) * self.signal.frequency,
                 in_phase = phase,
                 in_time = self.time).calc()
    Q = Garmonic(in_q = 1, in_f = (1 + dev) * self.signal.frequency, 
                 in_phase = phase,
                 in_time = self.time).calc()
    self.data = np.zeros(self.vis_symbol, dtype = np.complex)
    for i in range(0, self.vis_symbol):               # Цикл по символам
      n = self.unit_dots
      # Сигнал напрямую с модема не нужен (в реальных системах мы его вообще не знаем)
      temp1 = self.raw_signal[i * n: (i + 1)*n]
      temp_I = self.mult(I, np.flip(temp1))                                    # Кумулятивная сумма по символу
      temp_Q = self.mult(Q, np.flip(temp1))                                    # Кумулятивная сумма по символу для Q

      self.convolution = np.append(self.convolution, np.cumsum(temp_I))        # Запись результата накопления символа
      self.sgn_mul = np.append(self.sgn_mul, temp_I)                           # Результат перемножения
      
      # Для Q
      self.convolution_Q = np.append(self.convolution_Q, np.cumsum(temp_Q))
      self.sgn_mul_Q = np.append(self.sgn_mul_Q, temp_Q)

      # Пиковые значения 
      self.data[i] = (- self.convolution[-1] + (1j * self.convolution_Q[-1])) /\
                      self.signal.dots_per_osc

#------------------------------------------------------------------------------
# Отрисовка результата свертки:
    
  def ConvolutionPlot(self):
    
    in1 = self.support_signal[:self.unit_dots]
    in2 = self.convolution
    argument = self.signal.argument[0:int(5 * self.unit_dots)]
    
    fig,(ax2, ax3) = pyplot.subplots(2,1, figsize = (10,10))
    ax2.plot(argument[:self.unit_dots], in1)
    ax3.plot(argument, in2)

#==============================================================================
