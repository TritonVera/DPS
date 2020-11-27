import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve, QwtPlotGrid, QwtPlotMarker

#Класс графического полотна
class PlotPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumHeight(self, 200)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.eng = ScaleEngine(self.plot, coef = 0.25);
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)
      
    def draw_plot(self, points = np.zeros((2, 1))):
        
        y_list = points[0, :]
        x_list = points[1, :]

        y_color = QColor(0, 128, 128)
        y_pen = QPen(y_color)
        y_pen.setWidth(2)

        self.signal.setData(x_list, y_list)
        self.signal.setPen(y_pen)
        self.signal.attach(self.plot)

        self.eng.engine(y = y_list);

        self.draw_div(x_list[-1])

    def draw_div(self, end):
        self.markers = []
        l_color = QColor(16, 16, 16)
        l_pen = QPen(l_color)
        l_pen.setWidth(1)
        l_pen.setStyle(Qt.DashLine)
        for i in np.arange(np.floor(end/2), dtype = np.int):
            marker = QwtPlotMarker()
            self.markers.append(marker)
            self.markers[i].setValue((1+i) * 2.0, 0.0 )
            self.markers[i].setLineStyle(QwtPlotMarker.VLine)
        # self.first_marker.setLabelAlignment(Qt.AlignRight | Qt.AlignBottom )
            self.markers[i].setLinePen(l_pen)

            self.markers[i].attach(self.plot)

        # self.d_marker2 = Qwt.QwtPlotMarker()
        # self.d_marker2.setLineStyle( Qwt.QwtPlotMarker.HLine )
        # self.d_marker2.setLabelAlignment( Qt.AlignRight | Qt.AlignBottom )
        # self.d_marker2.setLinePen( QColor( 200, 150, 0 ), 0, Qt.DashDotLine )
        # self.d_marker2.setSymbol( Qwt.QwtSymbol( Qwt.QwtSymbol.Diamond,QColor( Qt.yellow ), QColor( Qt.green ), QSize( 8, 8 ) ) )
        # self.d_marker2.attach( self )

        self.plot.replot()
        self.plot.show()

class FftPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumHeight(self, 200)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.plot.enableAxis(QwtPlot.yLeft, 0)

        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)
      
    def draw_plot(self, graph = np.zeros((1, 0)), freq = 1):
        if graph.size == 0:
            return
        y_list = self.__calc(graph)
        border = freq/2
        step = freq/np.size(y_list)
        x_list = np.arange(-border, border, step)
            
        # Самописный движок масштаба
        ScaleEngine(self.plot, y = y_list)

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
            fft = np.sqrt(y.real**2 + y.imag**2)
            fft = np.roll(fft, int(fft.size/2))
            return fft
        else:
            return t


class StarPanel(QWidget):
    def __init__(self, parent = None):
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
      
    def draw_plot(self, graph = np.zeros((1, 0))):

        x_list = graph.real
        y_list = graph.imag
            
        # Самописный движок масштаба
        ScaleEngine(self.plot, x_list, y_list, borders = [[-1.2, 1.2], [-1.2, 1.2]])

        # Цвет и ширина линии
        y_pen = self.signal.pen()
        y_pen.setWidth(5)

        self.signal.setData(x_list, y_list)
        self.signal.attach(self.plot)    

        self.plot.replot()
        self.plot.show()

    def add_demodul(self, mod = ""):

        if mod == "2-ФМ":
            div_1 = QwtPlotCurve()
            div_1.setStyle(QwtPlotCurve.Sticks)
            div_1.setData([0, 0], [-10, 10])
            div_1.attach(self.plot)

            
class ConvPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 300, 300)
        vertical_layout = QVBoxLayout()

        self.plot_sqrt = QwtPlot(self)
        self.plot_sqrt.enableAxis(QwtPlot.yLeft, 0)

        self.sgn_sqrt_I = QwtPlotCurve()
        self.sgn_sqrt_Q = QwtPlotCurve()
        
        self.plot_conv = QwtPlot(self)
        self.plot_conv.enableAxis(QwtPlot.yLeft, 0)
        
        self.sgn_conv_I = QwtPlotCurve()
        self.sgn_conv_Q = QwtPlotCurve()
        
        # Начальные оси
        self.line_sqrt_I = QwtPlotCurve()
        self.line_sqrt_Q = QwtPlotCurve()
        self.line_conv_I = QwtPlotCurve()
        self.line_conv_Q = QwtPlotCurve()
        
        self.DrawPlots()
        
        vertical_layout.addWidget(self.plot_sqrt)
        vertical_layout.addWidget(self.plot_conv)

        self.setLayout(vertical_layout)
        
    def DrawPlots(self, points = np.zeros((3, 1)), mode = 0):
        time = points[0]
        sqrt_I = points[1]
        conv_I = points[2]
        sqrt_I_offset = 0
        conv_I_offset = 0
        
        line_pen = QPen(QColor(0, 0, 0))
        line_pen.setWidth(1)
        
        i_pen = QPen(QColor(128, 0, 0))
        i_pen.setWidth(2)
        
        q_pen = QPen(QColor(0, 128, 0))
        q_pen.setWidth(2)
        
        self.line_sqrt_I.detach()
        self.line_sqrt_Q.detach()
        self.line_conv_I.detach()
        self.line_conv_Q.detach()
        self.sgn_conv_I.detach()
        self.sgn_conv_Q.detach()
        self.sgn_sqrt_I.detach()
        self.sgn_sqrt_Q.detach()
        
        if mode == 1:
            sqrt_I_offset = np.max(np.abs(points[1])) + 1
            conv_I_offset = np.max(np.abs(points[2])) + 1
            sqrt_I = points[1] + (sqrt_I_offset * np.ones(points[1].size))
            conv_I = points[2] + (conv_I_offset * np.ones(points[2].size))
            
            sqrt_Q_offset = np.max(np.abs(points[3])) + 1
            conv_Q_offset = np.max(np.abs(points[4])) + 1
            sqrt_Q = points[3] - (sqrt_Q_offset * np.ones(points[3].size))
            conv_Q = points[4] - (conv_Q_offset * np.ones(points[4].size))
            
            # Движок масштаба
            ScaleEngine(self.plot_sqrt, y = [np.max(sqrt_I), np.min(sqrt_Q)])
            ScaleEngine(self.plot_conv, y = [np.max(conv_I), np.min(conv_Q)])
            
            self.line_sqrt_Q.setData([0, time[-1]], [-sqrt_Q_offset, -sqrt_Q_offset])
            self.line_sqrt_Q.setPen(line_pen)
            self.line_sqrt_Q.attach(self.plot_sqrt)
            self.sgn_sqrt_Q.setData(time, sqrt_Q)
            self.sgn_sqrt_Q.setPen(q_pen)
            self.sgn_sqrt_Q.attach(self.plot_sqrt)    

            self.line_conv_Q.setData([0, time[-1]], [-conv_Q_offset, -conv_Q_offset])
            self.line_conv_Q.setPen(line_pen)
            self.line_conv_Q.attach(self.plot_conv)
            self.sgn_conv_Q.setData(time, conv_Q)
            self.sgn_conv_Q.setPen(q_pen)
            self.sgn_conv_Q.attach(self.plot_conv) 
        else:            
            # Движок масштаба
            ScaleEngine(self.plot_sqrt, y = sqrt_I)
            ScaleEngine(self.plot_conv, y = conv_I)
         
        self.line_sqrt_I.setData([0, time[-1]], [sqrt_I_offset, sqrt_I_offset])
        self.line_sqrt_I.setPen(line_pen)
        self.line_sqrt_I.attach(self.plot_sqrt)
        self.sgn_sqrt_I.setData(time, sqrt_I)
        self.sgn_sqrt_I.setPen(i_pen)
        self.sgn_sqrt_I.attach(self.plot_sqrt)    

        self.line_conv_I.setData([0, time[-1]], [conv_I_offset, conv_I_offset])
        self.line_conv_I.setPen(line_pen)
        self.line_conv_I.attach(self.plot_conv)
        self.sgn_conv_I.setData(time, conv_I)
        self.sgn_conv_I.setPen(i_pen)
        self.sgn_conv_I.attach(self.plot_conv)

        self.plot_sqrt.replot()
        self.plot_conv.replot()
        
        self.plot_sqrt.show()
        self.plot_conv.show()
            
class ScaleEngine():
    def __init__(self, plot, x = [], y = [], coef = 0.2, borders = None):
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

    def engine(self, x = [], y = []):
        if x != []:
            value_max = np.max(x) + (self.coef*np.max(x))
            value_min = np.min(x) + (self.coef*np.min(x))
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
            value_max = np.max(y) + (self.coef*np.max(y))
            value_min = np.min(y) + (self.coef*np.min(y))
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

