

import visa

class gpib(object):

    def __ini__(self):

        self._rm = visa.ResourceManager()
        self._resource = None

    def open(self, address):
        result = False
        self._resource = self._rm.open_resource(address)
        print('Test',self._resource )
        if (self._resource == True):
            result = True
        return result

if __name__ == "__main__":

   # tester = gpib()
    #tester.open('GPIB5::28::INSTR')

    rm = visa.ResourceManager()
print(rm.list_resources())
instrumentA = rm.open_resource('GPIB1::28::INSTR')
instrumentB = rm.open_resource('GPIB1::29::INSTR')
print('Instrument A:',instrumentA.query('*IDN?'))
print('Instrument B:',instrumentB.query('*IDN?'))

print('Instrument A:', instrumentA.query('ATT?'))
instrumentA.write('ATT 1.12')
print('Instrument A:', instrumentA.query('ATT?'))