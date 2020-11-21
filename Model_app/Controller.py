from math import pi
from Line import FindStar

class Controller():

    def __init__(self, ui, modem, line, proc):
        self.__ui = ui
        self.__modem = modem
        self.proc = proc
        self.__line = line
        self.__osc_plot = ui.plot_panel
        self.__star_plot = ui.star_panel
        self.__noise_block = ui.nf_panel
        self.__noise = self.__noise_block.noise_factor_spinbox
        self.__choose_m = ui.modul_panel.combobox
        self.__choose_l = ui.line_panel.combobox
        self.__choose_s = ui.error_panel.combobox

    def plot_view(self):
        # Работа модулятора
        self.change_modul()
        
        # Инициализация коррелятора
        self.proc.Init(self.__modem)
        
        # Работа линии связи
        self.change_line()
        
        # Настройка модуля рассогласования
        devia = 0
        phase = 0
        if self.__choose_s.currentText() == "Расстройка по частоте":
            devia = 0.1 # TODO Manage from UI
        elif self.__choose_s.currentText() == "Фазовая расстройка":
            phase = pi/6 # TODO Manage from UI
        
        # Визуализация на осциллографе
        visible_sym = 5;            # Число отображаемых символов
        show_signal = self.__line.signal.data[:, 
                                              0:int(visible_sym * self.__modem.unit_dots)]
        self.__osc_plot.draw_plot(show_signal)
        
        # Коррелятор (Работает толькол с отсчетами сигнала)
        self.proc.Receive(show_signal[0])
        
        # Расчет созвездия для всех символов
        stars_out = FindStar(self.__line.signal, devia, phase).stars()    
        self.__star_plot.draw_plot(stars_out)

    def change_modul(self):
        # Начальная настройка модулятора
        self.__modem.signal.phase = 0                                                  # Начальная фаза сигнала
        self.__modem.code_type = "prob"
        # self.__star_plot.plot.setAxisScale(QwtPlot.xBottom, -1.2, 1.2, 0.4)
        # self.__star_plot.plot.setAxisScale(QwtPlot.yLeft, -1.2, 1.2, 0.4)

        # (TODO) For debug
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
            # self.__star_plot.plot.setAxisScale(QwtPlot.xBottom, -2.5, 2.5, 0.5)
            # self.__star_plot.plot.setAxisScale(QwtPlot.yLeft, -2.5, 2.5, 0.5)
            self.__modem.number = 8
            self.__modem.APM()

        elif self.__choose_m.currentText() == "16-АФМ":
            # self.__star_plot.plot.setAxisScale(QwtPlot.xBottom, -2.5, 2.5, 0.5)
            # self.__star_plot.plot.setAxisScale(QwtPlot.yLeft, -2.5, 2.5, 0.5)
            self.__modem.number = 16
            self.__modem.APM()

        elif self.__choose_m.currentText() == "16-КАМ":
            # self.__star_plot.plot.setAxisScale(QwtPlot.xBottom, -4, 4, 1)
            # self.__star_plot.plot.setAxisScale(QwtPlot.yLeft, -4, 4, 1)
            self.__modem.number = 16
            self.__modem.QAM()

        elif self.__choose_m.currentText() == "ЧМ":
            self.__modem.number = 2
            self.__modem.FM()

        elif self.__choose_m.currentText() == "ММС":
            self.__modem.number = 2
            self.__modem.FM()

    def show_param(self):

        self.__noise_block.setVisible(1)
        if self.__choose_l.currentText() == "Канал без искажений":
            self.__noise_block.setVisible(0)
        elif self.__choose_l.currentText() == "Гауссовская помеха":
            self.__noise.setValue(10)
            self.__noise_block.noise_label.setText("С/Ш (разы)")
        elif self.__choose_l.currentText() == "Релеевские замирания":
            self.__noise.setValue(1)
            self.__noise_block.noise_label.setText("Интервал корреляции")
        elif self.__choose_l.currentText() == "Гармоническая помеха":
            self.__noise.setValue(30)
            self.__noise_block.noise_label.setText("Сдвиг фаз (град)")

    def change_line(self):
        # Вычисление дисперсии полезного сигнала
        dis_input = self.__modem.signal.dispersion()

        # Выбор типа канала связи
        if self.__choose_l.currentText() == "Канал без искажений":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'simple')

        elif self.__choose_l.currentText() == "Гауссовская помеха":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'gauss', 
                dispersion = dis_input/self.__noise.value(), 
                mu = 0)

        elif self.__choose_l.currentText() == "Релеевские замирания":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'relei', 
                dispersion = dis_input/self.__noise.value(), 
                mu = 0)

        elif self.__choose_l.currentText() == "Гармоническая помеха":
            self.__line.change_parameters(
                input_signal = self.__modem.signal,
                type_of_line = 'garmonic', 
                dispersion = self.__noise.value(), 
                mu = 0)

        elif self.__choose_l.currentText() == "Линейные искажения":
            self.__line.change_parameters(
                input_signal = self.__modem.signal, 
                type_of_line = 'line_distor', 
                dispersion = dis_input/self.__noise.value(), 
                mu = 0)
