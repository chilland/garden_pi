#!/usr/bin/env python

import os
import sqlite3
import time
import utilities

dbname='/home/pi/Desktop/garden_pi/sensorlog.db'

def main():
    DHT_hum, DHT_temp = utilities.get_DHT()
    vis, IR, UV = utilities.get_light()
    utilities.log_temperature(DHT_hum, DHT_temp, vis, IR, UV, dbname)

if __name__=="__main__":
    main()