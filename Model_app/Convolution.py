# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 22:49:48 2020

@author: Григорий
"""

from math import sqrt

###############################################################################
# Свертка:

def Convolution(in1, in2):
    
  norma = __norma(in1,in1)

  normalisation = lambda x: x/norma

  
  v0, v2 = __LRConvolution(in1, in2)
  v1 = __CConvolution(in1, in2)

  value = v0 + v1 + v2
  
  if norma != 0:
    value = list(map(normalisation, value))
  else:
    print("")
    print("Предупреждение: нулевая норма")
  
#  value = list(map(abs, value))
  
  return(value)

#------------------------------------------------------------------------------
# Расчет коэффициента нормировки:
    
def __norma(in1, in2):

  temp1 = 0
  temp2 = 0
  for j in range(0, max(len(in1), len(in2))):
    if j < len(in1):
      temp1 = temp1 + abs(in1[j])**2
    if j < len(in2):
      temp2 = temp2 + abs(in2[j])**2

  temp = sqrt(temp1*temp2)
  return(temp)

#------------------------------------------------------------------------------
# Свертка по левым и правым краям:

def __LRConvolution(in1, in2):
  
  value1 = []
  value2 = []

  for i in range(0, len(in1)):
    temp1 = 0
    temp2 = 0
    for j in range(0, i):
          temp1 = temp1 + in1[-i+j] * in2[j]
          temp2 = temp2 + in1[j] * in2[-i+j]
      
    value1.append(temp1)
    value2.append(temp2)
    
  value2.reverse()
  
  return(value1, value2)
  
#------------------------------------------------------------------------------  
# Центральная свертка:
    
def __CConvolution(in1, in2):
  
    value = []

    for i in range(0, len(in2)-len(in1) + 1):
      temp = 0
      for j in range(0, len(in1)):
        temp = temp + in1[j]*in2[i+j]    
      value.append(temp)

    return(value)

#==============================================================================     
