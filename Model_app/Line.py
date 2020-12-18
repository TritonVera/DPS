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

class CommLine():

    def __init__(self, **kwargs):

        # Init new input signal and output
        self.signal = None
        self.__input = None
        self.__output = None

        # Communication line noise parameters
        self.__type_of_line = -1
        self.__dispersion = 0
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
                if kwargs[key] == 'simple':
                    self.__type_of_line = 0
                elif kwargs[key] == 'gauss':
                    self.__type_of_line = 1
                elif kwargs[key] == 'line_distor':
                    self.__type_of_line = 2
                elif kwargs[key] == 'garmonic':
                    self.__type_of_line = 3
                elif kwargs[key] == 'relei':
                    self.__type_of_line = 4
                else:
                    self.__type_of_line = -1

            # Change init parameters of noise
            elif key == 'dispersion':
                self.__dispersion = kwargs[key]
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
            # print("Simple")

        elif self.__type_of_line == 1:
            self.__output = self.__input + np.random.normal(self.__mu, 
                self.__dispersion, self.__input.size)
            # print("Gauss")

        elif self.__type_of_line == 2:
            filt = sio.loadmat("./Matlab_generator/filt.mat")["Num"][0]        # Коэффиценты КИХ фильтра из Matlabа
            self.__output = np.convolve(filt, self.__input, 'same')

        elif self.__type_of_line == 3:
            noise = Garmonic(in_i = self.__dispersion, 
                             in_f = self.signal.frequency, 
                             in_phase = np.deg2rad(self.__param),
                             in_time = self.signal.data[1, :]).calc()
            self.__output = noise + self.__input
            # print("Garmonic")

        elif self.__type_of_line == 4:
            shift = int(self.__param * self.signal.dots/self.signal.dots_per_osc)
            self.__output = self.__input + (self.__dispersion * \
                                            np.roll(self.__input, shift))
            # print("Relei")
        else:
            return
        self.signal.data = np.vstack((self.__output, self.signal.data[1]))
        # self.signal.data = np.delete(np.vstack((self.__output, self.signal.data)), 1, axis = 0)

    # Debug methods
    def get_input(self):
        return self.__input

    def get_output(self):
        return self.__output


class FindStar():
    
    def __init__(self, input_signal, devia = 0.0, phase = 0):
        # Init new input signal and output
        self.signal = input_signal
        self.input = np.array(self.signal.data[0, :])
        self.time_to_block = 2/self.signal.frequency
        self.point_to_block = int(self.signal.dots * self.time_to_block/self.signal.time)
        self.time_to_point = self.time_to_block/self.point_to_block
        self.times = np.arange(0, self.time_to_block, self.time_to_point)
        self.ref = Garmonic(in_i = 1, in_f = (1 + devia) * self.signal.frequency, in_phase = phase, in_time = self.times).calc() + \
                (1j * Garmonic(in_q = 1, in_f = (1 + devia) * self.signal.frequency, in_phase = phase, in_time = self.times).calc())

    def stars(self):
        num_of_blocks = np.int32(np.floor(self.signal.time/self.time_to_block))
        coords = np.zeros(num_of_blocks, dtype = np.complex)

        for i in np.arange(num_of_blocks):
            s = self.input[(i * self.point_to_block):((i+1) * self.point_to_block)]
            coords[i] = np.trapz(s * self.ref.real, self.times) + \
                     (1j*np.trapz(s * self.ref.imag, self.times))
        return coords


class Compare():

    def __init__(self, in1 = np.array([]), in2 = np.array([])):
        if in1.size == 0 or in2.size == 0:
            print("Неверная инициализация")
            return 
        self.points_0 = in1
        self.points_1 = in2
        self.errors = 0
        self.result = 0.0
        self.compare()

    def compare(self):

        self.errors = np.sum(np.logical_xor(self.points_0, self.points_1))
        if self.errors == 0:
            self.result = 10**(-4)
        else:
            self.result = float(self.errors)/self.points_1.size


