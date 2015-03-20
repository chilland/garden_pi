from flask import Blueprint, render_template, request, jsonify
from app import app
import utilities
import chartkick

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

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

@app.route('/sensors')
def sensors():
    dbname='/home/pi/Desktop/dashboard/sensorlog.db'
    interval='168'
    DHT_hum, DHT_temp = utilities.get_DHT()
    vis, IR, UV = utilities.get_light()
    rows = utilities.get_data(dbname, interval)
    temp_x, temp_y = utilities.create_temp(rows)
    hum_x, hum_y = utilities.create_hum(rows)
    return render_template('sensors.html', 
                            DHT_temp=round(DHT_temp,1),
                            DHT_hum=round(DHT_hum,1), 
                            vis=vis,
                            IR=IR,
                            UV=UV,
                            temp_x=temp_x,
			    temp_y=temp_y,
			    hum_x=hum_x,
                            hum_y=hum_y)