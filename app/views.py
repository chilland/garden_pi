from flask import render_template, request, jsonify
from app import app
import utilities

@app.route('/')
@app.route('/diagnostics')
def diagnostics():
    CPU_temp = str(utilities.get_temp())
    CPU_usage = utilities.getCPUuse()

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = utilities.getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
    RAM_perc = round(RAM_used/RAM_total*100,1)

    # Disk information
    DISK_stats = utilities.getDiskSpace()
    DISK_perc = DISK_stats[3][0:2]

    return render_template('diagnostics.html', 
                            CPU_temp=CPU_temp,
                            CPU_usage=CPU_usage,
                            RAM_perc=RAM_perc,
                            DISK_perc=DISK_perc)

@app.route('/temp-hum')
def temp_hum():
    dbname='/home/pi/Desktop/garden_pi/sensorlog.db'
    interval='168'
    DHT_hum, DHT_temp = utilities.get_DHT()
    rows = utilities.get_data(dbname, interval)
    temp_x, temp_y = utilities.create_temp(rows)
    hum_x, hum_y = utilities.create_hum(rows)
    return render_template('temp-hum.html', 
                            DHT_temp=round(DHT_temp,1),
                            DHT_hum=round(DHT_hum,1), 
                            temp_x=temp_x,
			    temp_y=temp_y,
			    hum_x=hum_x,
                            hum_y=hum_y)

@app.route('/light')
def light():
   dbname='/home/pi/Desktop/garden_pi/sensorlog.db'
   interval='168'
   rows = utilities.get_data(dbname, interval)
   vis, IR, UV = utilities.get_light()
   vis_x, vis_y = utilities.create_vis(rows)
   ir_x, ir_y = utilities.create_ir(rows)
   uv_x, uv_y = utilities.create_uv(rows) 
   return render_template('light.html', 
                            vis=vis,
                            IR=IR,
                            UV=UV,
                            ir_x=ir_x,
                            ir_y=ir_y,
                            vis_y=vis_y,
                            uv_x=uv_x,
                            uv_y=uv_y)