"""
Модуль линии связи:
Работает как черный ящик с многими входными данными и с одним выходом
Вход: kwargs - словарь параметров и их значений для настройки линии связи,
а также может содержать входные данные для работы с ними
Выход: output - выходной сигнал
С внешней стороны доступно только поле output и метод change_parameters
"""

import random
from math import sqrt, pi
import numpy as np
from Signal import Signal, Garmonic
from copy import deepcopy

class CommLine():

    def __init__(self, **kwargs):

        # Init new input signal and output
        self.signal = Signal()
        self.__input = np.array(1)
        self.__output = np.array(1)

        # Communication line noise parameters
        self.__type_of_line = 0
        self.__dispersion = 0
        self.__mu = 0

        # Load setup methods
        self.change_parameters(**kwargs)

    def change_parameters(self, **kwargs):

        # Search right keys in input parameters 
        for key in kwargs:
            # Load new input signal
            if key == 'input_signal':
                self.signal = deepcopy(kwargs[key])
                self.__input = np.array(self.signal.data[0, :])
                # print(self.signal.data)

            # Switch to choose type of communication line
            if key == 'type_of_line':
                if kwargs[key] == 'gauss':
                    self.__type_of_line = 1
                elif kwargs[key] == 'line_distor':
                    self.__type_of_line = 2
                elif kwargs[key] == 'garmonic':
                    self.__type_of_line = 3
                elif kwargs[key] == 'relei':
                    self.__type_of_line = 4
                else:
                    self.__type_of_line = 0

            # Change init parameters of noise
            elif key == 'dispersion':
                self.__dispersion = kwargs[key]
            elif key == 'mu':
                self.__mu = kwargs[key]

        # Link to work methods
        self.__choose_mode()

    # Switch to choose work method
    def __choose_mode(self):
        if self.__type_of_line == 0:
            self.__output = self.__input.copy()
            print("Simple")

        elif self.__type_of_line == 1:
            self.__output = self.__input + np.random.default_rng().normal(self.__mu, 
                self.__dispersion, self.__input.size)
            print("Gauss")

        elif self.__type_of_line == 2:
            pass

        elif self.__type_of_line == 3:
            noise = Garmonic(in_i = self.__dispersion, in_f = 0.5, in_time = self.signal.data[1, :]).calc()
            self.__output = noise + self.__input
            print("Garmonic")

        elif self.__type_of_line == 4:
            self.__output = self.__input + np.random.default_rng().rayleigh(
                self.__dispersion, self.__input.size)
            print("Relei")
        self.signal.data = np.delete(np.vstack((self.__output, self.signal.data)), 1, axis = 0)

    # Debug methods
    def get_input(self):
        return self.__input

    def get_output(self):
        return self.__output


class FindStar():
    
    def __init__(self, input_signal):
        # Init new input signal and output
        self.__signal = input_signal
        self.__input = np.array(self.__signal.data[0, :])
        self.__time_to_block = 1/self.__signal.frequency
        self.__point_to_block = int(self.__signal.dots * self.__time_to_block/self.__signal.time)
        self.__time_to_point = self.__time_to_block/self.__point_to_block
        self.__times = np.arange(0, self.__time_to_block, self.__time_to_point)
        self.__I = Garmonic(in_i = 1, in_f = self.__signal.frequency, in_time = self.__times).calc()
        self.__Q = Garmonic(in_i = 1, in_f = self.__signal.frequency, in_phase = pi/2, in_time = self.__times).calc()

    def stars(self):
        num_of_blocks = np.int32(np.floor(self.__signal.time/self.__time_to_block))
        coords = np.zeros((2, num_of_blocks))
        dis_i = np.trapz(self.__I * self.__I, self.__times)
        dis_q = np.trapz(self.__Q * self.__Q, self.__times)

        for i in np.arange(num_of_blocks):
            dis_s = np.trapz(self.__input[(i * self.__point_to_block):((i+1) * self.__point_to_block)]**2, self.__times)
            coords[0, i] = np.trapz(self.__input[(i * self.__point_to_block):
                                                ((i+1) * self.__point_to_block)] 
                                    * self.__I, self.__times) / (np.sqrt(dis_i * dis_s))
            coords[1, i] = np.trapz(self.__input[(i * self.__point_to_block):
                                                ((i+1) * self.__point_to_block)] 
                                    * self.__Q, self.__times) / (np.sqrt(dis_q * dis_s))
        return coords
