# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:08:55 2020

@author: Григорий
"""
from math import pi, sin
from matplotlib import pyplot

class Signal():
  
  def __init__(self):
      
      self.time = 0
      self.dots_per_wave = 0
      
      self.phase = 0
      self.frequency = 0
      self.amplitude = 0

      self.value = []
      self.argument = []
      
  def Create(self):
    
    for t in range(0, self.Time):
      
      w = 2*pi*self.frequency
      temp_value = self.amplitude*sin(w*t)
      
      self.value.append(temp_value)
      self.argument.append(t)
      
  def Plot(self):
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (5,5))
    ax1.plot(self.argument, self.value)