
import atexit
from api import instance as api
import time
import psutil
import raspin.physical_util as physical_util


def i2c(address_command,data):
    physical_util.i2c_write(address_command[0], [address_command[1],data[0], data[1]])

command_of_set_min = [[0x12, 0x01], [0x12, 0x03],[0x13, 0x01], [0x13, 0x03], [0x13, 0x05], [0x13, 0x07]]
command_of_set_max = [[0x12, 0x02], [0x12, 0x04],[0x13, 0x02], [0x13, 0x04], [0x13, 0x06], [0x13, 0x08]]
command_of_set_direction = [[0x12, 0x05], [0x12, 0x06],[0x13, 0x09], [0x13, 0x0a], [0x13, 0x0b], [0x13, 0x0c]]
command_of_set_speed = [[0x12, 0x07], [0x12, 0x08],[0x13, 0x0d], [0x13, 0x0e], [0x13, 0x0f], [0x13, 0x10]]
command_of_set_angle = [[0x12, 0x0d], [0x12, 0x0e],[0x13, 0x11], [0x13, 0x12], [0x13, 0x13], [0x13, 0x14]]

sholder_ud =0 
leg =1
sholder_lr =2
elbow = 4
def setup_ds939(num, speed=[0x10, 0x00]):
    min = [0x80, 0x01]
    max = [0xe8, 0x03]
    set(num, min, max, speed)
def setup_ly10(num,speed=[0x10, 0x00]):
    min = [0x10, 0x01]
    max = [0xbb, 0x03]
    set(num, min, max, speed)
def set(num, min,max,speed):
    i2c(command_of_set_min[num], min)
    i2c(command_of_set_max[num], max)
    i2c(command_of_set_speed[num], speed)


i2c([0x12,0x0b],[0xdd, 0x00])
setup_ds939(sholder_lr)
setup_ds939(sholder_ud)
setup_ds939(elbow)
setup_ly10(leg)

i2c(command_of_set_angle[sholder_lr], [0x80, 0x02])
i2c(command_of_set_angle[sholder_ud], [0x80, 0x02])
i2c(command_of_set_angle[elbow], [0x80, 0x02])
i2c(command_of_set_angle[leg], [0x80, 0x02])

process_name = "physical_controller"
wheel_move = "wheel"
sholder_move = "sholder"
sholder_elbow_move = "sholder_elbow"
elbow_move = "elbow"
leg_move = "leg"
arm_speed = "arm_speed"
wheel_speed = "wheel_speed"
#off_on = "off_on"

api.put_process(process_name, "Physical Controller")
#api.put_toggle_if(off_on,["off","on"], "Power", "physical_controller")

t_wheel_move = None
t_sholder_move = None
t_sholder_elbow_move = None
t_elbow_move = None
t_leg_move = None
t_arm_speed = None
t_wheel_speed = None


def receiver_off_on(data):
    print "speed:" + str(data)
