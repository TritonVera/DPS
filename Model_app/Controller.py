from Modem import Modem
from math import pi, sqrt
from Line import CommLine, FindStar

class Controller():

    def __init__(self, ui, modem, line):
        self.__ui = ui
        self.__modem = modem
        self.__line = line
        self.__osc_plot = ui.plot_panel
        self.__star_plot = ui.star_panel
        self.__noise_block = ui.nf_panel
        self.__noise = self.__noise_block.noise_factor_spinbox
        self.__choose_m = ui.modul_panel.combobox
        self.__choose_l = ui.line_panel.combobox

    def plot_view(self):
        # Расчет сигнала и созвездия
        self.change_modul()
        self.change_line()
        stars = FindStar(input_signal = self.__line.signal).stars()

        # Построение всех графиков
        self.__osc_plot.draw_plot(self.__line.signal.data)
        self.__star_plot.draw_plot(stars)

    def change_modul(self):
        # Начальная настройка модулятора
        self.__modem.signal.phase = 0                                                  # Начальная фаза сигнала

        # (TODO) For debug
        self.__modem.signal.frequency = self.__ui.signal_panel.freq_spinbox.value()    # Частота несущей
        self.__modem.signal.time = self.__ui.signal_panel.time_spinbox.value()         # Число отсчетов времени на котором генерируется сигнал
        self.__modem.unit_time = 2/self.__modem.signal.frequency

        # Выбор типа модуляции и его донастройка
        if self.__choose_m.currentText() == "BPSK":
            self.__modem.number = 2
            self.__modem.PM()

        elif self.__choose_m.currentText() == "QPSK":
            self.__modem.number = 4
            self.__modem.PM()

        elif self.__choose_m.currentText() == "8-PSK":
            self.__modem.number = 8
            self.__modem.PM()

        elif self.__choose_m.currentText() == "QPSK со сдвигом":
            self.__modem.signal.phase = pi/4
            self.__modem.number = 4
            self.__modem.PM()

        elif self.__choose_m.currentText() == "APM8":
            self.__modem.number = 8
            self.__modem.APM()

        elif self.__choose_m.currentText() == "APM16":
            self.__modem.number = 16
            self.__modem.APM()

        elif self.__choose_m.currentText() == "FM":
            self.__modem.number = 2
            self.__modem.FM()

    def show_param(self):

        if self.__choose_l.currentText() == "Канал без искажений":
            self.__noise_block.setVisible(0)
        else:
            self.__noise_block.setVisible(1)

    def change_line(self):
        # Выбор типа канала связи
        if self.__choose_l.currentText() == "Канал без искажений":
            self.__line.change_parameters(
                input_signal = Modem.signal, 
                type_of_line = '')

        elif self.__choose_l.currentText() == "Гауссовская помеха":
            self.__line.change_parameters(
                input_signal = Modem.signal, 
                type_of_line = 'gauss', 
                dispersion = sqrt(0.707/self.__noise.value()), 
                mu = 0)

        elif self.__choose_l.currentText() == "Релеевская помеха":
            self.__line.change_parameters(
                input_signal = Modem.signal, 
                type_of_line = 'relei', 
                dispersion = sqrt(0.707/self.__noise.value()), 
                mu = 0)

        elif self.__choose_l.currentText() == "Гармоническая помеха":
            self.__line.change_parameters(
                input_signal = Modem.signal,
                type_of_line = 'garmonic', 
                dispersion = sqrt(0.707/self.__noise.value()), 
                mu = 0)

        elif self.__choose_l.currentText() == "Линейные искажения":
            self.__line.change_parameters(
                input_signal = Modem.signal, 
                type_of_line = 'line_distor', 
                dispersion = sqrt(0.707/self.__noise.value()), 
                mu = 0)
