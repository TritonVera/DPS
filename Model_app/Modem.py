# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:11:01 2020

@author: Григорий
"""

import random

from Model import Model
from math import pi

class Modem(Model):
  
  def __init__(self):
    
    self.unit_time = 0                      #Длительность символа в Mod_code
    self.mod_code = []                      #Модуляционная последовательность
  
  def Modulation(self):                     #Формирование Mod_code
    
    for i in range(0,int(self.signal.time/self.unit_time)):
      self.mod_code.append(random.randint(0,1))
  
  
  def FM_2(self):                           #Двоичная фазовая манипуляция
    
    self.signal.Dots()
    self.Modulation()
    
    for i in range(0,self.signal.dots):
      
      now = i*self.signal.time/self.signal.dots
      symbol = int(now/self.unit_time)
      
      if (self.mod_code[symbol] == 0):
        self.signal.PS_Value(pi/2,now)
      elif(self.mod_code[symbol] == 1):
        self.signal.PS_Value(0,now)