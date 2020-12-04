from math import pi
import numpy as np
from Line import FindStar, DecodeStar, Compare

class Controller():

    def __init__(self, ui, modem, line, proc):
        self.__ui = ui
        self.__modem = modem
        self.proc = proc
        self.__line = line
        self.__osc_plot = ui.plot_panel
        self.__star_plot = ui.star_panel
        self.__conv_plot = ui.conv_panel
        self.__noise_block = ui.nf_panel
        self.__error_block = ui.devia_panel
        self.__noise = self.__noise_block.noise_factor_spinbox
        self.__choose_m = ui.modul_panel.combobox
        self.__choose_l = ui.line_panel.combobox
        self.__choose_s = ui.error_panel.combobox
        self.__choose_t = ui.transmitter_panel.combobox

    def plot_view(self):
        if self.__ui.show_panel.ber.isChecked():
            self.__ui.show_panel.label.setVisible(1)
            self.__modem.sym_number = 1000
        else:
            self.__ui.show_panel.label.setVisible(0)
            self.__modem.sym_number = 50

        # Работа модулятора
        self.change_modul()
        
        # Инициализация коррелятора
        self.proc.Init(self.__modem)
        
        # Работа линии связи
        self.bit_error = 1
        self.change_line()
        
        # Настройка модуля рассогласования
        devia = 0
        phase = 0
        if self.__choose_s.currentText() == "Расстройка по частоте":
            devia = self.__error_block.noise_factor_spinbox.value()
        elif self.__choose_s.currentText() == "Фазовая расстройка":
            phase = np.deg2rad(self.__error_block.noise_factor_spinbox.value())
        
        # Визуализация на осциллографе
        self.visible_sym = 5;            # Число отображаемых символов
        self.show_signal = self.__line.signal.data[:, 
                                              0:int(self.visible_sym * self.__modem.unit_dots)]
        self.__osc_plot.draw_plot(self.show_signal)
        
        if self.__choose_t.currentText() == "Корреляционный приёмник":
            self.plot_corr(devia, phase)
        
        elif self.__choose_t.currentText() == "Созвездия сигнала":
            # Расчет созвездия для всех символов
            stars_out = FindStar(self.__line.signal, devia, phase).stars()
            self.__ui.choose_mode("Созв")
            self.__star_plot.draw_plot(stars_out)
            self.__star_plot.add_demodul(self.__choose_m.currentText())
        
        # Построение графика БПФ. Второй аргумент это частота дискретищзации, необходимая для точной синхронизации
        if self.__ui.show_panel.fft.isChecked():
            self.__ui.fft_panel.setVisible(1)
        else:
            self.__ui.fft_panel.setVisible(0)
        discret_freq = self.__line.signal.frequency * self.__line.signal.dots_per_osc
        self.__ui.fft_panel.draw_plot(self.__line.signal.data[0, 0:int(100 * self.__modem.unit_dots)], discret_freq)
        # Попробуем декодировать символы
        # if self.__ui.show_panel.ber.isChecked():
        #     decoder = DecodeStar(stars_out, self.__choose_m.currentText())
        #     bit_error = Compare(np.ravel(self.__modem.mod_code), decoder.bits)

        #     self.__ui.show_panel.label.setText("Вероятность ошибки: {:.4}".format(bit_error.result))
        #     print(bit_error.errors)
        #     print(bit_error.result)

    def plot_corr(self, dev, ph):
        
        # Коррелятор (Работает только с отсчетами сигнала)
        self.__ui.choose_mode("Корр")
        self.proc.ReceiveV2(self.show_signal[0], dev, ph)
        
        if self.__modem.number == 2:
            signal = np.array([self.show_signal[1],
                           self.proc.sgn_mul,
                           self.proc.convolution])
            self.__conv_plot.DrawPlots(signal, 0)
        else:
            signal = np.array([self.show_signal[1],
                           self.proc.sgn_mul, 
                           self.proc.convolution,
                           self.proc.sgn_mul_Q,
                           self.proc.convolution_Q])
            self.__conv_plot.DrawPlots(signal, 1)
        
    def change_modul(self):
        # Начальная настройка модулятора
        self.__modem.signal.phase = 0                                                  # Начальная фаза сигнала
        self.__modem.code_type = "prob"

        # TODO For debug
        # self.__modem.signal.frequency = self.__ui.signal_panel.freq_spinbox.value()    # Частота несущей
        # self.__modem.signal.time = self.__ui.signal_panel.time_spinbox.value()         # Число отсчетов времени на котором генерируется сигнал
        # self.__modem.unit_time = 2/self.__modem.signal.frequency

        # Выбор типа модуляции и его донастройка
        if self.__choose_m.currentText() == "2-ФМ":
            self.__modem.number = 2
            self.__modem.PM()

        elif self.__choose_m.currentText() == "4-ФМ":
            self.__modem.number = 4
            self.__modem.PM()

        elif self.__choose_m.currentText() == "8-ФМ":
            self.__modem.number = 8
            self.__modem.PM()

        elif self.__choose_m.currentText() == "4-ФМ со сдвигом":
            self.__modem.signal.phase = pi/4
            self.__modem.number = 4
            self.__modem.PM()

        elif self.__choose_m.currentText() == "8-АФМ":
            self.__modem.number = 8
            self.__modem.APM()

        elif self.__choose_m.currentText() == "16-АФМ":
            self.__modem.number = 16
            self.__modem.APM()

        elif self.__choose_m.currentText() == "16-КАМ":
            self.__modem.number = 16
            self.__modem.QAM()

        elif self.__choose_m.currentText() == "ЧМ":
            self.__modem.number = 2
            self.__modem.FM()

        elif self.__choose_m.currentText() == "ММС":
            self.__modem.number = 2
            self.__modem.FM()

    def show_fft(self):
        if self.__ui.show_panel.fft.isChecked():
            self.__ui.fft_panel.setVisible(1)
        else:
            self.__ui.fft_panel.setVisible(0)

    def show_param(self):
        self.__noise_block.setEnabled(1)
        if self.__choose_l.currentText() == "Канал без искажений":
            self.__noise_block.setEnabled(0)
            self.__noise_block.configure(label = "", value = 0)
        elif self.__choose_l.currentText() == "Гауссовская помеха":
            self.__noise_block.configure(label = "С/Ш (разы)", 
                                         borders = [0, 100],
                                         value = 10,
                                         step = 0.1)
        elif self.__choose_l.currentText() == "Релеевские замирания":
            self.__noise_block.configure(label = "Интервал корреляции",
                                         borders = [0, 32],
                                         value = 1,
                                         step = 0.1)
        elif self.__choose_l.currentText() == "Гармоническая помеха":
            self.__noise_block.configure(label = "Сдвиг фаз (град)",
                                         borders = [-180, 180],
                                         value = 30,
                                         step = 10)

    def show_error(self):
        self.__error_block.setEnabled(1)
        if self.__choose_s.currentText() == "Когерентный приём":
            self.__error_block.setEnabled(0)
            self.__error_block.configure(label = "", value = 0)
        elif self.__choose_s.currentText() == "Расстройка по частоте":
            self.__error_block.configure(label = "Коэф. растройки", 
                                         value = 0.1,
                                         borders = [-0.9, 5],
                                         step = 0.01)
        elif self.__choose_s.currentText() == "Фазовая расстройка":
            self.__error_block.configure(label = "Нач. фаза", 
                                         value = 10,
                                         borders = [-180, 180],
                                         step = 10)
            

    def change_line(self):
        # Вычисление дисперсии полезного сигнала
        dis_input = 2 * self.__modem.signal.dispersion()    # Мощa (Умножение на 2 - полукостыль для соответствия проге)
        # dis_input = np.sqrt(self.__modem.signal.dispersion())   # Напруга

        # Выбор типа канала связи
        if self.__choose_l.currentText() == "Канал без искажений":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'simple')

        elif self.__choose_l.currentText() == "Гауссовская помеха":
            self.bit_error = self.__noise.value()
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'gauss', 
                dispersion = dis_input/self.bit_error, 
                mu = 0)

        elif self.__choose_l.currentText() == "Релеевские замирания":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'relei', 
                dispersion = dis_input/self.bit_error,
                param = self.__noise.value(),
                mu = 0)

        elif self.__choose_l.currentText() == "Гармоническая помеха":
            self.__line.change_parameters(
                input_signal = self.__modem.signal,
                type_of_line = 'garmonic', 
                dispersion = dis_input/self.bit_error,
                param = self.__noise.value(),
                mu = 0)

        elif self.__choose_l.currentText() == "Линейные искажения":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'line_distor', 
                dispersion = dis_input/self.bit_error, 
                mu = 0)
