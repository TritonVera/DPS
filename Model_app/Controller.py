import numpy as np
from Line import Compare
from Processor import FindStar
from decisive import NoCogDecisiveDevice
import time
from blocks import change_modul, change_line


class Controller():
    def __init__(self, ui, modem, line, proc):
        # Параметры визулизации и настройки сигнала
        self.symbols = 5  # Число отображаемых символов
        self.osc_per_sym = 2  # Периодов на символ (определяет полосу сигнала)
        self.freq = 1  # МГц
        self.sym_number = 50  # Число генерируемых символов

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

        # Объекты выбора параметров модели
        self.choose_transmitter = ui.transmitter_panel.combobox
        self.choose_modul = ui.modul_panel.combobox
        self.choose_line = ui.line_panel.combobox
        self.choose_sync = ui.error_panel.combobox

    # ------------------------------------------------------------------------------
    # Блок отработки нажатия кнопки

    def plot_view(self):

        # Определение числа генерируемых символов
        if self.__show_block.ber.isChecked():
            # self.__show_block.label.setVisible(1)
            self.sym_number = 1000
        else:
            # self.__show_block.label.setVisible(0)
            self.sym_number = 50

        # 1. Отработка модулятора 
        t_work = time.time()
        change_modul(self.modem,        # Сам блок
                     self.osc_per_sym,  # Число периодов на символ
                     self.freq,         # Частота несущей
                     self.sym_number,   # Число генерируемых символов
                     self.choose_modul.currentText())  # Тип модуляции
        t_work = time.time() - t_work
        print("Время модулятора: ", t_work * 1000000, " мкс")

        # 2. Инициализация приёмника для когерентного приёма
        t_work = time.time()
        self.proc.Init(self.modem)
        t_work = time.time() - t_work
        print("Время приёмника: ", t_work * 1000000, " мкс")

        # 3. Отработка линии связи
        t_work = time.time()
        change_line(self.line,
                    self.modem.signal,
                    self.choose_line.currentText(),
                    self.__noise.value())
        t_work = time.time() - t_work
        print("Время линии связи: ", t_work * 1000000, " мкс")

        # 4. Визуализация осциллограммы
        t_work = time.time()
        self.show_osc(self.symbols,
                      self.modem.mod_code)
        t_work = time.time() - t_work
        print("Время отображения на графике: ", t_work * 1000000, " мкс")

        # 5. Настройка модуля рассогласования приёма (искажаем сигнал заранее)
        t_work = time.time()
        self.config_trans()
        t_work = time.time() - t_work
        print("Время рассогласователя: ", t_work * 1000000, " мкс")

        # 6. Выбор типа приема
        t_work = time.time()
        self.change_transmitter()
        t_work = time.time() - t_work
        print("Время построения корреляции: ", t_work * 1000000, " мкс")

        # 7. Построение спектра
        t_work = time.time()
        self.show_fft()
        t_work = time.time() - t_work
        print("Время БПФ: ", t_work * 1000000, " мкс")

        # 8. Декодируем символы
        t_work = time.time()
        self.decoder(self.symbols)
        t_work = time.time() - t_work
        print("Время анализатора ошибок: ", t_work * 1000000, " мкс")

    # ------------------------------------------------------------------------------
    # Блок приёмников

    def change_transmitter(self):
        # Коррелятор
        if self.choose_transmitter.currentText() == "Корреляционный приёмник":
            self.plot_corr(self.symbols)

        # Созвездие сигнала (только некогерентный приём)
        elif self.choose_transmitter.currentText() == "Созвездия сигнала":
            self.plot_star(self.osc_per_sym)

        # Согласованный фильтр
        elif self.choose_transmitter.currentText() == "Согласованный фильтр":
            pass

    # Построение корреляции
    def plot_corr(self, visual):
        self.__star_plot.setVisible(0)
        self.__conv_plot.setVisible(1)
        visual = visual * self.modem.unit_dots

        # Некогерентный приём
        if self.__show_block.kog.isChecked():
            self.proc.ReceiveV2(self.line.signal.data[0, :],
                                self.devia,
                                self.phase)
            if self.modem.number == 2:
                signal = np.array([self.line.signal.data[1, :],
                                   self.proc.sgn_mul,
                                   self.proc.convolution])
                self.__conv_plot.DrawPlots(signal, visual, 0)
            else:
                signal = np.array([self.line.signal.data[1, :],
                                   self.proc.sgn_mul,
                                   self.proc.convolution,
                                   self.proc.sgn_mul_Q,
                                   self.proc.convolution_Q])
                self.__conv_plot.DrawPlots(signal, visual, 1)
            self.stars_out = self.proc.data

        # Когерентный приём
        else:
            self.proc.Receive(self.line.signal.data[0, :])  # , self.devia, self.phase)
            signal = np.array([self.line.signal.data[1, :],
                               self.proc.sgn_mul,
                               self.proc.convolution])
            self.__conv_plot.DrawPlots(signal, visual, 0)

    # Построение созвездия
    def plot_star(self, osc_per_sym):
        self.__star_plot.setVisible(1)
        self.__conv_plot.setVisible(0)
        # Расчет созвездия для всех символов
        self.stars_out = FindStar(self.line.signal,
                                  osc_per_sym,
                                  self.devia,
                                  self.phase).stars()
        self.__star_plot.draw_plot(self.stars_out)
        self.__star_plot.add_demodul(self.choose_modul.currentText())

    # ------------------------------------------------------------------------------
    # Блок изменения визуализации окна

    def show_fft(self):
        self.__show_block.fft.setEnabled(1)
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
                                      discret_freq, self.freq * 2)

            # Показ спектра
            self.__fft_plot.setVisible(1)
        else:
            # Выключение показа спектра
            self.__fft_plot.setVisible(0)

    def show_kog(self):
        if self.choose_transmitter.currentText() == "Корреляционный приёмник":
            self.__show_block.kog.setEnabled(1)
        elif self.choose_transmitter.currentText() == "Созвездия сигнала":
            self.__show_block.kog.setChecked(1)
            self.__show_block.kog.setEnabled(0)
        elif self.choose_transmitter.currentText() == "Согласованный фильтр":
            self.__show_block.kog.setEnabled(1)

    def show_ber(self):
        if self.__show_block.kog.isChecked():
            self.__show_block.ber.setEnabled(1)
        else:
            self.__show_block.ber.setEnabled(0)
            self.__show_block.ber.setChecked(0)

    def show_param(self):
        self.__noise_block.setEnabled(1)
        if self.choose_line.currentText() == "Канал без искажений" or \
                self.choose_line.currentText() == "Линейные искажения":
            self.__noise_block.setEnabled(0)
            self.__noise_block.configure(label="", value=0)
        elif self.choose_line.currentText() == "Гауссовская помеха":
            self.__noise_block.configure(label="С/Ш (дБ)",
                                         borders=[-100, 100],
                                         value=10,
                                         step=0.1)
        elif self.choose_line.currentText() == "Релеевские замирания":
            self.__noise_block.configure(label="Интервал корреляции",
                                         borders=[0, 32],
                                         value=1,
                                         step=0.1)
        elif self.choose_line.currentText() == "Гармоническая помеха":
            self.__noise_block.configure(label="Сдвиг фаз (град)",
                                         borders=[-180, 180],
                                         value=30,
                                         step=10)

    def show_error(self):
        self.__error_block.setEnabled(1)
        if self.choose_sync.currentText() == "Когерентный приём":
            self.__error_block.setEnabled(0)
            self.__error_block.configure(label="", value=0)
        elif self.choose_sync.currentText() == "Расстройка по частоте":
            self.__error_block.configure(label="Коэф. растройки",
                                         value=0.1,
                                         borders=[-0.9, 5],
                                         step=0.01)
        elif self.choose_sync.currentText() == "Фазовая расстройка":
            self.__error_block.configure(label="Нач. фаза",
                                         value=10,
                                         borders=[-180, 180],
                                         step=10)

    # -----------------------------------------------------------------------------

    def decoder(self, visual):
        if self.__show_block.kog.isChecked():  # self.__show_block.ber.isChecked() and
            decoder = NoCogDecisiveDevice(self.stars_out,
                                          self.choose_modul.currentText())
            self.__osc_plot.draw_bit(decoder.bits[0:visual], 1)
            bit_error = Compare(np.ravel(self.modem.mod_code), np.ravel(decoder.bits))

            self.__show_block.label.setText("Pош = {:.4}".format(bit_error.result))

    def config_trans(self):
        self.devia = 0  # Расстройка частоты
        self.phase = 0  # Расстройка фазы
        if self.choose_sync.currentText() == "Расстройка по частоте":
            self.devia = self.__error_block.noise_factor_spinbox.value()
        elif self.choose_sync.currentText() == "Фазовая расстройка":
            self.phase = np.deg2rad(self.__error_block.noise_factor_spinbox.value())

    def show_osc(self, visual, bits):
        self.show_signal = self.line.signal.data[:,
                           0:int(visual * self.modem.unit_dots)]
        self.__osc_plot.draw_plot(self.show_signal)
        self.__osc_plot.draw_div(np.array(bits[0:visual]))
