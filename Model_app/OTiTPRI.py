import sys

from PyQt5.QtWidgets import QApplication
from UI import DemoWindow as UI
from Modem import Modem
from Model import Model
from Line import CommLine
from Controller import Controller
from Processor import Processor

Modem = Modem()
Processor = Processor()
Model.signal.frequency = 1
NKP = CommLine()
app = QApplication(sys.argv)
ui = UI()

manage = Controller(ui, Modem, NKP, Processor)
ui.button_panel.plot_button.clicked.connect(manage.plot_view)
ui.line_panel.combobox.activated.connect(manage.show_param)
ui.error_panel.combobox.activated.connect(manage.show_error)
ui.show_panel.fft.toggled.connect(manage.show_fft)

ui.show()
sys.exit(app.exec_())