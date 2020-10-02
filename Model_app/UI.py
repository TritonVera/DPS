# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 15:10:12 2020

@author: Григорий
@author: Ivan
"""
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QSizePolicy, \
                            QMessageBox, QWidget, QGroupBox, QRadioButton, \
                            QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                            QDoubleSpinBox, QCheckBox, QSpinBox
from PyQt5.QtCore import Qt, QTimer
from ExtUI import PlotPanel

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

        self.modul_panel = ModulPanel(self.main_widget)
        self.main_grid.addWidget(self.modul_panel, 0, 0)

        self.line_panel = LinePanel(self.main_widget)
        self.main_grid.addWidget(self.line_panel, 1, 0, -1, 1)

        self.plot_panel = PlotPanel(self.main_widget)
        self.main_grid.addWidget(self.plot_panel, 0, 1, 2, -1)

        self.button_panel = ButtonPanel(self.main_widget)
        self.main_grid.addWidget(self.button_panel, 2, 1, -1, 1)

        self.main_widget.setLayout(self.main_grid)


    def create_main_widget(self):
        self.main_widget = QWidget()
        self.main_widget.setMinimumSize(800, 640)
        self.main_widget.setGeometry(0, 0, 800, 640)
        self.setCentralWidget(self.main_widget)


    def about(self):
        QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py demonstartion
Copyright 2020 Ivan Fomin, 2020 Grigory Galchenkov

This program is a demonstration of excite signal in receiver.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
                                )

class ModulPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setFixedSize(self, 300, 300)
        QWidget.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Fixed)

        #Create main widget and layout
        vertical_layout = QVBoxLayout()

        #Create groupboxes
        exciter_box = QGroupBox(self)
        exciter_box.setTitle("Модуляция")

        #Make main layout packer
        inner_grid_layout = QGridLayout(exciter_box)
        
        #Create radiobuttons
        self.bpsk_radiobutton = QRadioButton("BPSK", exciter_box)
        self.qpsk_radiobutton = QRadioButton("QPSK", exciter_box)

        #Pack radiobuttons
        inner_grid_layout.addWidget(self.bpsk_radiobutton, 0, 0)
        inner_grid_layout.addWidget(self.qpsk_radiobutton, 1, 0)

        #Ending packers
        exciter_box.setLayout(inner_grid_layout)
        vertical_layout.addWidget(exciter_box)
        self.setLayout(vertical_layout)


class LinePanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMaximumSize(self, 300, MAX_PIXEL_SIZE)
        QWidget.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Expanding)

        #Create main widget and layout
        vertical_layout = QVBoxLayout()

        #Create groupboxes
        setup_box = QGroupBox(self)
        setup_box.setTitle("Канал связи")

        #Make main layout packer
        inner_grid_layout = QGridLayout(setup_box)
        
        # Create elements
        self.no_noise_radiobutton = QRadioButton("Канал без искажений", setup_box)
        self.gauss_radiobutton = QRadioButton("Гауссовская помеха", setup_box)

        # Pack elememnts
        inner_grid_layout.addWidget(self.no_noise_radiobutton, 0, 0)
        inner_grid_layout.addWidget(self.gauss_radiobutton, 1, 0)

        #Ending packers
        setup_box.setLayout(inner_grid_layout)

        vertical_layout.addWidget(setup_box)
        self.setLayout(vertical_layout)


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
        self.exit_button = QPushButton("Выход", button_box)
        self.plot_button = QPushButton("Построить", button_box)

        # Add to layout
        box_layout.addWidget(self.plot_button)
        box_layout.addWidget(self.exit_button)
        button_box.setLayout(box_layout)

        # Place main layout
        simple_layout.addWidget(button_box)
        self.setLayout(simple_layout)