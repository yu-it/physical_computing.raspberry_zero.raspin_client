from raspin.raspin import api


instance = api("localhost", 3000)
machines = instance.machines()

instance.put_machine()
