# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 13:40:44 2020

@author: Р“СЂРёРіРѕСЂРёР№
"""

#from Processor_F import Processor #согласованный фильтр
from Processor import Processor

dsp = Processor()

dsp.raw_signal = [0,0,0,1,1,1,0,1,1,0,1]
dsp.support_signal = [0,0,0,1,1,1,0,1,1,0,1]

#dsp.ConvolutionPlot()
dsp.ConvolutionPlot()

#dsp.SignalCheck()