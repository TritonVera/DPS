# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:27:40 2020

@author: Григорий
"""

from Model import Model
from Signal import Signal

Model.signal.Time = 10
Model.signal.amplitude = 1
Model.signal.frequency = 10
Model.signal.phase = 0

Model.signal.Create()
Model.signal.Plot()