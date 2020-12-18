from math import pi
import numpy as np
from Line import FindStar, DecodeStar, Compare
import time

class Controller():

    def __init__(self, ui, modem, line, proc):
        # Модели блоков вычисления (Модем -> Линия связи -> Приёмник)
        self.modem = modem
        self.proc = proc
        self.line = line

        # Упрощение доступа к визуальным объектам
        self.__osc_plot = ui.plot_panel
        self.__star_plot = ui.star_panel
        self.__conv_plot = ui.conv_panel
        self.__fft_plot = ui.fft_panel
        self.__show_block = ui.show_panel
        self.__noise_block = ui.nf_panel
        self.__error_block = ui.devia_panel
        self.__noise = self.__noise_block.noise_factor_spinbox

        # # Упрощение доступа ко внутренней функции интерфейса
        # self.__visual_function = lambda x: ui.choose_mode(x)

        # Объекты выбора параметров модели
        self.choose_transmitter = ui.transmitter_panel.combobox
        self.choose_modul = ui.modul_panel.combobox
        self.choose_line = ui.line_panel.combobox
        self.choose_sync = ui.error_panel.combobox

    def plot_view(self):
        # Отработка нажатия кнопки Построить
        # TODO Настроить вычислитель вероятности ошибки
        if self.__show_block.ber.isChecked():
            self.__show_block.label.setVisible(1)
            self.modem.sym_number = 1000
        else:
            self.__show_block.label.setVisible(0)
            self.modem.sym_number = 200

        # 1. Отработка модулятора
        t_work = time.time()
        self.change_modul()
        t_work = time.time() - t_work
        print("Время модулятора: ", t_work * 1000000, " мкс")
        
        # 2. Инициализация приёмника для когерентного приёма
        t_work = time.time()
        self.proc.Init(self.modem)
        t_work = time.time() - t_work
        print("Время приёмника: ", t_work * 1000000, " мкс")
        
        # 3. Отработка линии связи
        t_work = time.time()
        self.change_line()
        t_work = time.time() - t_work
        print("Время линии связи: ", t_work * 1000000, " мкс")
        
        # 4. Настройка модуля рассогласования приёма
        t_work = time.time()
        self.config_trans()
        t_work = time.time() - t_work
        print("Время рассогласователя: ", t_work * 1000000, " мкс")
        
        # 5. Визуализация на осциллограмме
        t_work = time.time()
        self.show_osc()
        t_work = time.time() - t_work
        print("Время отображения на графике: ", t_work * 1000000, " мкс")
        
        # 6. Выбор типа отображения
        t_work = time.time()
        self.plot_corr()
        t_work = time.time() - t_work
        print("Время построения корреляции: ", t_work * 1000000, " мкс")
        
        # 7. Построение спектра
        t_work = time.time()
        self.show_fft()
        t_work = time.time() - t_work
        print("Время БПФ: ", t_work * 1000000, " мкс")

        # Попробуем декодировать символы
        if self.__show_block.ber.isChecked():
            decoder = DecodeStar(stars_out, self.choose_modul.currentText())
            bit_error = Compare(np.ravel(self.modem.mod_code), decoder.bits)

            self.__show_block.label.setText("Вероятность ошибки: {:.4}".format(bit_error.result))
            print(bit_error.errors)
            print(bit_error.result)

    def plot_corr(self):
        # Коррелятор (Работает только с отсчетами сигнала)
        if self.choose_transmitter.currentText() == "Корреляционный приёмник":
            self.__star_plot.setVisible(0)
            self.__conv_plot.setVisible(1)

            # Некогерентный приём
            if self.__show_block.kog.isChecked():
                self.proc.ReceiveV2(self.show_signal[0], self.devia, self.phase)
                if self.modem.number == 2:
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
            
            # Когерентный приём
            else:
                self.proc.Receive(self.show_signal[0])# , self.devia, self.phase)
                signal = np.array([self.show_signal[1],
                           self.proc.sgn_mul,
                           self.proc.convolution])
                self.__conv_plot.DrawPlots(signal, 0)
                self.__conv_plot.add_demodul(self.choose_modul.currentText())

        # Созвездие сигнала (только некогерентный приём)
        elif self.choose_transmitter.currentText() == "Созвездия сигнала":
            self.__star_plot.setVisible(1)
            self.__conv_plot.setVisible(0)
            # Расчет созвездия для всех символов
            stars_out = FindStar(self.line.signal, self.devia, self.phase).stars()
            self.__star_plot.draw_plot(stars_out)
            self.__star_plot.add_demodul(self.choose_modul.currentText())

        # Согласованный фильтр
        elif self.choose_transmitter.currentText() == "Согласованный фильтр":
            pass
        
    def change_modul(self):
        # Начальная настройка модулятора
        self.modem.signal.phase = 0                                                  # Начальная фаза сигнала
        self.modem.code_type = "prob"

        # TODO For debug
        # self.modem.signal.frequency = self.ui.signal_panel.freq_spinbox.value()    # Частота несущей
        # self.modem.signal.time = self.ui.signal_panel.time_spinbox.value()         # Число отсчетов времени на котором генерируется сигнал
        # self.modem.unit_time = 2/self.modem.signal.frequency

        # Выбор типа модуляции и его донастройка
        if self.choose_modul.currentText() == "2-ФМ":
            self.modem.number = 2
            self.modem.PM()

        elif self.choose_modul.currentText() == "4-ФМ":
            self.modem.number = 4
            self.modem.PM()

        elif self.choose_modul.currentText() == "8-ФМ":
            self.modem.number = 8
            self.modem.PM()

        elif self.choose_modul.currentText() == "4-ФМ со сдвигом":
            self.modem.signal.phase = pi/4
            self.modem.number = 4
            self.modem.PM()

        elif self.choose_modul.currentText() == "8-АФМ":
            self.modem.number = 8
            self.modem.APM()

        elif self.choose_modul.currentText() == "16-АФМ":
            self.modem.number = 16
            self.modem.APM()

        elif self.choose_modul.currentText() == "16-КАМ":
            self.modem.number = 16
            self.modem.QAM()

        elif self.choose_modul.currentText() == "ЧМ":
            self.modem.number = 2
            self.modem.FM()

        elif self.choose_modul.currentText() == "ММС":
            self.modem.number = 2
            self.modem.FM()

        self.__show_block.fft.setEnabled(1)

    def show_fft(self):
        if self.__show_block.fft.isChecked():
            # Вычисление частоты дискретизации
            discret_freq = self.line.signal.frequency * \
                           self.line.signal.dots_per_osc
            # Вычисление числа точек для построения спектра (Берем не больше 100 символов)
            num_points = int(100 * self.modem.unit_dots)

            # Расчет и построение спектра
            """ Построение спектра (Точки во времени, \
                Частота дискретизации, Отображаемая частота) """
            self.__fft_plot.draw_plot(self.line.signal.data[0, 0:num_points], \
                discret_freq, 3)

            # Показ спектра
            self.__fft_plot.setVisible(1)
        else:
            # Выключение показа спектра
            self.__fft_plot.setVisible(0)

    def show_kog(self):
        if self.choose_transmitter.currentText() == "Корреляционный приёмник":
            self.__show_block.kog.setChecked(0)
            self.__show_block.kog.setEnabled(1)
        elif self.choose_transmitter.currentText() == "Созвездия сигнала":
            self.__show_block.kog.setChecked(1)
            self.__show_block.kog.setEnabled(0)
        elif self.choose_transmitter.currentText() == "Согласованный фильтр":
            self.__show_block.kog.setChecked(0)
            self.__show_block.kog.setEnabled(1)

    def show_param(self):
        self.__noise_block.setEnabled(1)
        if self.choose_line.currentText() == "Канал без искажений":
            self.__noise_block.setEnabled(0)
            self.__noise_block.configure(label = "", value = 0)
        elif self.choose_line.currentText() == "Гауссовская помеха":
            self.__noise_block.configure(label = "С/Ш (разы)", 
                                         borders = [0, 100],
                                         value = 10,
                                         step = 0.1)
        elif self.choose_line.currentText() == "Релеевские замирания":
            self.__noise_block.configure(label = "Интервал корреляции",
                                         borders = [0, 32],
                                         value = 1,
                                         step = 0.1)
        elif self.choose_line.currentText() == "Гармоническая помеха":
            self.__noise_block.configure(label = "Сдвиг фаз (град)",
                                         borders = [-180, 180],
                                         value = 30,
                                         step = 10)

    def show_error(self):
        self.__error_block.setEnabled(1)
        if self.choose_sync.currentText() == "Когерентный приём":
            self.__error_block.setEnabled(0)
            self.__error_block.configure(label = "", value = 0)
        elif self.choose_sync.currentText() == "Расстройка по частоте":
            self.__error_block.configure(label = "Коэф. растройки", 
                                         value = 0.1,
                                         borders = [-0.9, 5],
                                         step = 0.01)
        elif self.choose_sync.currentText() == "Фазовая расстройка":
            self.__error_block.configure(label = "Нач. фаза", 
                                         value = 10,
                                         borders = [-180, 180],
                                         step = 10)
            

    def change_line(self):
        # Cтандартное SNR
        self.bit_error = 1      # SNR в разах

        # Средняя амплитуда полезного сигнала на дискрету
        dis_input = 2 * self.modem.signal.dispersion()    # Мощa (Умножение на 2 - полукостыль для соответствия проге)

        # Выбор типа канала связи
        # TODO Перенастроить Гауссовскую помеху, как добавочную к исходному сигналу
        if self.choose_line.currentText() == "Канал без искажений":
            self.line.change_parameters(
                input_signal = self.modem.signal, 
                type_of_line = 'simple')

        elif self.choose_line.currentText() == "Гауссовская помеха":
            self.bit_error = self.__noise.value()
            self.line.change_parameters(
                input_signal = self.modem.signal, 
                type_of_line = 'gauss', 
                dispersion = dis_input/self.bit_error, 
                mu = 0)

        elif self.choose_line.currentText() == "Релеевские замирания":
            self.line.change_parameters(
                input_signal = self.modem.signal, 
                type_of_line = 'relei', 
                dispersion = dis_input/self.bit_error,
                param = self.__noise.value(),
                mu = 0)

        elif self.choose_line.currentText() == "Гармоническая помеха":
            self.line.change_parameters(
                input_signal = self.modem.signal,
                type_of_line = 'garmonic', 
                dispersion = dis_input/self.bit_error,
                param = self.__noise.value(),
                mu = 0)

        elif self.choose_line.currentText() == "Линейные искажения":
            self.line.change_parameters(
                input_signal = self.modem.signal, 
                type_of_line = 'line_distor', 
                dispersion = dis_input/self.bit_error, 
                mu = 0)

    def config_trans(self):
        self.devia = 0               # Расстройка частоты
        self.phase = 0               # Расстройка фазы
        if self.choose_sync.currentText() == "Расстройка по частоте":
            self.devia = self.__error_block.noise_factor_spinbox.value()
        elif self.choose_sync.currentText() == "Фазовая расстройка":
            self.phase = np.deg2rad(self.__error_block.noise_factor_spinbox.value())

    def show_osc(self):
        self.visible_sym = 10;            # Число отображаемых символов
        self.show_signal = self.line.signal.data[:, 
                                              0:int(self.visible_sym * self.modem.unit_dots)]
        self.__osc_plot.draw_plot(self.show_signal)
