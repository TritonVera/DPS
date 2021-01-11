import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve, QwtPlotGrid, QwtPlotMarker


# Класс графического полотна
class PlotPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumHeight(self, 200)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.eng = ScaleEngine(self.plot, coef=0.4);
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)

    def draw_plot(self, points=np.zeros((2, 1))):

        self.plot.detachItems()
        y_list = points[0, :]
        x_list = points[1, :]

        y_color = QColor(0, 128, 128)
        y_pen = QPen(y_color)
        y_pen.setWidth(2)

        self.signal.setData(x_list, y_list)
        self.signal.setPen(y_pen)
        self.signal.attach(self.plot)

        self.eng.engine(y=y_list);

        self.end = x_list[-1]

        self.plot.replot()
        self.plot.show()

    def draw_div(self, sym):
        # Массивы отображаемых разделителей и символов
        self.markers = []
        self.symbols_up = []
        self.symbols_down = []

        # Верхняя надпись
        up_label = QwtPlotMarker()
        up_label.setValue(self.end / 2, self.eng.max_value_y * (14 / 15))
        up_label.setLabel("Переданные символы")
        up_label.attach(self.plot)

        # Нижняя надпись
        down_label = QwtPlotMarker()
        down_label.setValue(self.end / 2, self.eng.min_value_y * (14 / 15))
        down_label.setLabel("Принятые символы")
        down_label.attach(self.plot)

        l_color = QColor(16, 16, 16)
        l_pen = QPen(l_color)
        l_pen.setWidth(1)
        l_pen.setStyle(Qt.DashLine)
        self.step = self.end / len(sym[:])
        for i in np.arange(len(sym[:]), dtype=np.int):
            marker = QwtPlotMarker()
            self.markers.append(marker)

            self.markers[i].setValue((1 + i) * self.step, 0.0)
            self.markers[i].setLineStyle(QwtPlotMarker.VLine)
            self.markers[i].setLinePen(l_pen)
            self.markers[i].attach(self.plot)

        self.draw_bit(sym, 0)

    def draw_bit(self, sym, mode):
        for i in np.arange(len(sym[:]), dtype=np.int):
            x_pos = ((1 + i) * self.step) - (self.step / 2)
            if mode:
                y_pos = self.eng.min_value_y * (4 / 5)
                symbol = QwtPlotMarker()
                self.symbols_down.append(symbol)
                self.symbols_down[i].setValue(x_pos, y_pos)
                self.symbols_down[i].setLabel(" ".join(str(sym[i])))
                print(" ".join(str(sym[i])))
                self.symbols_down[i].attach(self.plot)
            else:
                y_pos = self.eng.max_value_y * (4 / 5)
                symbol = QwtPlotMarker()
                self.symbols_up.append(symbol)
                self.symbols_up[i].setValue(x_pos, y_pos)
                self.symbols_up[i].setLabel(" ".join(str(sym[i])))
                print(" ".join(str(sym[i])))
                self.symbols_up[i].attach(self.plot)

        self.plot.replot()
        self.plot.show()


class FftPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumHeight(self, 200)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.plot.enableAxis(QwtPlot.yLeft, 0)

        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)

    def draw_plot(self, graph=np.zeros((1, 0)), freq=1, freq_show=None):
        # Проверка на наличие входных параметров
        if graph.size == 0:
            return
        if freq_show == None:
            freq_show = freq

        # Расчет БПФ
        y_list = self.__calc(graph)

        # Установка границ отображения и шага дискретизации спектра
        border = freq / 2
        step = freq / np.size(y_list)

        # Проверка на ограничение, заданное на входной параметр
        if freq_show > border:
            freq_show = border

        # Удаление лишних точек
        mid_point = int(border / step)
        show_point = int(freq_show / step)
        y_list = y_list[int(np.floor(mid_point)):int(np.ceil(mid_point + show_point))]
        x_list = np.linspace(0, freq_show, y_list.size)

        # Самописный движок масштаба
        ScaleEngine(self.plot, y=y_list)

        # Цвет и ширина линии
        y_pen = self.signal.pen()
        y_pen.setWidth(1)
        if x_list != []:
            self.signal.setData(x_list, y_list)
            self.signal.attach(self.plot)

        self.plot.replot()
        self.plot.show()

    def __calc(self, t):
        if t.size != 0:
            y = np.fft.fft(t)
            fft = np.sqrt(y.real ** 2 + y.imag ** 2)
            fft = np.roll(fft, int(fft.size / 2))
            return fft
        else:
            return t


class StarPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 300, 300)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.grid = QwtPlotGrid()

        self.grid.attach(self.plot)
        grid_color = QColor(196, 196, 196)
        grid_pen = QPen(grid_color)
        grid_pen.setWidth(0.5)
        self.grid.setPen(grid_pen)

        self.signal.setStyle(QwtPlotCurve.Dots)
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)

    def draw_plot(self, graph=[]):
        self.plot.detachItems()
        self.grid.attach(self.plot)
        if graph == []:
            return

        x_list = graph.real
        y_list = graph.imag

        self.scaled_value = max(max(np.abs(x_list)), max(np.abs(y_list)))

        # Самописный движок масштаба
        self.engine = ScaleEngine(self.plot, [-self.scaled_value, self.scaled_value],
                                  [-self.scaled_value, self.scaled_value], borders=[[-1.2, 1.2], [-1.2, 1.2]])

        # Цвет и ширина линии
        y_pen = self.signal.pen()
        y_pen.setWidth(5)

        self.signal.setData(x_list, y_list)
        self.signal.attach(self.plot)

        self.plot.replot()
        self.plot.show()

    def add_demodul(self, mod=""):
        marker = []
        l_color = QColor(64, 16, 64)
        l_pen = QPen(l_color)
        l_pen.setWidth(1)
        l_pen.setStyle(Qt.DashLine)
        if mod == "2-ФМ":
            marker_1 = QwtPlotCurve()

            marker_1.setData([0.0, 0.0],
                             [self.engine.max_value_y, self.engine.min_value_y])
            marker_1.setPen(l_pen)
            marker_1.attach(self.plot)
        elif mod == "4-ФМ":
            scale = self.engine.max_value_y
            marker_1 = QwtPlotCurve()
            marker_2 = QwtPlotCurve()

            marker_1.setData([-scale, scale],
                             [-scale, scale])
            marker_1.setPen(l_pen)
            marker_1.attach(self.plot)

            marker_2.setData([-scale, scale],
                             [scale, -scale])
            marker_2.setPen(l_pen)
            marker_2.attach(self.plot)
        elif mod == "4-ФМ со сдвигом":
            scale = self.engine.max_value_y
            marker_1 = QwtPlotCurve()
            marker_2 = QwtPlotCurve()

            marker_1.setData([-scale, scale],
                             [0, 0])
            marker_1.setPen(l_pen)
            marker_1.attach(self.plot)

            marker_2.setData([0, 0],
                             [scale, -scale])
            marker_2.setPen(l_pen)
            marker_2.attach(self.plot)
        elif mod == "8-ФМ":
            scale = self.engine.max_value_y
            scale_2 = scale / np.tan(22.5 * np.pi / 180)  # 22,5 градусов
            marker_1 = QwtPlotCurve()
            marker_2 = QwtPlotCurve()
            marker_3 = QwtPlotCurve()
            marker_4 = QwtPlotCurve()

            marker_1.setData([-scale_2, scale_2],
                             [-scale, scale])
            marker_1.setPen(l_pen)
            marker_1.attach(self.plot)

            marker_2.setData([-scale, scale],
                             [-scale_2, scale_2])
            marker_2.setPen(l_pen)
            marker_2.attach(self.plot)

            marker_3.setData([scale, -scale],
                             [-scale_2, scale_2])
            marker_3.setPen(l_pen)
            marker_3.attach(self.plot)

            marker_4.setData([scale_2, -scale_2],
                             [-scale, scale])
            marker_4.setPen(l_pen)
            marker_4.attach(self.plot)

        elif mod == "8-АФМ":
            scale = self.engine.max_value_y
            for i in range(6):
                marker.append(QwtPlotCurve())

            marker[0].setData([-scale, scale],
                              [-scale, scale])
            marker[1].setData([-scale, scale],
                              [scale, -scale])

            # Создание массива кружочка
            x = np.linspace(-1.5, 1.5, 100)
            y = np.sqrt((1.5 ** 2) - (x ** 2))
            x = np.append(x, np.flip(x))
            y = np.append(y, -y)
            marker[2].setData(x, y)

            for i in range(6):
                marker[i].setPen(l_pen)
                marker[i].attach(self.plot)

        elif mod == "16-КАМ":
            scale = self.engine.max_value_y
            for i in range(6):
                marker.append(QwtPlotCurve())

            marker[0].setData([scale, -scale],
                              [0, 0])
            marker[1].setData([0, 0],
                              [scale, -scale])
            marker[2].setData([2, 2],
                              [scale, -scale])
            marker[3].setData([-2, -2],
                              [scale, -scale])
            marker[4].setData([scale, -scale],
                              [2, 2])
            marker[5].setData([scale, -scale],
                              [-2, -2])

            for i in range(6):
                marker[i].setPen(l_pen)
                marker[i].attach(self.plot)

        elif mod == "ЧМ" or mod == "Ортогональный ЧМ":
            scale = self.engine.max_value_y
            marker = QwtPlotCurve()

            marker.setData([-scale, scale],
                           [-scale, scale])
            marker.setPen(l_pen)
            marker.attach(self.plot)

            pos = [0, scale * (3.5 / 5)]
            first_symbol = QwtPlotMarker()
            first_symbol.setValue(pos[0], pos[1])
            first_symbol.setLabel("1")
            first_symbol.attach(self.plot)

            pos = [scale * (3.5 / 5), 0]
            second_symbol = QwtPlotMarker()
            second_symbol.setValue(pos[0], pos[1])
            second_symbol.setLabel("0")
            second_symbol.attach(self.plot)


class ConvPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 300, 300)
        vertical_layout = QVBoxLayout()

        # Произведение сигналов
        self.plot_sqrt = QwtPlot(self)
        self.plot_sqrt.enableAxis(QwtPlot.yLeft, 0)

        self.sgn_sqrt_1 = QwtPlotCurve()
        self.sgn_sqrt_2 = QwtPlotCurve()
        self.sgn_sqrt_3 = QwtPlotCurve()
        self.sgn_sqrt_4 = QwtPlotCurve()

        # Свертка сигналов
        self.plot_conv = QwtPlot(self)
        self.plot_conv.enableAxis(QwtPlot.yLeft, 0)

        self.sgn_conv_1 = QwtPlotCurve()
        self.sgn_conv_2 = QwtPlotCurve()
        self.sgn_conv_3 = QwtPlotCurve()
        self.sgn_conv_4 = QwtPlotCurve()

        # Начальные оси
        self.line_sqrt_1 = QwtPlotCurve()
        self.line_sqrt_2 = QwtPlotCurve()
        self.line_sqrt_3 = QwtPlotCurve()
        self.line_sqrt_4 = QwtPlotCurve()

        self.line_conv_1 = QwtPlotCurve()
        self.line_conv_2 = QwtPlotCurve()
        self.line_conv_3 = QwtPlotCurve()
        self.line_conv_4 = QwtPlotCurve()

        self.DrawPlots()

        vertical_layout.addWidget(self.plot_sqrt)
        vertical_layout.addWidget(self.plot_conv)

        self.setLayout(vertical_layout)

    def DrawPlots(self, points=[], num_of_points=0, mode=0):
        if not points:
            return

        self.line_pen = QPen(QColor(0, 0, 0))
        self.line_pen.setWidth(1)

        self.graph_pen = QPen(QColor(128, 0, 0))
        self.graph_pen.setWidth(2)

        self.graph_clear()

        if mode == 1:
            self.two_graph(points[:, 0:num_of_points])
        elif mode == 2:
            self.three_graph(points[:, 0:num_of_points])
        elif mode == 3:
            self.four_graph(points[:, 0:num_of_points])
        else:
            self.one_graph(points[:, 0:num_of_points])

        self.plot_sqrt.replot()
        self.plot_conv.replot()

        self.plot_sqrt.show()
        self.plot_conv.show()

    def graph_clear(self):
        self.line_sqrt_1.detach()
        self.line_conv_1.detach()
        self.sgn_conv_1.detach()
        self.sgn_sqrt_1.detach()
        self.line_sqrt_2.detach()
        self.line_conv_2.detach()
        self.sgn_conv_2.detach()
        self.sgn_sqrt_2.detach()
        self.line_sqrt_3.detach()
        self.line_conv_3.detach()
        self.sgn_conv_3.detach()
        self.sgn_sqrt_3.detach()
        self.line_sqrt_4.detach()
        self.line_conv_4.detach()
        self.sgn_conv_4.detach()
        self.sgn_sqrt_4.detach()

    def one_graph(self, points):
        time = points[0]
        sqrt_1 = points[1]
        conv_1 = points[2]

        # Движок масштаба
        ScaleEngine(self.plot_sqrt, y=sqrt_1)
        ScaleEngine(self.plot_conv, y=conv_1)

        self.line_sqrt_1.setData([0, time[-1]], [0, 0])
        self.line_sqrt_1.setPen(self.line_pen)
        self.line_sqrt_1.attach(self.plot_sqrt)
        self.sgn_sqrt_1.setData(time, sqrt_1)
        self.sgn_sqrt_1.setPen(self.graph_pen)
        self.sgn_sqrt_1.attach(self.plot_sqrt)

        self.line_conv_1.setData([0, time[-1]], [0, 0])
        self.line_conv_1.setPen(self.line_pen)
        self.line_conv_1.attach(self.plot_conv)
        self.sgn_conv_1.setData(time, conv_1)
        self.sgn_conv_1.setPen(self.graph_pen)
        self.sgn_conv_1.attach(self.plot_conv)

    def two_graph(self, points):
        time = points[0]
        # sqrt_1 = points[1]
        # conv_1 = points[2]
        # sqrt_2 = points[3]
        # conv_2 = points[4]

        sqrt_1_offset = np.max(np.abs(points[1])) + 1
        conv_1_offset = np.max(np.abs(points[2])) + 1
        sqrt_1 = points[1] + (sqrt_1_offset * np.ones(points[1].size))
        conv_1 = points[2] + (conv_1_offset * np.ones(points[2].size))

        sqrt_2_offset = -np.max(np.abs(points[3])) - 1
        conv_2_offset = -np.max(np.abs(points[4])) - 1
        sqrt_2 = points[3] + (sqrt_2_offset * np.ones(points[3].size))
        conv_2 = points[4] + (conv_2_offset * np.ones(points[4].size))

        # Движок масштаба
        ScaleEngine(self.plot_sqrt, y=[np.max(sqrt_1), np.min(sqrt_2)])
        ScaleEngine(self.plot_conv, y=[np.max(conv_1), np.min(conv_2)])

        self.line_sqrt_1.setData([0, time[-1]], [sqrt_1_offset, sqrt_1_offset])
        self.line_sqrt_1.setPen(self.line_pen)
        self.line_sqrt_1.attach(self.plot_sqrt)
        self.sgn_sqrt_1.setData(time, sqrt_1)
        self.sgn_sqrt_1.setPen(self.graph_pen)
        self.sgn_sqrt_1.attach(self.plot_sqrt)

        self.line_conv_1.setData([0, time[-1]], [conv_1_offset, conv_1_offset])
        self.line_conv_1.setPen(self.line_pen)
        self.line_conv_1.attach(self.plot_conv)
        self.sgn_conv_1.setData(time, conv_1)
        self.sgn_conv_1.setPen(self.graph_pen)
        self.sgn_conv_1.attach(self.plot_conv)

        self.line_sqrt_2.setData([0, time[-1]], [sqrt_2_offset, sqrt_2_offset])
        self.line_sqrt_2.setPen(self.line_pen)
        self.line_sqrt_2.attach(self.plot_sqrt)
        self.sgn_sqrt_2.setData(time, sqrt_2)
        self.sgn_sqrt_2.setPen(self.graph_pen)
        self.sgn_sqrt_2.attach(self.plot_sqrt)

        self.line_conv_2.setData([0, time[-1]], [conv_2_offset, conv_2_offset])
        self.line_conv_2.setPen(self.line_pen)
        self.line_conv_2.attach(self.plot_conv)
        self.sgn_conv_2.setData(time, conv_2)
        self.sgn_conv_2.setPen(self.graph_pen)
        self.sgn_conv_2.attach(self.plot_conv)

    def three_graph(self, points):
        time = points[0]
        sqrt_1 = points[1]
        conv_1 = points[2]
        sqrt_2 = points[3]
        conv_2 = points[4]
        sqrt_3 = points[5]
        conv_3 = points[6]

        sqrt_1_offset = - np.min(points[1]) + 1 + np.max(points[3])
        conv_1_offset = - np.min(points[2]) + 1 + np.max(points[4])
        sqrt_1 = points[1] + (sqrt_1_offset * np.ones(points[1].size))
        conv_1 = points[2] + (conv_1_offset * np.ones(points[2].size))

        sqrt_2_offset = 0
        conv_2_offset = 0
        sqrt_2 = points[3] + (sqrt_2_offset * np.ones(points[3].size))
        conv_2 = points[4] + (conv_2_offset * np.ones(points[4].size))

        sqrt_3_offset = - np.max(points[5]) - 1 - np.min(points[3])
        conv_3_offset = - np.max(points[6]) - 1 - np.min(points[4])
        sqrt_3 = points[5] + (sqrt_1_offset * np.ones(points[5].size))
        conv_3 = points[6] + (conv_1_offset * np.ones(points[6].size))

        # Движок масштаба
        ScaleEngine(self.plot_sqrt, y=[np.max(sqrt_1), np.min(sqrt_3)])
        ScaleEngine(self.plot_conv, y=[np.max(conv_1), np.min(conv_3)])

        self.line_sqrt_1.setData([0, time[-1]], [sqrt_1_offset, sqrt_1_offset])
        self.line_sqrt_1.setPen(self.line_pen)
        self.line_sqrt_1.attach(self.plot_sqrt)
        self.sgn_sqrt_1.setData(time, sqrt_1)
        self.sgn_sqrt_1.setPen(self.graph_pen)
        self.sgn_sqrt_1.attach(self.plot_sqrt)

        self.line_conv_1.setData([0, time[-1]], [conv_1_offset, conv_1_offset])
        self.line_conv_1.setPen(self.line_pen)
        self.line_conv_1.attach(self.plot_conv)
        self.sgn_conv_1.setData(time, conv_1)
        self.sgn_conv_1.setPen(self.graph_pen)
        self.sgn_conv_1.attach(self.plot_conv)

        self.line_sqrt_2.setData([0, time[-1]], [sqrt_2_offset, sqrt_2_offset])
        self.line_sqrt_2.setPen(self.line_pen)
        self.line_sqrt_2.attach(self.plot_sqrt)
        self.sgn_sqrt_2.setData(time, sqrt_2)
        self.sgn_sqrt_2.setPen(self.graph_pen)
        self.sgn_sqrt_2.attach(self.plot_sqrt)

        self.line_conv_2.setData([0, time[-1]], [conv_2_offset, conv_2_offset])
        self.line_conv_2.setPen(self.line_pen)
        self.line_conv_2.attach(self.plot_conv)
        self.sgn_conv_2.setData(time, conv_2)
        self.sgn_conv_2.setPen(self.graph_pen)
        self.sgn_conv_2.attach(self.plot_conv)

        self.line_sqrt_3.setData([0, time[-1]], [sqrt_3_offset, sqrt_3_offset])
        self.line_sqrt_3.setPen(self.line_pen)
        self.line_sqrt_3.attach(self.plot_sqrt)
        self.sgn_sqrt_3.setData(time, sqrt_3)
        self.sgn_sqrt_3.setPen(self.graph_pen)
        self.sgn_sqrt_3.attach(self.plot_sqrt)

        self.line_conv_3.setData([0, time[-1]], [conv_3_offset, conv_3_offset])
        self.line_conv_3.setPen(self.line_pen)
        self.line_conv_3.attach(self.plot_conv)
        self.sgn_conv_3.setData(time, conv_2)
        self.sgn_conv_3.setPen(self.graph_pen)
        self.sgn_conv_3.attach(self.plot_conv)


