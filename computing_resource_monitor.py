import atexit
from api import instance as api
import time
import psutil

def get_cpu_usage():
    return psutil.cpu_percent()

def get_memory_usage():
    return psutil.virtual_memory().percent

def shutdown_hook():
    api.delete_if(api.If_Numbers, cpu_usage, process_name)
    api.delete_if(api.If_Numbers, mem_usage, process_name)
    api.delete_process(process_name)

process_name = "computing_resource"
cpu_usage = "cpu_usage"
mem_usage = "memory_usage"
api.put_process(process_name, "Computing Resource")
api.put_number_if(cpu_usage,"CPU Usage",1,"%",process_name)
api.put_number_if(mem_usage,"Memory Usage",1,"%",process_name)

atexit.register(shutdown_hook)

while True:
    api.put_data(api.If_Numbers, cpu_usage, get_cpu_usage(), process_name)
    api.put_data(api.If_Numbers, mem_usage, get_memory_usage(), process_name)
    time.sleep(2)


