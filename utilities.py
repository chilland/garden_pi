import os
import sqlite3
import time
import Adafruit_DHT
import SI1145.SI1145 as SI1145

def get_light():
    sensor = SI1145.SI1145()
    vis = sensor.readVisible()
    IR = sensor.readIR()
    UV = sensor.readUV()
    uvIndex = UV / 100.0
    return vis, IR, uvIndex

def get_DHT():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    temperature_f = 9.0/5.0*int(float(temperature))+32
    return(round(float(humidity),1), temperature_f)
    
def get_temp():
    res = os.popen('vcgencmd measure_temp').readline()
    raw_temp = res.replace("temp=","").replace("'C\n","")
    temp_c = int(float(raw_temp))
    temp_f = 9.0/5.0*temp_c+32
    return temp_f

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def log_temperature(DHT_hum, DHT_temp, vis, IR, UV, dbname):
    entries = [DHT_temp, DHT_hum, vis, IR, UV]

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO sensors VALUES(datetime('now'), {0}, {1}, {2}, {3}, {4})".format(entries[0], entries[1], entries[2], entries[3], entries[4]))

    conn.commit()
    conn.close()

def display_data(dbname):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM sensors"):
        print str(row[0])+"	"+str(row[1])

    conn.close()

def get_data(dbname, interval):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * from sensors")
    else:
        curs.execute("SELECT * from sensors WHERE timestamp>datetime('now','-%s hours')" % interval)
    rows = curs.fetchall()
    
    conn.close()
    return rows

def create_table(rows):
    chart_table = {}

    for row in rows:
        chart_table[row[0]] = row[1]

    return chart_table

def create_temp(rows):
    x_axis = ['x']
    y_axis = ['Temperature (F)']

    for row in rows:
        x_axis.append(str(row[0]))
        y_axis.append(float(row[1]))

    return x_axis, y_axis

def create_hum(rows):
    x_axis = ['x']
    y_axis = ['Humidity (%)']

    for row in rows:
        x_axis.append(str(row[0]))
        y_axis.append(float(row[2]))

    return x_axis, y_axis