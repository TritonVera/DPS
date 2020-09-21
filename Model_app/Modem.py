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
    
    self.unit_time = 0                      #Длительность символа в Mod_code
    self.mod_code = []                      #Модуляционная последовательность
  
  def Modulation(self, number):             #Формирование Mod_code
    
    for i in range(0,int(self.signal.time/self.unit_time)):
      unit = []
      for j in range(0, number):
        unit.append(random.randint(0,1))
      self.mod_code.append(unit)
      
  def CodeCheck(self,In):
    
    check = "".join(map(str,In))
    return(int(check,2) + 1)
  
  
  def FM(self, number):                      #Фазовая манипуляция
    
    self.signal.Dots()
    self.Modulation(int(log2(number)))
    print(self.mod_code)
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      symbol = int(now/self.unit_time)
      
      phase_shift = 2*pi*self.CodeCheck(self.mod_code[symbol])/number
      self.signal.PS_Value(phase_shift,now)
      