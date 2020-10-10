import numpy as np

from PyQt5.QtWidgets import QSizePolicy, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve, QwtPlotGrid

#Класс графического полотна
class PlotPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)
      
    def draw_plot(self, y_points = np.arange(0)):
        
        x_list = np.arange(y_points.size)
        y_list = y_points

        y_color = QColor(0, 128, 128)
        y_pen = QPen(y_color)
        y_pen.setWidth(1)

        self.signal.setData(x_list, y_list)
        self.signal.setPen(y_pen)
        self.signal.attach(self.plot)    

        self.plot.replot()
        self.plot.show()


class StarPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        vertical_layout = QVBoxLayout()

        self.plot = QwtPlot(self)
        self.signal = QwtPlotCurve()
        self.grid = QwtPlotGrid()

        self.plot.setAxisScale(QwtPlot.xBottom, -1.2, 1.2, 0.2)
        self.plot.setAxisScale(QwtPlot.yLeft, -1.2, 1.2, 0.2)

        self.grid.attach(self.plot)
        grid_color = QColor(196, 196, 196)
        grid_pen = QPen(grid_color)
        grid_pen.setWidth(0.5)
        self.grid.setPen(grid_pen)

        self.signal.setStyle(QwtPlotCurve.Dots)
        self.draw_plot()

        vertical_layout.addWidget(self.plot)

        self.setLayout(vertical_layout)
      
    def draw_plot(self, x_points = np.arange(0), y_points = np.arange(0)):
        
        x_list = x_points
        y_list = y_points

        y_color = QColor(128, 0, 0)
        y_pen = QPen(y_color)
        y_pen.setWidth(5)

        self.signal.setData(x_list, y_list)
        self.signal.setPen(y_pen)
        self.signal.attach(self.plot)    

        self.plot.replot()
        self.plot.show()