import visa
import pyvisa


rm = visa.ResourceManager()
#rm = visa.ResourceManager('@py')
#dmm=rm.open_resource('TCPIP0::172.17.115.132::inst0::INSTR')
#dmm=rm.open_resource('TCPIP0::172.17.115.132::GPIB5::28::INSTR')
print(rm.list_resources())

inst = rm.open_resource('GPIB5::28::INSTR')

instrumentA = rm.open_resource('GPIB5::28::INSTR')
instrumentB = rm.open_resource('GPIB5::29::INSTR')
print('Instrument A:',instrumentA.query('*IDN?'))
print('Instrument B:',instrumentB.query('*IDN?'))

print('Instrument A:', instrumentA.query('ATT?'))
instrumentA.write('ATT 3.12')
print('Instrument A:', instrumentA.query('ATT?'))
