import visa
import pyvisa


#rm = visa.ResourceManager()
rm = visa.ResourceManager('@py')
rm.list_resources()