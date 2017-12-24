import atexit
from api import instance as api
import time
import raspin.physical_util as physical_util

import os
import subprocess

process_name = "Sensor"
def launch_process():
    global p
    cmd = ["./mjpg_streamer"
        , "-i"
        , './input_raspicam.so -fps 10 -x 320 -y 240'
        , "-o"
        , './output_http.so -w ./www -p 8080']

    p = subprocess.Popen(cmd, cwd="/home/pi/bin/programs/camera_inst/mjpg-streamer/mjpg-streamer-experimental")
    # proc.communicate()
    time.sleep(3)

if os.name <> "nt":
    launch_process()

api.put_process(process_name)
api.put_video_if("Camera","Camera",process_name)
api.put_number_if("Source_Voltage", "Source Voltage", 1, "V", process_name)

def shutdown_hook():
    api.delete_if(api.If_Video, "Camera", process_name)
    api.delete_if(api.If_Numbers, "Source_Voltage", process_name)
    api.delete_process(process_name)

atexit.register(shutdown_hook)

while True:
    time.sleep(2)

    api.put_data(api.If_Numbers, "Source_Voltage",physical_util.read_analog_volt(7,0.25))

