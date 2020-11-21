import numpy as np

from PyQt5.QtWidgets import QSizePolicy, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from qwt import QwtPlot, QwtPlotCurve, QwtPlotGrid, QwtPlotMarker

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

        self.draw_div(x_list[-1])

    def draw_div(self, end):
        self.markers = []
        l_color = QColor(16, 16, 16)
        l_pen = QPen(l_color)
        l_pen.setWidth(2)
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
        
        self.plot.setAxisAutoScale(QwtPlot.xBottom)
        self.plot.setAxisAutoScale(QwtPlot.yLeft)

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