from numpy import pi, sqrt


def change_module(modem, osc_per_sym, freq, sym_number, modulation):
    # Начальная настройка модулятора (TODO Кнопочки и крутилки)
    modem.signal.frequency = freq
    modem.signal.phase = 0  # Начальная фаза сигнала
    modem.code_type = "prob"
    modem.sym_number = sym_number
    modem.unit_time = osc_per_sym / modem.signal.frequency

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
        modem.signal.phase = pi / 4
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


def change_line(line, input_signal, channel, noise_factor, add_snr=None):
    # Вычисление действующей амплитуды сигнала
    dispersion = input_signal.dispersion()

    # Выбор типа канала связи
    if channel == "Канал без искажений":
        line.change_parameters(
            input_signal=input_signal,
            type_of_line='simple')

    elif channel == "Гауссовская помеха":
        if add_snr is not None:
            line.change_parameters(
                input_signal=input_signal,
                type_of_line='gauss',
                dispersion=sigma(dispersion, add_snr),
                mu=0)
        else:
            line.change_parameters(
                input_signal=input_signal,
                type_of_line='gauss',
                dispersion=sigma(dispersion, noise_factor),
                mu=0)

    elif channel == "Релеевские замирания":
        line.change_parameters(
            input_signal=input_signal,
            dispersion=sigma(dispersion, add_snr),
            type_of_line='relei',
            param=noise_factor,
            impact=1,
            mu=0)

    elif channel == "Гармоническая помеха":
        line.change_parameters(
            input_signal=input_signal,
            type_of_line='garmonic',
            dispersion=sigma(dispersion, add_snr),
            param=noise_factor,
            impact=1,
            mu=0)

    elif channel == "Линейные искажения":
        line.change_parameters(
            input_signal=input_signal,
            dispersion=sigma(dispersion, add_snr),
            mu=0,
            type_of_line='line_distor')


def sigma(dispersion, param):
    if param:
        return sqrt(dispersion / (10 ** (param / 10)))
    else:
        return 0