#
"""
    global t_wheel_move
    global t_sholder_move
    global t_elbow_move
    global t_leg_move
    global t_speed
    if data == "on":
        api.put_arrow_if(wheel_move, "Wheel", "trbl", process_name)
        api.put_arrow_if(sholder_move, "Sholder", "trbl", process_name)
        api.put_arrow_if(elbow_move, "Elbow","tb",process_name)
        api.put_arrow_if(leg_move, "Leg","tb",process_name)
        api.put_toggle_if(wheel_speed,[" fast ","middle"," slow "], "Wheel Speed", "physical_controller")

        t_wheel_move = api.start_signal_observing(api.If_Arrows, wheel_move, receiver_wheel)
        t_sholder_move = api.start_signal_observing(api.If_Arrows, sholder_move, receiver_sholder)
        t_elbow_move = api.start_signal_observing(api.If_Arrows, elbow_move, receiver_elbow)
        t_elbow_move = api.start_signal_observing(api.If_Arrows, leg_move, receiver_leg)
        t_speed = api.start_signal_observing(api.If_Toggles, wheel_speed, receiver_speed)

    if data == "off":
        api.end_signal_observing(t_wheel_move)
        api.end_signal_observing(t_sholder_move)
        api.end_signal_observing(t_elbow_move)
        api.end_signal_observing(t_leg_move)
        api.end_signal_observing(t_speed)
        api.delete_if(api.If_Arrows, wheel_move, process_name)
        api.delete_if(api.If_Arrows, wheel_move, process_name)
        api.delete_if(api.If_Arrows, sholder_move, process_name)
        api.delete_if(api.If_Arrows, elbow_move, process_name)
        api.delete_if(api.If_Arrows, leg_move, process_name)
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
        physical_util.i2c_write(0x12, [0x09, 0x03, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x01, 0x00])
    elif data == "r":
        physical_util.i2c_write(0x12, [0x09, 0x01, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x03, 0x00])
    else:
        physical_util.i2c_write(0x12, [0x09, 0x02, 0x00])
        physical_util.i2c_write(0x12, [0x0a, 0x02, 0x00])




def receiver_sholder(data):
    print "sholder:" + str(data)
    if data == "t":
        i2c(command_of_set_direction[sholder_ud], [3,0])
    elif data == "b":
        i2c(command_of_set_direction[sholder_ud], [1,0])
    elif data == "l":
        i2c(command_of_set_direction[sholder_lr], [1,0])
    elif data == "r":
        i2c(command_of_set_direction[sholder_lr], [3,0])
    else:
        i2c(command_of_set_direction[sholder_ud], [2,0])
        i2c(command_of_set_direction[sholder_lr], [2,0])


def receiver_elbow(data):
    if data == "t":
        i2c(command_of_set_direction[elbow], [3,0])
    elif data == "b":
        i2c(command_of_set_direction[elbow], [1,0])
    else:
        i2c(command_of_set_direction[elbow], [2,0])

def receiver_leg(data):
    if data == "t":
        i2c(command_of_set_direction[leg], [3,0])
    elif data == "b":
        i2c(command_of_set_direction[leg], [1,0])
    else:
        i2c(command_of_set_direction[leg], [2,0])


def receiver_sholder_elbow(data):
    if data == "t":
        i2c(command_of_set_direction[sholder_ud], [3,0])
        i2c(command_of_set_direction[elbow], [1,0])
    elif data == "b":
        i2c(command_of_set_direction[sholder_ud], [1,0])
        i2c(command_of_set_direction[elbow], [3,0])
    else:
        i2c(command_of_set_direction[sholder_ud], [2,0])
        i2c(command_of_set_direction[elbow], [2,0])


def receiver_arm_speed(data):
    print "arm_speed:" + str(data)
    if data == " fast ":
        setup_ly10(sholder_ud, [0x5, 0x00])
        setup_ly10(elbow, [0x5, 0x00])
        setup_ds939(sholder_lr, [0x5, 0x00])
    elif data == "middle":
        setup_ly10(sholder_ud)
        setup_ly10(elbow)
        setup_ds939(sholder_lr)
    elif data == " slow ":
        setup_ly10(sholder_ud, [0x30, 0x00])
        setup_ly10(elbow, [0x30, 0x00])
        setup_ds939(sholder_lr, [0x30, 0x00])


def receiver_wheel_speed(data):
    print "wheel_speed:" + str(data)
    if data == " fast ":
        i2c([0x12, 0x0b], [0xff, 0x00])
    elif data == "middle":
        i2c([0x12, 0x0b], [0xdd, 0x00])
    elif data == " slow ":
        i2c([0x12, 0x0b], [0xcc, 0x00])


def shutdown_hook():
    api.delete_process(process_name)


#t = api.start_signal_observing(api.If_Toggles, off_on, receiver_off_on)

api.put_arrow_if(wheel_move, "Wheel", "trbl", process_name)
api.put_arrow_if(sholder_move, "Sholder", "trbl", process_name)
api.put_arrow_if(elbow_move, "Elbow", "tb", process_name)
api.put_arrow_if(leg_move, "Leg", "tb", process_name)
api.put_arrow_if(sholder_elbow_move, "Sholder And Elbow", "tb", process_name)

api.put_toggle_if(arm_speed, [" fast ", "middle", " slow "], "Arm Speed", "physical_controller")
api.put_toggle_if(wheel_speed, [" fast ", "middle", " slow "], "Wheel Speed", "physical_controller")

t_wheel_move = api.start_signal_observing(api.If_Arrows, wheel_move, receiver_wheel)
t_sholder_move = api.start_signal_observing(api.If_Arrows, sholder_move, receiver_sholder)
t_elbow_move = api.start_signal_observing(api.If_Arrows, elbow_move, receiver_elbow)
t_leg_move = api.start_signal_observing(api.If_Arrows, leg_move, receiver_leg)
t_arm_speed = api.start_signal_observing(api.If_Toggles, arm_speed, receiver_arm_speed)
t_wheel_speed = api.start_signal_observing(api.If_Toggles, wheel_speed, receiver_wheel_speed)
t_sholder_elbow_move = api.start_signal_observing(api.If_Arrows, sholder_elbow_move, receiver_sholder_elbow)

atexit.register(shutdown_hook)


t_wheel_move.join()