class DecodeStar():

    def __init__(self, points, modul = ""):
        if points.size == 0:
            return
        self.points = points
        self.bits = np.array([])
        if modul == "2-ФМ":
            self.PM2()
        elif modul == "4-ФМ":
            self.PM4()
        elif modul == "4-ФМ со сдвигом":
            self.PM4s()
        elif modul == "8-ФМ":
            self.PM8()
        elif modul == "8-АФМ":
            self.APM8()
        elif modul == "16-АФМ":
            self.APM16()
        elif modul == "16-КАМ":
            self.QAM16()
        elif modul == "ЧМ":
            self.FM()
        elif modul == "ММС":
            self.MPS()
        else:
            return
        self.bits = np.bool_(self.bits)

    def PM2(self):
        for i in range(self.points.size):
            if self.points[i].real < 0:
                self.bits = np.append(self.bits, [1])
            else:
                self.bits = np.append(self.bits, [0])

    def PM4(self):
        for i in range(self.points.size):
            if self.points[i].real + self.points[i].imag > 0:
                if self.points[i].real - self.points[i].imag > 0:
                    self.bits = np.append(self.bits, [0, 0])
                else:
                    self.bits = np.append(self.bits, [1, 1])
            else:
                if self.points[i].real - self.points[i].imag > 0:
                    self.bits = np.append(self.bits, [0, 1])
                else:
                    self.bits = np.append(self.bits, [1, 0])

    def PM4s(self):
        for i in range(self.points.size):
            if self.points[i].real > 0:
                if self.points[i].imag > 0:
                    self.bits = np.append(self.bits, [1, 1])
                else:
                    self.bits = np.append(self.bits, [0, 0])
            else:
                if self.points[i].imag > 0:
                    self.bits = np.append(self.bits, [1, 0])
                else:
                    self.bits = np.append(self.bits, [0, 1])

    def PM8(self):
        for i in range(self.points.size):
            if (0.404*self.points[i].real) + self.points[i].imag > 0:
                if self.points[i].real - (0.404*self.points[i].imag) > 0:
                    if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [1, 1, 1])
                    else:
                        self.bits = np.append(self.bits, [0, 0, 0])
                else:
                    if (0.404*self.points[i].imag) + self.points[i].real > 0:
                        self.bits = np.append(self.bits, [1, 1, 0])
                    else:
                        self.bits = np.append(self.bits, [1, 0, 1])
            else:
                if self.points[i].real - (0.404*self.points[i].imag) > 0:
                    if (0.404*self.points[i].imag) + self.points[i].real > 0:
                        self.bits = np.append(self.bits, [0, 0, 1])
                    else:
                        self.bits = np.append(self.bits, [0, 1, 0])
                else:
                    if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [1, 0, 0])
                    else:
                        self.bits = np.append(self.bits, [0, 1, 1])

    def APM8(self):
        for i in range(self.points.size):
            if np.abs(self.points[i]) < 1.5:
                if self.points[i].real + self.points[i].imag > 0:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [0, 0, 0])
                    else:
                        self.bits = np.append(self.bits, [0, 1, 1])
                else:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [0, 0, 1])
                    else:
                        self.bits = np.append(self.bits, [0, 1, 0])
            else:
                if self.points[i].real + self.points[i].imag > 0:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [1, 0, 0])
                    else:
                        self.bits = np.append(self.bits, [1, 1, 1])
                else:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [1, 0, 1])
                    else:
                        self.bits = np.append(self.bits, [1, 1, 0])

    def APM16(self):
        for i in range(self.points.size):
            if np.abs(self.points[i]) < 1.5:
                if self.points[i].real + self.points[i].imag > 0:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [0, 0, 0, 0])
                    else:
                        self.bits = np.append(self.bits, [0, 0, 1, 1])
                else:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits = np.append(self.bits, [0, 0, 0, 1])
                    else:
                        self.bits = np.append(self.bits, [0, 0, 1, 0])
            else: # TODO Доделать эту дичь
                if (0.404*self.points[i].real) + self.points[i].imag > 0:
                    if self.points[i].real - (0.404*self.points[i].imag) > 0:
                        if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                            self.bits = np.append(self.bits, [1, 1, 1, 0])
                        else:
                            self.bits = np.append(self.bits, [1, 0, 0, 0])
                    else:
                        if (0.404*self.points[i].imag) + self.points[i].real > 0:
                            self.bits = np.append(self.bits, [1, 1, 1, 1])
                        else:
                            self.bits = np.append(self.bits, [1, 1, 0, 1])
                else:
                    if self.points[i].real - (0.404*self.points[i].imag) > 0:
                        if (0.404*self.points[i].imag) + self.points[i].real > 0:
                            self.bits = np.append(self.bits, [1, 0, 0, 1])
                        else:
                            self.bits = np.append(self.bits, [1, 0, 1, 0])
                    else:
                        if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                            self.bits = np.append(self.bits, [1, 1, 0, 0])
                        else:
                            self.bits = np.append(self.bits, [1, 0, 1, 1])

    def QAM16(self):
        pass

    def FM(self):
        pass

    def MPS(self):
        pass

# class BitErrorRatio():

#     def __init__(self, input_array = np.zeros(0, dtype = np.complex)):
#         self.__points = input_array
#         self.__error = 0

#     def calc(self):
#         for point in self.__points:
#             if (point.real < 4) and (point.real > 2):
#                 self.__error = np.abs(point.real - 3)
#                 if (point.imag < 4) and (point.imag > 2):
#                     self.__error = np.abs(point.real)