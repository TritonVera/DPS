# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:11:01 2020

@author: Григорий
"""

# =============================================================================
# Класс модем - используется для формирования заданного типа сигнала и 
# модуляции его некоторой последовательностью. Является наследником Model.

# Сигнал как объект создан в Model и является переменной класса.

# code_type определяет тип последовательности: случайная или последовательная в
# размер созвездия.

# Для случайной требуется указать время символа unit_time.
# =============================================================================

import random
from Model import Model
from Signal import Garmonic
from math import pi, log2, ceil
import numpy as np

###############################################################################
class Modem(Model):
  
  def __init__(self):

# Параметры модулятора:
    self.sym_number = 10                   # Число анализируемых символов
    self.number = 0                         # Размерность созвездия
    self.unit_time = 0                      # Длительность символа в сигнале
    self.unit_dots = 0                      # Количество точек на символ
    self.mod_code = []                      # Модуляционная последовательность
    self.code_type = "prop"                 # Тип последовательности:
                                            # "full" в размер созвездия
                                            # "prob" случайная, количество
                                            # задается sym_number
                                            # """время сигнала/время символа"""
                                            
#------------------------------------------------------------------------------
# Формирование мод.последовательности в размер созвездия (кодировщик1):
# Выставляет время символа, так чтобы число символов соотвествовало числу
# cостояний созвездия
    
  def Code1(self):
    
    self.mod_code.clear()
    unit_number = int(log2(self.number))
    
    # (TODO) Предлагаю рассчитывать длительность всего сигнала, а не длительность 
    # одного символа
    self.signal.time = self.unit_time * self.number
    # self.unit_time = self.signal.time/self.number                            # Определение времени символа в зависимости
                                                                               # от их количества и времени всего сигнала.
    array = [i for i in range(0, self.number)]                                 # Массив символов.
    if self.code_type == "full_mix":                                           # Перемешивание массива по требованию.
      random.shuffle(array)
    
    for i in range(0, self.number):
      
      symbol = bin(array[i])[2:] 
      symbol = list(map(int,symbol))                                           # Двоичный номер состояния созвездия
                                                                               # т.е символ.
      if len(symbol) < unit_number:                                         
        for i in range(0, unit_number - len(symbol)):                          # Дополнение нулями до размера символа.
          symbol.insert(0, 0)

      self.mod_code.append(symbol)   

#------------------------------------------------------------------------------
# Формирование слуайной мод.последовательности (кодировщик2):
# Время символа задается самостоятельно, размер последовательности
# количеству поместившихся символов.
      
  def Code2(self):             
    
    self.mod_code.clear()
    number = int(log2(self.number))
    
    # Аналогично предыдущему пункту
    self.signal.time = self.unit_time * self.sym_number
    
    for i in range(0,int(self.signal.time/self.unit_time)):
      unit = []
      for j in range(0, number):
        unit.append(random.randint(0,1))
      self.mod_code.append(unit)

#------------------------------------------------------------------------------
# Вывод мод.последовательности:
 
  def CodePrint(self):
    
    print("")
    print("Кодирующая последовательность: ")
    print("")
    for i in range(0, len(self.mod_code)):
      print('{0:4}'.format(i), " ",self.mod_code[i])
     
#==============================================================================
# Отладка кодировщиков:
  
  def CodeTest(self, n = 1):
    
    self.number = 16
    self.signal.time = 10
    
    if n == 1:
      self.Code1()
    if n == 2:
      self.unit_time = self.signal.time/self.number                            # Время символа выбрано так, чтобы поместилось
      self.Code2()                                                             # self.number символов
   
    # self.CodePrint()

###############################################################################
# Инициализация модулятора:
# Инициализация сигнала и расчет мод.последовательности.
  
  def Init(self):

    # (TODO) Расчет длительности символа
    self.unit_time = 2/self.signal.frequency
    if self.code_type == "full" or self.code_type == "full_mix":
      self.Code1()
    if self.code_type == "prob":
      self.Code2()
     
    self.signal.Init()
      
    self.CodePrint()
    
    self.unit_dots = self.signal.dots_num(self.unit_time)                      # Расчет количества точек на символ         
     
#------------------------------------------------------------------------------       
# Номер состояния в десятичной системе:
      
  def State(self,In):
    
    check = "".join(map(str,In))
    return(int(check,2))

#------------------------------------------------------------------------------
# Фазоманипулированный сигнал:

  def PM(self):                      
    
    self.Init()

    for i in range(0, len(self.mod_code)):                                     # Цикл по символам.
      
      state = self.State(self.mod_code[i])                                     # Перевод символа в десятичную систему.
      phase_shift = 2*pi*state/self.number                                     # Расчет фазы.

      for j in range(0 , self.unit_dots):                                      # Цикл по точкам символа.
        now = self.signal.now(j) + i*self.unit_time                            
        self.signal.Point(now, phase_shift)
        
#------------------------------------------------------------------------------
# Амплитудофазоманипулированный сигнал:

  def APM(self):                      
    
    self.Init()
    phase_shift = 0;

    amp_inc = 0
    phs_shift = 0
    for i in range(0, len(self.mod_code)):                                     # Схема аналогична PM.
      
      state = self.State(self.mod_code[i])
      
      if state < 4:
        amp_inc = 1                                                            # Отличие: фазовый круг обнуляется 
        phs_shift = 2*pi*state/4                                               # через 4 символа, а амлитуда увеличивается
                                                                               # вдвое.
      if state >= 4 and state < 16:
        amp_inc  = 2
        if self.number == 8:
          phs_shift = 2*pi*(state - 4)/4
        if self.number == 16:
          phs_shift = 2*pi*(state - 4)/12
      
      for j in range(0 , self.unit_dots):
        now = self.signal.now(j) + i*self.unit_time
        self.signal.Point(now, phs_shift, [amp_inc, amp_inc])

#------------------------------------------------------------------------------
# Квадратурный сигнал
  def QAM(self):                      
    
    self.Init()

    self.signal.modul = '16QAM'

    for i in range(int(self.signal.time/self.unit_time)):
        # print(self.State(self.mod_code[i]))
        bin_i = np.array(self.mod_code[i][0:ceil(len(self.mod_code[i])/2)])
        bin_q = np.array(self.mod_code[i][ceil(len(self.mod_code[i])/2):len\
                        (self.mod_code[i])])

        times = np.arange(i * self.unit_time, 
                          (i+1) * self.unit_time, 
                          self.unit_time/(2 * self.signal.dots_per_osc))
        calc_block = Garmonic(
            in_i = 2 * (self.State(bin_i.tolist()) - \
                       ((2**bin_i.size) - 1.0)/2), 
            in_q = 2 * (self.State(bin_q.tolist()) - \
                       ((2**bin_q.size) - 1.0)/2), 
            in_f = self.signal.frequency, 
            in_time = times).calc_with_time()
        self.signal.data = np.hstack((self.signal.data, calc_block))

#------------------------------------------------------------------------------
# Частотномодулированный сигнал:
        
  def FM(self):
    
    self.Init()
    
    for i in range(0, len(self.mod_code)):                                     # Схема аналогична PM                         
      
      state = self.State(self.mod_code[i])
      deviation = (-1 + 2*state)*self.signal.frequency/4                       # Отличие: вместо фазы меняется частота

      for j in range(0 , self.unit_dots):                                               
        now = self.signal.now(j) + i*self.unit_time
        self.signal.Point(now, freq_dev = deviation)

#------------------------------------------------------------------------------
# Сигнал с минимальным сдвигом:
        
  def MSK(self, shift = pi/2):
    
    self.signal.phase = shift
    self.PM()
    
    self.signal.phase = 0

#==============================================================================
# Отладка модулятора: 
  
  def Test(self):
    
    self.number = 16
#    self.signal.time = 10
    self.signal.frequency = 1
    
    self.unit_time = self.signal.time/self.number                              #Время символа требуется указывать 
    self.code_type = "full"                                                    #для случайной последовательности
    
#    self.PM()
    self.APM()
#    self.FM()
#    self.MSK()
    
    self.signal.Plot()
    
#==============================================================================
