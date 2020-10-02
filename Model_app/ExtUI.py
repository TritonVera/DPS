import numpy as np

from PyQt5.QtWidgets import QSizePolicy, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve

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
      
    def draw_plot(self, y_points = []):
        x_list = np.arange(len(y_points))
        y_list = np.asarray(y_points)

        y_color = QColor(0, 128, 128)
        y_pen = QPen(y_color)
        y_pen.setWidth(1)

        self.signal.setData(x_list, y_list)
        self.signal.setPen(y_pen)
        self.signal.attach(self.plot)    

        self.plot.replot()
        self.plot.show()
