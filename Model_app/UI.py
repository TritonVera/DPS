# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 15:10:12 2020

@author: Григорий
@author: Ivan
"""
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QSizePolicy, \
                            QMessageBox, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox, QCheckBox, QSpinBox, QComboBox
from PyQt5.QtCore import Qt, QTimer
from ExtUI import PlotPanel, StarPanel

MAX_PIXEL_SIZE = 16777215

#Класс главного окна
class DemoWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Демонстрационная программа")
        self.timer = QTimer()
        self.create_ui()

    def create_ui(self):
        #Create and configure central widget
        self.create_main_widget()

        #Create and configure packer
        self.main_grid = QGridLayout(self.main_widget)

        self.modul_panel = ChangePanel(self.main_widget, "Тип модуляции", 
                                    ["BPSK", 
                                     "QPSK", 
                                     "QPSK со сдвигом", 
                                     "8-PSK", 
                                     "APM8",
                                     "APM16",
                                     "FM"])
        self.main_grid.addWidget(self.modul_panel, 0, 0)

        self.line_panel = ChangePanel(self.main_widget, "Тип канала связи", 
                                    ["Канал без искажений", 
                                     "Гауссовская помеха", 
                                     "Линейные искажения", 
                                     "Гармоническая помеха", 
                                     "Релеевская помеха"])
        self.main_grid.addWidget(self.line_panel, 0, 1)

        self.signal_panel = SignalPanel(self.main_widget)
        self.main_grid.addWidget(self.signal_panel, 1, 0)

        self.nf_panel = NFPanel(self.main_widget)
        self.nf_panel.setVisible(0)
        self.main_grid.addWidget(self.nf_panel, 1, 1)

        self.transmitter_panel = ChangePanel(self.main_widget, "Тип приемника", 
                                    ["Созвездия сигнал"])
        self.main_grid.addWidget(self.transmitter_panel, 0, 2)

        self.plot_panel = PlotPanel(self.main_widget)
        self.main_grid.addWidget(self.plot_panel, 2, 0, 1, 2)

        self.star_panel = StarPanel(self.main_widget)
        self.main_grid.addWidget(self.star_panel, 2, 2)

        self.button_panel = ButtonPanel(self.main_widget)
        self.main_grid.addWidget(self.button_panel, 3, 0, -1, -1)

        self.main_widget.setLayout(self.main_grid)


    def create_main_widget(self):
        self.main_widget = QWidget()
        self.main_widget.setMinimumSize(1000, 600)
        self.main_widget.setGeometry(0, 0, 1000, 640)
        self.setCentralWidget(self.main_widget)


    def about(self):
        QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py demonstartion
Copyright 2020 Ivan Fomin, 2020 Grigory Galchenkov

This program is a demonstration of excite signal in receiver.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
                                )

class ChangePanel(QWidget):
    def __init__(self, parent = None, name = "", combo_box = []):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 200, 100)
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Make main layout packer
        inner_grid_layout = QGridLayout(self)
        
        # Create elements
        self.name_label = QLabel(name, self)
        self.name_label.setFixedSize(150, 15)

        self.combobox = QComboBox(self)
        self.combobox.addItems(combo_box)

        #Pack radiobuttons
        inner_grid_layout.addWidget(self.name_label, 0, 0)
        inner_grid_layout.addWidget(self.combobox, 1, 0)

        #Ending packers
        self.setLayout(inner_grid_layout)


class NFPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 200, 70)
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Make main layout packer
        inner_grid_layout = QHBoxLayout(self)
        
        self.noise_label = QLabel("Сигнал/шум (разы)", self)

        self.noise_factor_spinbox = QDoubleSpinBox(self)
        self.noise_factor_spinbox.setValue(10.0)
        self.noise_factor_spinbox.setRange(0.1, 100)
        self.noise_factor_spinbox.setSingleStep(0.1)

        # Pack elememnts
        inner_grid_layout.addWidget(self.noise_label)
        inner_grid_layout.addWidget(self.noise_factor_spinbox)

        #Ending packers
        self.setLayout(inner_grid_layout)


class SignalPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 200, 70)
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Make main layout packer
        inner_grid_layout = QGridLayout(self)
        
        self.time_label = QLabel("Время сигнала, нс", self)

        self.time_spinbox = QDoubleSpinBox(self)
        self.time_spinbox.setValue(10)
        self.time_spinbox.setRange(10, 1000)

        # Pack elememnts
        inner_grid_layout.addWidget(self.time_label, 0, 0)
        inner_grid_layout.addWidget(self.time_spinbox, 0, 1)

        self.freq_label = QLabel("Частота сигнала, ГГц", self)

        self.freq_spinbox = QDoubleSpinBox(self)
        self.freq_spinbox.setValue(1)
        self.freq_spinbox.setRange(0.1, 100)
        self.freq_spinbox.setSingleStep(0.1)

        # Pack elememnts
        inner_grid_layout.addWidget(self.freq_label, 1, 0)
        inner_grid_layout.addWidget(self.freq_spinbox, 1, 1)

        #Ending packers
        self.setLayout(inner_grid_layout)


class ButtonPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setMaximumSize(MAX_PIXEL_SIZE, MAX_PIXEL_SIZE)
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Fixed)

        simple_layout = QHBoxLayout()
        button_box = QGroupBox(self)
        button_box.setTitle("Управление")
        box_layout = QVBoxLayout(button_box)

        # Create buttons
        # self.exit_button = QPushButton("Выход", button_box)
        self.plot_button = QPushButton("Построить", button_box)

        # Add to layout
        box_layout.addWidget(self.plot_button)
        # box_layout.addWidget(self.exit_button)
        button_box.setLayout(box_layout)

        # Place main layout
        simple_layout.addWidget(button_box)
        self.setLayout(simple_layout)