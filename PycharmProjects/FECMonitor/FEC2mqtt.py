#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


__app__ = "FEC2mqtt Adapter"
__VERSION__ = "0.8"
__DATE__ = "30.06.2016"
__author__ = "Markus Schiesser"
__contact__ = "Markus.Schiesser@swisscom.com"
__copyright__ = "Copyright (C) 2016 Markus Schiesser"
__license__ = 'GPL v3'

import sys
import csv
import dateutil.parser
from library.remoteConnect import WrapperRemote
from library.cfghandler import cfghandler
from library.mqttclient import *
from library.msgbus import *
from library.logging import log_adapter

class manager(msgbus):

    def __init__(self,cfgfile):
        self._cfgfile = cfgfile

        self._cfg_broker = None
        self._cfg_gerneral = None
        self._cfg_server = None
        self._cfg_link = None

    def readcfg(self):
        config = cfghandler()
     #   cfg = ConfigObj(self._cfgfile)
       # print('configfile',self._cfgfile)
        config.open(self._cfgfile)
        print(config.get())
        cfg = config.get()


        self._cfg_broker = cfg.get('BROKER')
        self._cfg_general = cfg.get('GENERAL')
        self._cfg_server = cfg.get('SERVER')
        self._cfg_link = cfg.get('LINK')
        self._cfg_data = cfg.get('DATA')

        print('GENERAL',self._cfg_general)
        print('BROKER',self._cfg_broker)
        print('SERVER',self._cfg_server)
        print('LINK',self._cfg_link)

    def start_logging(self):
        self._log_thread = log_adapter(self._cfg_general)
        self._log_thread.start()
     #   self.msgbus_publish('LOG','%s Start Logging Adapter')

    def getFileFromRemote(self):
        processList = {}
        result = {}
        dataStore ={}
        for key, value in self._cfg_server.items():
            dataStore[key] = {}
            dataStore[key]['PROCESS-ID']=(WrapperRemote(value))
            print(key,value)
            #processList[key]=(WrapperRemote(value))

        for key, value in self._cfg_server.items():
            result[key]={}
            print(key)
            processID = dataStore[key]['PROCESS-ID']
            processID.chdir(value.get('PATH'))
           # print(processID.filesinRemoteDir(value.get('PATH')))
            (fileName,fileDate)=(processID.fileinRemoteDirLatest(value.get('FILE_FILTER')))
            print(fileName,fileDate)
            dataStore[key]['FILEDATE']=fileDate
            dataStore[key]['FILENAME']=fileName
          #  processList[key]['FILENAME'].append(fileName)
         #   resultDict[key]['FILEDATE'].append(fileDate)
            print(dataStore)

        temp_timeStamp = 0
        latest = None
        for key, value in dataStore.items():
            timeStamp = value.get('FILEDATE')
            if temp_timeStamp < timeStamp:
                temp_timeStamp = timeStamp
                latest = key
        print('Result',latest,temp_timeStamp,value.get('FILENAME'))

        processID = dataStore[latest]['PROCESS-ID']
        processID.getFile(self._cfg_general['TEMPDIR'],dataStore[latest]['FILENAME'])

        return dataStore[latest]['FILENAME']

    def processData(self,datafile):
        if not os.path.exists(self._cfg_general['TEMPDIR']+'/'+ self._cfg_general['RESULTFILE']):
            print('Result file does not exist',self._cfg_general['TEMPDIR']+'/'+ self._cfg_general['RESULTFILE'])
            filename = self._cfg_general['TEMPDIR']+'/'+ datafile
            #print(filename)
            fp = open(filename,'rt')
            reader = csv.DictReader(fp,delimiter='\t')
            fieldnames = reader.fieldnames
            fp.close()


            wf = open(self._cfg_general['TEMPDIR']+'/'+ self._cfg_general['RESULTFILE'], 'wt')
            print("Feldnamen",fieldnames)
            writer = csv.DictWriter(wf,delimiter='\t', fieldnames=fieldnames)
            writer.writeheader()
            wf.close()
       #     file(filename, 'w').close()

        fp = open(self._cfg_general['TEMPDIR']+'/'+ datafile, 'rt')
        reader = csv.DictReader(fp,delimiter='\t')
        fieldnames = reader.fieldnames
        print('xxx',self._cfg_data['SRC'][0],self._cfg_data['SRC'][1],self._cfg_data['SRC'][2])
        wf = open(self._cfg_general['TEMPDIR']+'/'+ self._cfg_general['RESULTFILE'], 'wt')
     #   print("Feldnamen",fieldnames)
        writer = csv.DictWriter(wf,delimiter='\t', fieldnames=fieldnames)
        for row in reader:
            if (row['NEName']== self._cfg_data['SRC'][0]) & (row['ShelfID'] == self._cfg_data['SRC'][1]) & (row['BrdID']== self._cfg_data['SRC'][2]):
                for item in self._cfg_data['EVENT_NAME']:
                    if row['EventName'] == item:
                     #   print(row)
                        eventTime = row['EndTime']
                        print(eventTime)
                        print(dateutil.parser.parse(eventTime))
                        row['EndTime']=eventTime.split('+')[0]
                        writer.writerow(row)
              #  if (row['EventName'] == 'FEC_BEF_CORER_FLOAT'):
               # eventTime = row['EndTime']
       # for row in reader:
           #     print(row)





#    def remoteC

    def start_mqttbroker(self):
        self._mqttbroker = mqttbroker(self._cfg_broker)
        self._mqttbroker.start()
        return True

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """

    #    self.start_logging()
     #   self.msgbus_publish('LOG','%s Start mqtt2gpio adapter; Version: %s, %s '%('INFO', __VERSION__ ,__DATE__))
        self.readcfg()
        filename = self.getFileFromRemote()
        self.processData(filename)

       # self.start_logging()
       # self.start_mqttbroker()

      #  self.msgbus_publish('MQTT_TX','123456')
       # self.msgbus_subscribe('MQTT_RX',self.mqttif)
       # self.msgbus_subscribe('CAN_RX',self.canif)




if __name__ == "__main__":

    print ('main',len(sys.argv))
    if len(sys.argv) == 2:
        print('with commandline',sys.argv[1])
        cfgfile = sys.argv[1]
    else:
        print('read default file')
        cfgfile = 'FEC2mqtt.cfg'

    mgr_handle = manager(cfgfile)
    mgr_handle.run()