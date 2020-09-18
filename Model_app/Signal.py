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
      self.dots_per_osc = 0
      
      self.phase = 0
      self.frequency = 0
      self.amplitude = 0

      self.value = []
      self.argument = []
      
  def Create(self):
    
    dots = int(self.dots_per_osc * self.time * self.frequency)
    for i in range(0, dots):
      
      now = i*self.time/dots
      w = 2*pi*self.frequency
      temp_value = self.amplitude*sin(w*now)
      
      self.value.append(temp_value)
      self.argument.append(now)
      
  def Plot(self):
    
    fig,(ax1) = pyplot.subplots(1,1, figsize = (5,5))
    ax1.plot(self.argument, self.value)