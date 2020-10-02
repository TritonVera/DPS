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

        self.i_flag = 1;
        self.q_flag = 1;
        self.z_flag = 1;
        self.w_flag = 1;

        self.add_plot = QwtPlot(self)
        self.add_plot.setVisible(0)
        self.plot = QwtPlot(self)
        self.line_i = QwtPlotCurve()
        self.line_q = QwtPlotCurve()
        self.line_z = QwtPlotCurve()
        self.line_w = QwtPlotCurve()
        self.draw_plot()

        vertical_layout.addWidget(self.plot)
        vertical_layout.addWidget(self.add_plot)

        self.setLayout(vertical_layout)
        
    def draw_addPlot(self,x_points = [], w_points = []):
        
        x_list = np.asarray(x_points)
        w_list = np.asarray(w_points)

        w_color = QColor(0, 128, 128)
        w_pen = QPen(w_color)
        w_pen.setWidth(2)
        
        self.line_w.setData(x_list, w_list)
        self.line_w.setPen(w_pen)
        if self.w_flag:
            self.line_w.attach(self.add_plot)
        else:
            self.line_w.detach()
                    
        self.add_plot.replot()
      
    def draw_plot(self, x_points = [], i_points = [], q_points = [], z_points = [],):
        x_list = np.asarray(x_points)
        i_list = np.asarray(i_points)
        q_list = np.asarray(q_points)
        z_list = np.asarray(z_points)

        z_color = QColor(0, 128, 128)
        z_pen = QPen(z_color)
        z_pen.setWidth(2)

        self.line_z.setData(x_list, z_list)
        self.line_z.setPen(z_pen)
        if self.z_flag:
            self.line_z.attach(self.plot)
        else:
            self.line_z.detach() 
        
        i_color = QColor(255, 0, 255)
        i_pen = QPen(i_color)
        i_pen.setWidth(2)

        self.line_i.setData(x_list, i_list)
        self.line_i.setPen(i_pen)
        if self.i_flag:
            self.line_i.attach(self.plot)
        else:
            self.line_i.detach()

        q_color = QColor(255, 0, 0)
        q_pen = QPen(q_color)
        q_pen.setWidth(2)

        self.line_q.setData(x_list, q_list)
        self.line_q.setPen(q_pen)
        if self.q_flag:
            self.line_q.attach(self.plot)
        else:
            self.line_q.detach()     

        self.plot.replot()
        self.plot.show()
