import atexit
from api import instance as api
import time
import raspin.physical_util as physical_util

import os
import subprocess

process_name = "Sensor"

api.put_process(process_name)
api.put_number_if("Source_Voltage", "Source Voltage", 1, "V", process_name)
api.put_video_if("Camera", "Camera", process_name)

def shutdown_hook():
    api.delete_if(api.If_Numbers, "Source_Voltage", process_name)
    api.delete_if(api.If_Video, "Camera", process_name)
    api.delete_process(process_name)

atexit.register(shutdown_hook)

while True:
    time.sleep(2)
    api.put_data(api.If_Numbers, "Source_Voltage",physical_util.read_analog_volt(7,0.25))