class ScaleEngine():
    def __init__(self, plot, x=[], y=[], coef=0.2, borders=None):
        self.plot = plot;
        self.max_value_x = 0;
        self.min_value_x = 0;
        self.max_value_y = 0;
        self.min_value_y = 0;

        # Границы меньше которых масштаб быть не может
        # border - двумерный массив (2 оси на 2 границы)
        self.set_min_x = 0;
        self.set_max_x = 0;
        self.set_min_y = 0;
        self.set_max_y = 0;
        if borders != None:
            self.set_min_x = borders[0][0];
            self.set_max_x = borders[0][1];
            self.set_min_y = borders[1][0];
            self.set_max_y = borders[1][1];

        self.coef = coef;
        self.engine(x, y);

    def engine(self, x=[], y=[]):
        if x != []:
            value_max = np.max(x) + (self.coef * np.max(x))
            value_min = np.min(x) + (self.coef * np.min(x))
            self.min_value_x = np.floor(10 * value_min) / 10
            self.max_value_x = np.ceil(10 * value_max) / 10

            if self.min_value_x > self.set_min_x:
                self.min_value_x = self.set_min_x
            if self.max_value_x < self.set_max_x:
                self.max_value_x = self.set_max_x

            step_x = (self.max_value_x - self.min_value_x) / 10
            self.plot.setAxisScale(QwtPlot.xBottom,
                                   self.min_value_x,
                                   self.max_value_x,
                                   step_x)
        if y != []:
            value_max = np.max(y) + (self.coef * np.max(y))
            value_min = np.min(y) + (self.coef * np.min(y))
            self.min_value_y = np.floor(10 * value_min) / 10
            self.max_value_y = np.ceil(10 * value_max) / 10

            if self.min_value_y > self.set_min_y:
                self.min_value_y = self.set_min_y
            if self.max_value_y < self.set_max_y:
                self.max_value_y = self.set_max_y

            step_y = (self.max_value_y - self.min_value_y) / 10
            self.plot.setAxisScale(QwtPlot.yLeft,
                                   self.min_value_y,
                                   self.max_value_y,
                                   step_y)
