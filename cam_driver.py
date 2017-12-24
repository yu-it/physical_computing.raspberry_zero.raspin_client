import raspin
import time
from multiprocessing import Process
import subprocess
import os

api = raspin.api("localhost", 3000)

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
    print("@kidou kanryou")

launch_process()

while True:
    mess = api.subscribe_control_message(pvid,120)
    if mess["ret"] == "to":
        print("timeout")
        continue
    if mess["message"] == available_mess_dir["message_name"]:
        if mess["arg"] == u"u":
            #driver.up()
            pass
        elif mess["arg"] == u"d":
            #driver.down()
            pass
        elif mess["arg"] == u"r":
            driver.right()
        elif mess["arg"] == u"l":
            driver.left()
    elif mess["message"] == available_mess_stop["message_name"]:
        driver.stop()
    elif mess["message"] == available_mess_kill["message_name"]:
        driver.stop()
        api.acknowledge(pvid, mess["req_id"], "1", [], [pvid])
        break
    api.acknowledge(pvid, mess["req_id"],0,[],[])


api.delete_provider(pvid)
