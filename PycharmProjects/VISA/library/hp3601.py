

class hp3601(object):

    def __init__(self, instr):
        self._instr = instr

    def __del__(self):
        self._instr.close()

    def getInventory(self):
        return self._instr.query('*IDN?')

    def getAttenuation(self):
        return self._instr.query('ATT?')

    def setAttenuation(self,value):
        self._instr.write('ATT %f',value)