# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 13:40:44 2020

@author: Григорий
"""

from Processor import Processor

dsp = Processor()

dsp.raw_signal = [1,1,1,1,1]
dsp.support_signal = [0,1,1,1,0]

#dsp.ConvolutionPlot()
#dsp.ConvolutionPlot("self")

dsp.SignalCheck()