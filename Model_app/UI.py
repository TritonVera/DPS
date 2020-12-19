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
from PyQt5.QtGui import QPalette
from ExtUI import PlotPanel, StarPanel, ConvPanel, FftPanel

MAX_PIXEL_SIZE = 16777215

#Класс главного окна
class DemoWindow(QMainWindow):
    def __init__(self):
        # Конструктор
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Демонстрационная программа")

        # self.timer = QTimer() # Таймер убран из-за остутсвия необходимости к автогенерации сигнала

        # Настройка главного окна
        self.create_main_widget()

        # Настройка визуализации программы
        self.create_ui()

    def create_main_widget(self):
        # Создание и настройка основного окна программы
        self.main_widget = QWidget()
        self.main_widget.setMinimumSize(1000, 800)
        self.main_widget.setGeometry(0, 0, 1000, 960)
        self.setCentralWidget(self.main_widget)

    def create_ui(self):
        # Создание упаковщика
        self.main_grid = QGridLayout(self.main_widget)

        # Блок создания приемника и сигнала (ряд 1)
        # Выбор типа приемника
        self.transmitter_panel = ChangePanel(self.main_widget, "Тип приемника", 
                                    ["Созвездия сигнала",
                                     "Корреляционный приёмник"])
        self.main_grid.addWidget(self.transmitter_panel, 0, 0)

        # Выбор типа модуляции
        self.modul_panel = ChangePanel(self.main_widget, "Тип модуляции", 
                                    ["2-ФМ", 
                                     "4-ФМ", 
                                     "4-ФМ со сдвигом", 
                                     "8-ФМ", 
                                     "8-АФМ",
                                     "16-АФМ",
                                     "16-КАМ",
                                     "ЧМ",
                                     "ММС"])
        self.main_grid.addWidget(self.modul_panel, 0, 1)

        # Тип канала связи
        self.line_panel = ChangePanel(self.main_widget, "Тип канала связи", 
                                    ["Канал без искажений", 
                                     "Гауссовская помеха", 
                                     "Линейные искажения", 
                                     "Гармоническая помеха", 
                                     "Релеевские замирания"])
        self.main_grid.addWidget(self.line_panel, 0, 2)

        # Тип синхронизации
        self.error_panel = ChangePanel(self.main_widget, "Синхронизация", 
                                    ["Без расстройки", 
                                     "Расстройка по частоте", 
                                     "Фазовая расстройка"])
        self.main_grid.addWidget(self.error_panel, 0, 3)

# self.signal_panel = SignalPanel(self.main_widget)
# self.main_grid.addWidget(self.signal_panel, 1, 0)

        # Блок настройки (ряд 2)
        # Настройка показа преобразования Фурье и вероятности ошибки
        self.show_panel = ShowPanel(self.main_widget)
        self.main_grid.addWidget(self.show_panel, 1, 0)

        # Настройка канала связи
        self.nf_panel = NFPanel(self.main_widget)
        self.nf_panel.setEnabled(0)
        self.main_grid.addWidget(self.nf_panel, 1, 2)
        
        # Настройка параметров расстройки
        self.devia_panel = NFPanel(self.main_widget)
        self.devia_panel.setEnabled(0)
        self.main_grid.addWidget(self.devia_panel, 1, 3)

        # Блок графиков (ряд 3-4)
        # Осциллограмма сигнала
        self.plot_panel = PlotPanel(self.main_widget)
        self.main_grid.addWidget(self.plot_panel, 2, 0, 1, 2)

        # Показ созвездия
        self.star_panel = StarPanel(self.main_widget)
        self.star_panel.setVisible(0)
        self.main_grid.addWidget(self.star_panel, 2, 2, 2, 2)
        
        # График корреляции
        self.conv_panel = ConvPanel(self.main_widget)
        self.conv_panel.setVisible(0)
        self.main_grid.addWidget(self.conv_panel, 2, 2, 2, 2)

        # Спектрограмма сигнала
        self.fft_panel = FftPanel(self.main_widget)
        self.fft_panel.setVisible(0)
        self.main_grid.addWidget(self.fft_panel, 3, 0, 1, 2)

        # Блок кнопок (ряд 5)
        self.button_panel = ButtonPanel(self.main_widget)
        self.main_grid.addWidget(self.button_panel, 4, 0, -1, -1)

        # Упаковка на главный виджет
        self.main_widget.setLayout(self.main_grid)

    def about(self):
        # Пасхалка о создателях проги :)
        QMessageBox.about(self, "About",
                                    """Embedding_in_qt5.py demonstartion
Copyright 2020 Ivan Fomin, 2020 Grigory Galchenkov

This program is a demonstration of excite signal in receiver.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation."""
                                )

# Классы визуальных объектов
class ChangePanel(QWidget):
    def __init__(self, parent = None, name = "", combo_box = []):
        QWidget.__init__(self, parent)
        QWidget.setMinimumWidth(self, 200)
        QWidget.setFixedHeight(self, 120)
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


class ShowPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        # QWidget.setFixedHeight(self, 90)

        # Configure size policy
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Make main layout packer
        inner_grid_layout = QVBoxLayout(self)

        self.fft = QCheckBox("Преобразование Фурье", self)
        self.kog = QCheckBox("Некогерентный приём", self)
        self.ber = QCheckBox("Уточ. вероятность ошибки", self)
        self.fft.setEnabled(0)
        self.kog.setChecked(1)
        self.kog.setEnabled(0)
        self.label = QLabel("", self)
        # self.label.setVisible(0)

        inner_grid_layout.addWidget(self.kog)
        inner_grid_layout.addWidget(self.fft)
        inner_grid_layout.addWidget(self.ber)
        inner_grid_layout.addWidget(self.label)

        #Ending packers
        self.setLayout(inner_grid_layout)


class NFPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        # QWidget.setFixedHeight(self, 90)
        QWidget.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Fixed)

        #Make main layout packer
        inner_grid_layout = QHBoxLayout(self)
        
        self.noise_label = QLabel("", self)

        self.noise_factor_spinbox = QDoubleSpinBox(self)
        self.noise_factor_spinbox.setValue(10.0)
        self.noise_factor_spinbox.setRange(0, 100)
        self.noise_factor_spinbox.setSingleStep(1)

        # Pack elememnts
        inner_grid_layout.addWidget(self.noise_label)
        inner_grid_layout.addWidget(self.noise_factor_spinbox)

        #Ending packers
        self.setLayout(inner_grid_layout)
        
    def configure(self, label = None, borders = [], value = None, step = None):
        if label != None:
            self.noise_label.setText(label)
        if borders != []:
            self.noise_factor_spinbox.setRange(borders[0], borders[1])
        if value != None:
            self.noise_factor_spinbox.setValue(value)
        if step != None:
            self.noise_factor_spinbox.setSingleStep(step)
            

class SignalPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        QWidget.setMinimumSize(self, 200, 150)
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
        self.about_button = QPushButton("О программе", button_box)
        self.plot_button = QPushButton("Построить", button_box)

        # Add to layout
        box_layout.addWidget(self.plot_button)
        # box_layout.addWidget(self.exit_button)
        box_layout.addWidget(self.about_button)
        button_box.setLayout(box_layout)

        # Place main layout
        simple_layout.addWidget(button_box)
        self.setLayout(simple_layout)