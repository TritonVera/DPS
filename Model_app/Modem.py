# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:11:01 2020

@author: Григорий
"""

import random

from Model import Model
from Signal import Garmonic
from math import pi, log2, ceil, floor
import numpy as np

class Modem(Model):
  
  def __init__(self):
    
    self.number = 0
    self.unit_time = 0                      #Длительность символа в Mod_code
    self.mod_code = []                      #Модуляционная последовательность
  
  def Modulation(self, number):             #Формирование Mod_code
    
    self.mod_code.clear()
    number = int(log2(number))
    for i in range(0,int(self.signal.time/self.unit_time)):
      unit = []
      for j in range(0, number):
        unit.append(random.randint(0,1))
      self.mod_code.append(unit)
      
  def State(self,In):
    
    check = "".join(map(str,In))
    return(int(check,2))
  
  def init(self):
    
    self.signal.clear()
    # self.signal.value.clear()
    # self.signal.argument.clear()
    self.signal.Dots()
    self.signal.modul = 'None'
    
    self.Modulation(self.number)
    print(self.mod_code)
  
  def PM(self):                      
    
    self.init()
    
    if self.number == 2:
         self.signal.modul = 'BPSK'
    elif self.number == 4:
        if self.signal.phase == 0:
            self.signal.modul = 'QPSK'
        else:
            self.signal.modul = 'QPSKm'
    elif self.number == 8:
        self.signal.modul = '8PSK'

    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      unit_number = int(now/self.unit_time)
      phase_shift = 2*pi*self.State(self.mod_code[unit_number])/self.number
      self.signal.Point(now, phase_shift)
      
  def APM(self):                      
    
    self.init()

    if self.number == 8:
         self.signal.modul = '8QAM'
    elif self.number == 16:
         self.signal.modul = '16QAM'

    for i in range(int(self.signal.time/self.unit_time)):
        # print(self.State(self.mod_code[i]))
        bin_i = np.array(self.mod_code[i][0:ceil(len(self.mod_code[i])/2)])
        bin_q = np.array(self.mod_code[i][ceil(len(self.mod_code[i])/2):len(self.mod_code[i])])

        times = np.arange(i * self.unit_time, 
                          (i+1) * self.unit_time, 
                          self.unit_time/(2 * self.signal.dots_per_osc))
        calc_block = Garmonic(
            in_i = 2 * (self.State(bin_i.tolist()) - ((2**bin_i.size) - 1.0)/2), 
            in_q = 2 * (self.State(bin_q.tolist()) - ((2**bin_q.size) - 1.0)/2), 
            in_f = self.signal.frequency, 
            in_time = times).calc_with_time()
        self.signal.data = np.hstack((self.signal.data, calc_block))


    # for i in range(0,self.signal.dots):
      
    #   now = i*self.signal.time/self.signal.dots
    #   unit_number = int(now/self.unit_time)
    #   unit_value = self.State(self.mod_code[unit_number])
      
    #   phase_shift = 2*pi*unit_value/self.number
    #   amplitude_inc = (unit_value + 1)/self.number
      
    #   self.signal.Point(now, phase_shift, amplitude_inc)
      
  def FM(self):

    self.init()
    self.signal.modul = 'FM'
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      unit_number = int(now/self.unit_time)
      unit_value = self.State(self.mod_code[unit_number])
      
      deviation = (-1 + 2*unit_value)*self.signal.frequency/4
      self.signal.Point(now, 0, 1, deviation)

