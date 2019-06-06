#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import *
from SnipsClients import SnipsMPU

VERSION = '0.3.0'

CONFIG_INI = 'config.ini'
I18N_DIR = 'assets/i18n'

MQTT_ADDR_HOST = "localhost"
MQTT_ADDR_PORT = "1883"
MQTT_ADDR = "{}:{}".format(MQTT_ADDR_HOST, MQTT_ADDR_PORT)
SITE_ID = "default"
TEMP_UNIT = "celsius"
LOCALE = "fr_FR"

i18n = SnipsI18n(I18N_DIR, LOCALE)
client = SnipsMPU.SnipsMPU(i18n, MQTT_ADDR, SITE_ID)

if __name__ == "__main__":
    try:
        client.start_block()

    except KeyboardInterrupt:
        print("stop")
