import numpy as np

#------------------------------------------------------------------------------
# Решающее устройство некогерентного приемника
class NoCogDecisiveDevice():

    def __init__(self, points, modul = ""):
        if points.size == 0:
            return
        self.points = points
        if modul == "2-ФМ":
            self.bits = np.zeros((points.size,1))
            self.PM2()
        elif modul == "4-ФМ":
            self.bits = np.zeros((points.size,2))
            self.PM4()
        elif modul == "4-ФМ со сдвигом":
            self.bits = np.zeros((points.size,2))
            self.PM4s()
        elif modul == "8-ФМ":
            self.bits = np.zeros((points.size,3))
            self.PM8()
        elif modul == "8-АФМ":
            self.bits = np.zeros((points.size,3))
            self.APM8()
        elif modul == "16-АФМ":
            self.bits = np.zeros((points.size,4))
            self.APM16()
        elif modul == "16-КАМ":
            self.bits = np.zeros((points.size,4))
            self.QAM16()
        elif modul == "ЧМ":
            self.bits = np.zeros((points.size,1))
            self.FM()
        elif modul == "Ортогональный ЧМ":
            self.bits = np.zeros((points.size,1))
            self.FM()
        elif modul == "ММС":
            self.bits = np.zeros((points.size,1))
            self.MPS()
        else:
            return
        self.bits = np.array(self.bits, dtype=int)

    def PM2(self):
        for i in range(self.points.size):
            if self.points[i].real < 0:
                self.bits[i] = [1]
            else:
                self.bits[i] = [0]

    def PM4(self):
        for i in range(self.points.size):
            if self.points[i].real + self.points[i].imag > 0:
                if self.points[i].real - self.points[i].imag > 0:
                    self.bits[i] = [0, 0]
                else:
                    self.bits[i] = [1, 1]
            else:
                if self.points[i].real - self.points[i].imag > 0:
                    self.bits[i] = [0, 1]
                else:
                    self.bits[i] = [1, 0]

    def PM4s(self):
        for i in range(self.points.size):
            if self.points[i].real > 0:
                if self.points[i].imag > 0:
                    self.bits[i] = [1, 1]
                else:
                    self.bits[i] = [0, 0]
            else:
                if self.points[i].imag > 0:
                    self.bits[i] = [1, 0]
                else:
                    self.bits[i] = [0, 1]

    def PM8(self):
        for i in range(self.points.size):
            if (0.404*self.points[i].real) + self.points[i].imag > 0:
                if self.points[i].real - (0.404*self.points[i].imag) > 0:
                    if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                        self.bits[i] = [1, 1, 1]
                    else:
                        self.bits[i] = [0, 0, 0]
                else:
                    if (0.404*self.points[i].imag) + self.points[i].real > 0:
                        self.bits[i] = [1, 1, 0]
                    else:
                        self.bits[i] = [1, 0, 1]
            else:
                if self.points[i].real - (0.404*self.points[i].imag) > 0:
                    if (0.404*self.points[i].imag) + self.points[i].real > 0:
                        self.bits[i] = [0, 0, 1]
                    else:
                        self.bits[i] = [0, 1, 0]
                else:
                    if -(0.404*self.points[i].real) + self.points[i].imag > 0:
                        self.bits[i] = [1, 0, 0]
                    else:
                        self.bits[i] = [0, 1, 1]

    def APM8(self):
        for i in range(self.points.size):
            if np.abs(self.points[i]) < 1.5:
                if self.points[i].real + self.points[i].imag > 0:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits[i] = [0, 0, 0]
                    else:
                        self.bits[i] = [0, 1, 1]
                else:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits[i] = [0, 0, 1]
                    else:
                        self.bits[i] = [0, 1, 0]
            else:
                if self.points[i].real + self.points[i].imag > 0:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits[i] = [1, 0, 0]
                    else:
                        self.bits[i] = [1, 1, 1]
                else:
                    if self.points[i].real - self.points[i].imag > 0:
                        self.bits[i] = [1, 0, 1]
                    else:
                        self.bits[i] = [1, 1, 0]

    def APM16(self):
        pass

    def QAM16(self):
        for i in range(self.points.size):
            if self.points[i].real < -2:
                if self.points[i].imag < -2:
                    self.bits[i] = [0, 0, 0, 0]
                elif self.points[i].imag > -2 and self.points[i].imag < 0:
                    self.bits[i] = [0, 0, 0, 1]
                elif self.points[i].imag > 0 and self.points[i].imag < 2:
                    self.bits[i] = [0, 0, 1, 0]
                else:
                    self.bits[i] = [0, 0, 1, 1]
            elif self.points[i].real > -2 and self.points[i].real < 0:
                if self.points[i].imag < -2:
                    self.bits[i] = [0, 1, 0, 0]
                elif self.points[i].imag > -2 and self.points[i].imag < 0:
                    self.bits[i] = [0, 1, 0, 1]
                elif self.points[i].imag > 0 and self.points[i].imag < 2:
                    self.bits[i] = [0, 1, 1, 0]
                else:
                    self.bits[i] = [0, 1, 1, 1]
            elif self.points[i].real > 0 and self.points[i].real < 2:
                if self.points[i].imag < -2:
                    self.bits[i] = [1, 0, 0, 0]
                elif self.points[i].imag > -2 and self.points[i].imag < 0:
                    self.bits[i] = [1, 0, 0, 1]
                elif self.points[i].imag > 0 and self.points[i].imag < 2:
                    self.bits[i] = [1, 0, 1, 0]
                else:
                    self.bits[i] = [1, 0, 1, 1]
            else:
                if self.points[i].imag < -2:
                    self.bits[i] = [1, 1, 0, 0]
                elif self.points[i].imag > -2 and self.points[i].imag < 0:
                    self.bits[i] = [1, 1, 0, 1]
                elif self.points[i].imag > 0 and self.points[i].imag < 2:
                    self.bits[i] = [1, 1, 1, 0]
                else:
                    self.bits[i] = [1, 1, 1, 1]

    def FM(self):
        for i in range(self.points.size):
            if self.points[i].imag - self.points[i].real > 0:
                self.bits[i] = [1]
            else:
                self.bits[i] = [0]

    def MPS(self):
        pass
