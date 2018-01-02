
import atexit
from api import instance as api
import time
import psutil
import raspin.physical_util as physical_util

physical_util.i2c_write(0x12,[0x0b, 0xdd, 0x00])

process_name = "physical_controller"
wheel_move = "wheel"
sholder_move = "sholder"
elbow_move = "elbow"
wheel_speed = "wheel_speed"
off_on = "off_on"

api.put_process(process_name, "Physical Controller")
api.put_toggle_if(off_on,["off","on"], "Power", "physical_controller")

t_wheel_move = None
t_sholder_move = None
t_elbow_move = None
t_speed = None


def receiver_off_on(data):
    print "speed:" + str(data)
#
"""
    global t_wheel_move
    global t_sholder_move
    global t_elbow_move
    global t_speed
    if data == "on":
        api.put_arrow_if(wheel_move, "Wheel", "trbl", process_name)
        api.put_arrow_if(sholder_move, "Sholder", "trbl", process_name)
        api.put_arrow_if(elbow_move, "Elbow","tb",process_name)
        api.put_toggle_if(wheel_speed,[" fast ","middle"," slow "], "Wheel Speed", "physical_controller")

        t_wheel_move = api.start_signal_observing(api.If_Arrows, wheel_move, receiver_wheel)
        t_sholder_move = api.start_signal_observing(api.If_Arrows, sholder_move, receiver_sholder)
        t_elbow_move = api.start_signal_observing(api.If_Arrows, elbow_move, receiver_elbow)
        t_speed = api.start_signal_observing(api.If_Toggles, wheel_speed, receiver_speed)

    if data == "off":
        api.end_signal_observing(t_wheel_move)
        api.end_signal_observing(t_sholder_move)
        api.end_signal_observing(t_elbow_move)
        api.end_signal_observing(t_speed)
        api.delete_if(api.If_Arrows, wheel_move, process_name)
        api.delete_if(api.If_Arrows, wheel_move, process_name)
        api.delete_if(api.If_Arrows, sholder_move, process_name)
        api.delete_if(api.If_Arrows, elbow_move, process_name)
        api.delete_if(api.If_Toggles, wheel_speed, process_name)
"""


def receiver_wheel(data):
    print "wheel:" + str(data)
    if data == "t":
        physical_util.i2c_write(0x12, [0x09, 0x01, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x01, 0x00])
    elif data == "b":
        physical_util.i2c_write(0x12, [0x09, 0x03, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x03, 0x00])
    elif data == "l":
        physical_util.i2c_write(0x12, [0x09, 0x01, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x03, 0x00])
    elif data == "r":
        physical_util.i2c_write(0x12, [0x09, 0x03, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x01, 0x00])
    else:
        physical_util.i2c_write(0x12, [0x09, 0x02, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x02, 0x00])




def receiver_sholder(data):
    print "sholder:" + str(data)
def receiver_elbow(data):
    print "elbow:" + str(data)
def receiver_speed(data):
    print "speed:" + str(data)
def shutdown_hook():
    api.delete_process(process_name)


t = api.start_signal_observing(api.If_Toggles, off_on, receiver_off_on)

api.put_arrow_if(wheel_move, "Wheel", "trbl", process_name)
api.put_arrow_if(sholder_move, "Sholder", "trbl", process_name)
api.put_arrow_if(elbow_move, "Elbow", "tb", process_name)
api.put_toggle_if(wheel_speed, [" fast ", "middle", " slow "], "Wheel Speed", "physical_controller")

t_wheel_move = api.start_signal_observing(api.If_Arrows, wheel_move, receiver_wheel)
t_sholder_move = api.start_signal_observing(api.If_Arrows, sholder_move, receiver_sholder)
t_elbow_move = api.start_signal_observing(api.If_Arrows, elbow_move, receiver_elbow)
t_speed = api.start_signal_observing(api.If_Toggles, wheel_speed, receiver_speed)

atexit.register(shutdown_hook)


t.join()
