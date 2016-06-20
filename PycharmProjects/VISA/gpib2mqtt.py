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


__app__ = "gpib2mqtt Adapter"
__VERSION__ = "0.8"
__DATE__ = "16.03.2016"
__author__ = "Markus Schiesser"
__contact__ = "Markus.Schiesser@swisscom.com"
__copyright__ = "Copyright (C) 2015 Markus Schiesser"
__license__ = 'GPL v3'

import sys

from library.cfghandler import cfghandler
from library.mqttclient import *
from library.msgbus import *
from library.logging import log_adapter

class manager(msgbus):

    def __init__(self,cfgfile):
        self._cfgfile = cfgfile

        self._cfg_broker = None
        self._cfg_gerneral = None
        self._cfg_instrument = None

    def readcfg(self):
        cfg = cfghandler()
     #   cfg = ConfigObj(self._cfgfile)
        cfg.open(self._cfgfile)

        self._cfg_broker = cfg.value('BROKER')
        self._cfg_general = cfg.value('GENERAL')
        self._cfg_instr = cfg.value('INSTRUMENT')

        print('GENERAL',self._cfg_general)
        print('BROKER',self._cfg_broker)
        print('INSTRUMENT',self._cfg_instr)

    def start_logging(self):
        self._log_thread = log_adapter(self._cfg_general)
        self._log_thread.start()
     #   self.msgbus_publish('LOG','%s Start Logging Adapter')

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
        self.start_logging()
        self.start_mqttbroker()

      #  self.msgbus_publish('MQTT_TX','123456')
        self.msgbus_subscribe('MQTT_RX',self.mqttif)
        self.msgbus_subscribe('CAN_RX',self.canif)




if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        print('no commandline ')
        cfgfile = sys.argv[1]
    else:
        print('read default file')
        cfgfile = 'gpib2mqtt.cfg'

    mgr_handle = manager(cfgfile)
    mgr_handle.run()