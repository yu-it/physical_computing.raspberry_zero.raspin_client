from raspin.raspin import api


instance = api("localhost", 3000)
machines = instance.machines()
if len(machines) == 0:
 instance.put_machine()
 
