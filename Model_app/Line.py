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

class CommLine():

    def __init__(self, **kwargs):

        # Init new input signal and output
        self.__signal = Signal()
        self.input = np.array(0)
        self.output = np.array(0)

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
                self.__signal = kwargs[key]
                self.input = np.array(self.__signal.value)

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
            print("Simple")
            self.output = self.input.copy()

        elif self.__type_of_line == 1:
            print("Gauss")
            self.output = self.input + np.random.default_rng().normal(self.__mu, 
                self.__dispersion, self.input.size)

        elif self.__type_of_line == 2:
            self.__line_distor()

        elif self.__type_of_line == 3:
            print("Garmonic")
            noise = Garmonic(in_i = self.__dispersion, in_w0 = 0.5, in_time = self.__signal.argument).calc()
            self.output = noise + self.input

        elif self.__type_of_line == 4:
            print("Relei")
            self.output = self.input + np.random.default_rng().rayleigh(
                self.__dispersion, self.input.size)

    # Work methods
    def __line_distor(self):
        pass

    # Debug methods
    def print_input(self):
        print(self.__input)

    def print_output(self):
        print(self.output)


class FindStar():
    
    def __init__(self, input_signal):

        # Init new input signal and output
        self.__signal = input_signal
        self.__input = np.array(self.__signal.value)
        self.__time_to_block = 1/self.__signal.frequency
        self.__point_to_block = int(self.__signal.dots * self.__time_to_block/self.__signal.time)
        self.__time_to_point = self.__signal.time/self.__signal.dots
        self.__times = np.arange(0, self.__time_to_block, self.__time_to_point)
        self.__i = Garmonic(in_i = 1, in_w0 = self.__signal.frequency, in_time = self.__times).calc()
        self.__q = Garmonic(in_i = 1, in_w0 = self.__signal.frequency, in_phase = pi/2, in_time = self.__times).calc()

    def stars(self):
        num_of_blocks = np.int32(np.floor(self.__signal.time/self.__time_to_block))
        coords = np.zeros((2, num_of_blocks))
        for i in np.arange(num_of_blocks):
            coords[0, i] = np.trapz(self.__input[(i * self.__point_to_block):((i+1) * self.__point_to_block)] * self.__i, self.__times)
            coords[1, i] = np.trapz(self.__input[(i * self.__point_to_block):((i+1) * self.__point_to_block)] * self.__q, self.__times)
        return coords
