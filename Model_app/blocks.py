from math import pi

def change_modul(modem, osc_per_sym, freq, sym_number, modulation):
        # Начальная настройка модулятора (TODO Кнопочки и крутилки)
        modem.signal.frequency = freq
        modem.signal.phase = 0                                                  # Начальная фаза сигнала
        modem.code_type = "prob"
        modem.sym_number = sym_number
        modem.unit_time = osc_per_sym/modem.signal.frequency

        # Выбор типа модуляции и его донастройка
        if modulation == "2-ФМ":
            modem.number = 2
            modem.PM()

        elif modulation == "4-ФМ":
            modem.number = 4
            modem.PM()

        elif modulation == "8-ФМ":
            modem.number = 8
            modem.PM()

        elif modulation == "4-ФМ со сдвигом":
            modem.signal.phase = pi/4
            modem.number = 4
            modem.PM()

        elif modulation == "8-АФМ":
            modem.number = 8
            modem.APM()

        elif modulation == "16-АФМ":
            modem.number = 16
            modem.APM()

        elif modulation == "16-КАМ":
            modem.number = 16
            modem.QAM()

        elif modulation == "ЧМ":
            modem.number = 2
            modem.FM()

        elif modulation == "ММС":
            modem.number = 2
            modem.FM()

def change_line(line, input_signal, channel, noise_factor):
        # Cтандартное SNR
        bit_error = 1      # SNR в разах

        # Средняя амплитуда полезного сигнала на дискрету
        dis_input = 2 * input_signal.dispersion()    # Мощa (Умножение на 2 - полукостыль для соответствия проге)

        # Выбор типа канала связи
        # TODO Перенастроить Гауссовскую помеху, как добавочную к исходному сигналу
        if channel == "Канал без искажений":
            line.change_parameters(
                input_signal = input_signal, 
                type_of_line = 'simple')

        elif channel == "Гауссовская помеха":
            line.change_parameters(
                input_signal = input_signal, 
                type_of_line = 'gauss', 
                dispersion = dis_input/noise_factor, 
                mu = 0)

        elif channel == "Релеевские замирания":
            line.change_parameters(
                input_signal = input_signal, 
                type_of_line = 'relei', 
                dispersion = dis_input/bit_error,
                param = noise_factor,
                mu = 0)

        elif channel == "Гармоническая помеха":
            line.change_parameters(
                input_signal = input_signal,
                type_of_line = 'garmonic', 
                dispersion = dis_input/bit_error,
                param = noise_factor,
                mu = 0)

        elif channel == "Линейные искажения":
            line.change_parameters(
                input_signal = input_signal, 
                type_of_line = 'line_distor')