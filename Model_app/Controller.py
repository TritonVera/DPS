import numpy as np
from Line import Compare
from Processor import FindStar
from decisive import NoCogDecisiveDevice
import time
from blocks import change_module, change_line


class Controller:
    def __init__(self, ui, modem, line, proc):
        # Параметры визулизации, настройки сигнала и приёмника
        self.symbols = 5  # Число отображаемых символов
        self.osc_per_sym = 2  # Периодов на символ (определяет полосу сигнала)
        self.freq = 1  # МГц
        self.sym_number = 50  # Число генерируемых символов
        self.deviate = 0  # Расстройка частоты
        self.phase = 0  # Расстройка фазы

        # Выходной параметр
        self.stars_out = []
        self.show_signal = []
        self.signal_out = []
        self.bits_out = []
        self.error = 0

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
        self.choose_module = ui.modul_panel.combobox
        self.choose_line = ui.line_panel.combobox
        self.choose_sync = ui.error_panel.combobox

    # ------------------------------------------------------------------------------
    # Блок обработки нажатия кнопки "Кривая вероятности"
    def curve_view(self):
        # Интервал проверки
        ber_range = np.linspace(-20, 20, 11)

        # Общий блок модулятора (Блоки 1 и 2)
        self.modulation()

        for n in ber_range:
            print(n)
            # 3. Отработка линии связи
            change_line(self.line,
                        self.modem.signal,
                        self.choose_line.currentText(),
                        self.__noise.value(),
                        n)

            # 4. Настройка модуля рассогласования приёма (искажаем сигнал заранее)
            self.config_trans()

            # 5. Выбор типа приема
            self.change_transmitter()

            # 6. Декодируем символы
            self.decoder()

            # 7. Печатаем результат
            print(self.error)

    # ------------------------------------------------------------------------------
    # Блок отработки нажатия кнопки "Построить"
    def plot_view(self):
        # Общий блок модулятора (Блоки 1 и 2)
        self.modulation()

        # 3. Отработка линии связи
        t_work = time.time()
        change_line(self.line,
                    self.modem.signal,
                    self.choose_line.currentText(),
                    self.__noise.value())
        t_work = time.time() - t_work
        print("Время линии связи: ", t_work * 1000000, " мкс")

        # 4. Настройка модуля рассогласования приёма (искажаем сигнал заранее)
        t_work = time.time()
        self.config_trans()
        t_work = time.time() - t_work
        print("Время рассогласователя: ", t_work * 1000000, " мкс")

        # 5. Выбор типа приема
        t_work = time.time()
        self.change_transmitter()
        t_work = time.time() - t_work
        print("Время построения корреляции: ", t_work * 1000000, " мкс")

        # 6. Декодируем символы
        t_work = time.time()
        self.decoder()
        t_work = time.time() - t_work
        print("Время анализатора ошибок: ", t_work * 1000000, " мкс")

        # 7. Построение спектра
        t_work = time.time()
        self.show_fft()
        t_work = time.time() - t_work
        print("Время БПФ: ", t_work * 1000000, " мкс")

        # 8. Визуализация в программе
        t_work = time.time()
        self.show_osc(self.symbols,
                      self.modem.mod_code)
        t_work = time.time() - t_work
        print("Время отображения на графике: ", t_work * 1000000, " мкс")

    # ------------------------------------------------------------------------------
    # Блок приёмников
    # Построение корреляции TODO
    def plot_corr(self, visual):
        visual = visual * self.modem.unit_dots

        # Некогерентный приём
        if self.__show_block.kog.isChecked():
            self.proc.ReceiveV2(self.line.signal.data[0, :],
                                self.deviate,
                                self.phase)
            if self.modem.number == 2:
                self.signal_out = np.array([self.line.signal.data[1, :],
                                   self.proc.sgn_mul,
                                   self.proc.convolution])
            else:
                self.signal_out = np.array([self.line.signal.data[1, :],
                                   self.proc.sgn_mul,
                                   self.proc.convolution,
                                   self.proc.sgn_mul_Q,
                                   self.proc.convolution_Q])
            self.stars_out = self.proc.data

        # Когерентный приём
        else:
            self.proc.Receive(self.line.signal.data[0, :])  # , self.devia, self.phase)
            self.signal_out = np.array([self.line.signal.data[1, :],
                               self.proc.sgn_mul,
                               self.proc.convolution])

    # Построение созвездия
    def plot_star(self, osc_per_sym):
        # Расчет созвездия для всех символов
        self.stars_out = FindStar(self.line.signal,
                                  osc_per_sym,
                                  self.deviate,
                                  self.phase).stars()

    # ------------------------------------------------------------------------------
    # Модулирование сигнала (Блоки обработки 1 и 2)
    def modulation(self):
        # Определение числа генерируемых символов
        if self.__show_block.ber.isChecked():
            # self.__show_block.label.setVisible(1)
            self.sym_number = 1000
        else:
            # self.__show_block.label.setVisible(0)
            self.sym_number = 50

        # 1. Отработка модулятора
        t_work = time.time()
        change_module(self.modem,  # Сам блок
                      self.osc_per_sym,  # Число периодов на символ
                      self.freq,  # Частота несущей
                      self.sym_number,  # Число генерируемых символов
                      self.choose_module.currentText())  # Тип модуляции
        t_work = time.time() - t_work
        print("Время модулятора: ", t_work * 1000000, " мкс")

        # 2. Инициализация приёмника для когерентного приёма
        t_work = time.time()
        self.proc.Init(self.modem)
        t_work = time.time() - t_work
        print("Время приёмника: ", t_work * 1000000, " мкс")

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
            """ Построение спектра (Точки во времени,
                                    Частота дискретизации,
                                    Отображаемая частота) """
            self.__fft_plot.draw_plot(self.line.signal.data[0, 0:num_points],
                                      discret_freq,
                                      self.freq * 2)
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

    def config_trans(self):
        if self.choose_sync.currentText() == "Расстройка по частоте":
            self.deviate = self.__error_block.noise_factor_spinbox.value()
        elif self.choose_sync.currentText() == "Фазовая расстройка":
            self.phase = np.deg2rad(self.__error_block.noise_factor_spinbox.value())

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

    def decoder(self):
        if self.__show_block.kog.isChecked():  # self.__show_block.ber.isChecked() and
            self.bits_out = NoCogDecisiveDevice(self.stars_out,
                                                self.choose_module.currentText()).bits
            self.error = Compare(np.ravel(self.modem.mod_code), np.ravel(self.bits_out)).result

            self.__show_block.label.setText(f"Pош = {self.error:.4}")

    def show_osc(self, visual, bits):
        self.show_signal = self.line.signal.data[:,
                           0:int(visual * self.modem.unit_dots)]
        self.__osc_plot.draw_plot(self.show_signal)
        self.__osc_plot.draw_div(np.array(bits[0:visual]))
        self.__osc_plot.draw_bit(self.bits_out[0:visual], 1)
        if self.choose_transmitter.currentText() == "Созвездия сигнала":
            self.__star_plot.setVisible(1)
            self.__star_plot.draw_plot(self.stars_out)
            self.__star_plot.add_demodul(self.choose_module.currentText())
            self.__conv_plot.setVisible(0)
        elif self.choose_transmitter.currentText() == "Корреляционный приёмник":
            self.__star_plot.setVisible(0)
            self.__conv_plot.setVisible(1)
            if self.__show_block.kog.isChecked() or self.modem.number != 2:
                self.__conv_plot.DrawPlots(self.signal_out, visual, 1)
            else:
                self.__conv_plot.DrawPlots(self.signal_out, visual, 0)


