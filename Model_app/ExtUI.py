import numpy as np

from PyQt5.QtWidgets import QSizePolicy, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve, QwtPlotGrid, QwtText

#Класс графического полотна
class PlotPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.title = QwtText()
        self.title.setText('0021302')
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
        # self.title.attach(self.plot)
        self.signal.attach(self.plot)

        self.plot.replot()
        self.plot.show()


class StarPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        # QWidget.setFixedSize(self, 400, 400)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.grid = QwtPlotGrid()

        self.plot.setAxisScale(QwtPlot.xBottom, -1.2, 1.2, 0.4)
        self.plot.setAxisScale(QwtPlot.yLeft, -1.2, 1.2, 0.4)

        self.grid.attach(self.plot)
        grid_color = QColor(196, 196, 196)
        grid_pen = QPen(grid_color)
        grid_pen.setWidth(0.5)
        self.grid.setPen(grid_pen)

        self.signal.setStyle(QwtPlotCurve.Dots)
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)
      
    def draw_plot(self, *points):
        
        num = 0
        for graph in points:
            x_list = graph.real
            y_list = graph.imag

            y_pen = QPen(QColor(128, 0, 0))
            y_pen.setWidth(5)

            if num == 1:
                y_pen = QPen(QColor(0, 128, 0))
            elif num == 2:
                y_pen = QPen(QColor(0, 0, 128))
            elif num == 3:
                y_pen = QPen(QColor(0, 0, 0))

            self.signal.setData(x_list, y_list)
            self.signal.setPen(y_pen)
            self.signal.attach(self.plot)    

            self.plot.replot()
            self.plot.show()
            num = num + 1