import sys

from PyQt5.QtWidgets import QApplication
from UI import DemoWindow as Ui
from Modem import Modem
from Line import CommLine
from Controller import Controller
from Processor import Processor

app = QApplication(sys.argv)
ui = Ui()

manage = Controller(ui, Modem(), CommLine(), Processor())

# Кнопочки
ui.button_panel.plot_button.clicked.connect(manage.plot_view)
ui.button_panel.about_button.clicked.connect(ui.about)

# Изменение визуализации из-за выбора определенных параметров
ui.line_panel.combobox.activated.connect(manage.show_param)
ui.error_panel.combobox.activated.connect(manage.show_error)
ui.transmitter_panel.combobox.activated.connect(manage.show_kog)
ui.show_panel.fft.toggled.connect(manage.show_fft)
ui.show_panel.kog.toggled.connect(manage.show_ber)

# Показ окна
ui.show()
sys.exit(app.exec_())