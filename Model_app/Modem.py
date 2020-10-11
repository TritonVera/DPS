# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:11:01 2020

@author: Григорий
"""

import random

from Model import Model
from math import pi, log2

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
    
    self.Modulation(self.number)
    print(self.mod_code)
  
  def PM(self):                      
    
    self.init()
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      unit_number = int(now/self.unit_time)
      
      phase_shift = 2*pi*self.State(self.mod_code[unit_number])/self.number
      self.signal.Point(now, phase_shift)
      
  def APM(self):                      
    
    self.init()
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      unit_number = int(now/self.unit_time)
      unit_value = self.State(self.mod_code[unit_number])
      
      phase_shift = 2*pi*unit_value/self.number
      amplitude_inc = (unit_value + 1)/self.number
      
      self.signal.Point(now, phase_shift, amplitude_inc)
      
  def FM(self):

    self.signal.clear()    
    # self.signal.value.clear()
    # self.signal.argument.clear()
    self.signal.Dots()
    
    self.Modulation(2)
    print(self.mod_code)
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      unit_number = int(now/self.unit_time)
      unit_value = self.State(self.mod_code[unit_number])
      
      deviation = (-1 + 2*unit_value)*self.signal.frequency/4
      self.signal.Point(now, 0, 1, deviation)
