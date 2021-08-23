from time import sleep
from pySX127x.SX127x.LoRa import *
from pySX127x.SX127x.board_config import BOARD

class MyLoRa(LoRa):
	def __init__(self, verbose=False):
		super(MyLoRa, self).__init__(verbose)
		self.set_mode(MODE.SLEEP)
		self.set_freq(915.0)
		self.set_dio_mapping([0] * 6)

	def start(self):
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)
		while (True):
			sleep(.5)
			rssi_value = self.get_rssi_value()
			status     = self.get_modem_status()
			sys.stdout.flush()

	def on_rx_done(self):
		print("\nReceived: ")
		self.clear_irq_flags(RxDone=1)
		payload = self.read_payload(nocheck=True)
		print(bytes(payload).decode("utf-8",'ignore'))
		self.set_mode(MODE.SLEEP)
		self.reset_ptr_rx()
		self.set_mode(MODE.RXCONT)

BOARD.setup()

lora = MyLoRa()

print(lora.get_version())
print(lora.get_freq())

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    
lora.set_mode(MODE.SLEEP)
BOARD.teardown()


