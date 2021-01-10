"""
Модуль линии связи:
Работает как черный ящик с многими входными данными и с одним выходом
Вход: kwargs - словарь параметров и их значений для настройки линии связи,
а также может содержать входные данные для работы с ними
Выход: output - выходной сигнал
С внешней стороны доступно только поле output и метод change_parameters
"""

import numpy as np
import scipy.io as sio
from Signal import Garmonic
from copy import deepcopy


class CommLine:

    def __init__(self, **kwargs):

        # Init new input signal and output
        self.signal = None
        self.__input = None
        self.__output = None

        # Communication line noise parameters
        self.__type_of_line = -1
        self.__dispersion = 0
        self.__power = 0
        self.__mu = 0
        self.__param = 0

        # Load setup methods
        self.change_parameters(**kwargs)

    def change_parameters(self, **kwargs):

        # Search right keys in input parameters 
        for key in kwargs:
            # Load new input signal
            if key == 'input_signal':
                self.signal = deepcopy(kwargs[key])
                self.__input = np.array(self.signal.data[0, :])

            # Switch to choose type of communication line
            elif key == 'type_of_line':
                if kwargs[key] == 'simple' or kwargs[key] == 'gauss':
                    self.__type_of_line = 0
                elif kwargs[key] == 'line_distor':
                    self.__type_of_line = 1
                elif kwargs[key] == 'garmonic':
                    self.__type_of_line = 2
                elif kwargs[key] == 'relei':
                    self.__type_of_line = 3
                else:
                    self.__type_of_line = -1

            # Change init parameters of noise
            elif key == 'dispersion':
                self.__dispersion = kwargs[key]
            elif key == 'impact':
                self.__power = kwargs[key]
            elif key == 'mu':
                self.__mu = kwargs[key]
            elif key == 'param':
                self.__param = kwargs[key]

        # Link to work methods
        self.__choose_mode()

    # Switch to choose work method
    def __choose_mode(self):
        if self.__type_of_line == 0:
            self.__output = self.__input.copy()

        # Line distortion
        elif self.__type_of_line == 1:
            filter = sio.loadmat("./Matlab_generator/filt.mat")["Num"][0]  # Коэффиценты КИХ фильтра из Matlabа
            self.__output = np.convolve(filter, self.__input, 'same')

        # Harmonic distortion
        elif self.__type_of_line == 2:
            noise = Garmonic(in_i=self.__power,
                             in_f=self.signal.frequency,
                             in_phase=np.deg2rad(self.__param),
                             in_time=self.signal.data[1, :]).calc()
            self.__output = noise + self.__input

        # Relei's fading
        elif self.__type_of_line == 3:
            shift = int(self.__param * self.signal.dots / self.signal.dots_per_osc)
            self.__output = self.__input + (self.__power * np.roll(self.__input, shift))
        # Another way
        else:
            return

        # Add white Gauss noise
        self.__add_gauss()

        # Update signal matrix
        self.signal.data = np.vstack((self.__output, self.signal.data[1]))

    def __add_gauss(self):
        self.__output += np.random.normal(self.__mu, self.__dispersion, self.__output.size)

    # Debug methods
    def get_input(self):
        return self.__input

    def get_output(self):
        return self.__output


# ------------------------------------------------------------------------------
# Анализатор ошибок
class Compare():

    def __init__(self, in1=np.array([]), in2=np.array([])):
        self.points_0 = in1
        self.points_1 = in2
        self.errors = 0
        self.result = 0.0
        if in1.size == 0 or in2.size == 0:
            print("Неверная инициализация")
            return
        self.compare()

    def compare(self):

        self.errors = np.sum(np.logical_xor(self.points_0, self.points_1))
        if self.errors != 0:
            self.result = float(self.errors) / self.points_1.size
        else:
            self.result = 10 ** (-4)
