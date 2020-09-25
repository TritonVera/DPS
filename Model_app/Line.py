"""
Модуль линии связи:
Работает как черный ящик с многими входными данными и с одним выходом
Вход: kwargs - словарь параметров и их значений для настройки линии связи,
а также может содержать входные данные для работы с ними
Выход: output - выходной сигнал
С внешней стороны доступно только поле output и метод change_parameters
"""

import random

class CommLine():

	def __init__(self, **kwargs):

		# Init new input signal and output
		self.__input = []
		self.output = []

		# Communication line noise parameters
		self.__type_of_line = 0
		self.__dispersion = 0
		self.__mu = 0

		# Load setup methods
		self.change_parameters(**kwargs)

	def change_parameters(self, **kwargs):

		# Search right keys in input parameters 
		for key in kwargs:
			# Load new input signal
			if key == 'input_signal':
				self.__input = kwargs[key]
				self.output = []

			# Switch to choose type of communication line
			if key == 'type_of_line':
				if kwargs[key] == 'gauss':
					self.__type_of_line = 1
				elif kwargs[key] == 'line_distor':
					self.__type_of_line = 2
				elif kwargs[key] == 'garmonic':
					self.__type_of_line = 3
				elif kwargs[key] == 'relei':
					self.__type_of_line = 4

			# Change init parameters of noise
			elif key == 'dispersion':
				self.__dispersion = kwargs[key]
			elif key == 'mu':
				self.__mu = kwargs[key]

		# Link to work methods
		self.__choose_mode()

	# Switch to choose work method
	def __choose_mode(self):
		if self.__type_of_line == 0:
			self.output = self.__input.copy()
		elif self.__type_of_line == 1:
			self.__gauss()
		elif self.__type_of_line == 2:
			self.__line_distor()
		elif self.__type_of_line == 3:
			self.__garmonic()
		elif self.__type_of_line == 4:
			self.__relei()

	# Work methods
	def __gauss(self):
		for i in range(len(self.__input)):
			self.output.append(self.__input[i] + \
			random.gauss(self.__mu, self.__dispersion))

	def __line_distor(self):
		pass

	def __garmonic(self):
		pass

	def __relei(self):
		pass

	# Debug methods
	def print_input(self):
		print(self.__input)

	def print_output(self):
		print(self.output)
