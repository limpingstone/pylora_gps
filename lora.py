import time
import sys
import RPi.GPIO as GPIO
import spidev
import lora_reg as regs
import threading

class LoRa:
    DIO0 = 4
    RST  = 22
    CS   = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup (LoRa.DIO0, GPIO.IN) 
        GPIO.setup (LoRa.RST, GPIO.OUT) 
        GPIO.output(LoRa.RST, 0)
        time.sleep(0.01)
        GPIO.output(LoRa.RST, 1)

        self.spi = spidev.SpiDev()
        self.spi.open(0, LoRa.CS)
        self.spi.max_speed_hz = 1000000

        self.irq_seen = False
<<<<<<< HEAD
        self.irq_data = None
=======
>>>>>>> cb36340 (While loop)
        self.irq_cv = threading.Condition()
        GPIO.add_event_detect(LoRa.DIO0, GPIO.RISING, callback=self.isr)

    
        self.write_reg(regs.REG_OP_MODE, regs.MODE_LORA | regs.MODE_SLEEP)
        val = self.read_reg(regs.REG_OP_MODE)

        if (val != regs.MODE_LORA or val != regs.MODE_LORA):
            raise Exception('Failed to load LoRa in sleep mode!')

        self.write_reg(regs.REG_PAYLOAD_LENGTH, regs.PACKET_SIZE)
        val = self.read_reg(regs.REG_PAYLOAD_LENGTH)

        if (val != regs.PACKET_SIZE):
            raise Exception('Failed to set payload size!')

        self.write_reg(regs.REG_MAX_PAYLOAD_LENGTH, regs.PACKET_SIZE)
        val = self.read_reg(regs.REG_MAX_PAYLOAD_LENGTH)

        if (val != regs.PACKET_SIZE):
            raise Exception('Failed to set payload size!')

        for pair in regs.DEFAULT_MODEM_CONFIG:
            self.write_reg(pair[0], pair[1])
            val = self.read_reg(pair[0])

            if (val != pair[1]):
                raise Exception('Failed to write to register!')

    def isr(self, channel): 
        # Read irq_data register
        sys.stderr.write("ISR!\n")
        self.irq_data = self.read_reg(regs.REG_IRQFLAGS)

        #if (self.irq_data != regs.MASK_IRQFLAGS_RXDONE | regs.MASK_IRQFLAGS_VALIDHEADER):
        #    sys.stderr.write("Bad data!\n")
        #    sys.stderr.write(bin(self.irq_data) + '\n')

        # Clear IRQ flag. Needs to be done twice for some reason (hw errata?)
        self.write_reg(regs.REG_IRQFLAGS, 0xFF)
        self.write_reg(regs.REG_IRQFLAGS, 0xFF)

        self.irq_seen = True

        with self.irq_cv: 
            self.irq_cv.notify()

    def write_reg(self, reg, val):
        self.spi.xfer([reg | regs.WRITE_MASK, val])

    def read_reg(self, reg):
        return self.spi.xfer([reg, 0])[1]

    def listen(self):
        self.write_reg(regs.REG_DIO_MAPPING_1, 0x00)
        self.write_reg(regs.REG_OP_MODE, regs.MODE_LORA | regs.MODE_RXCON)

        while (self.irq_seen == False):
            with self.irq_cv: 
                if (self.irq_cv.wait(timeout = 1) == False):
                    return False

        self.irq_seen = False

        return True

    def transmit(self):
        self.write_reg(regs.REG_DIO_MAPPING_1, 0x40)
        self.write_reg(regs.REG_OP_MODE, regs.MODE_LORA | regs.MODE_TX)

        while (self.irq_seen == False):
            with self.irq_cv: 
                if (self.irq_cv.wait(timeout = 1) == False):
                    return False

        self.irq_seen = False

        return self.irq_data == regs.MASK_IRQFLAGS_TXDONE

    def write_fifo(self, buf, offset):
        self.write_reg(regs.REG_FIFO_ADDR_PTR, offset)
        self.spi.xfer([regs.REG_FIFO | regs.WRITE_MASK] + buf)

    def read_fifo(self):
        offset = self.read_reg(regs.REG_FIFO_RX_CUR_ADDR)
        
        self.write_reg(regs.REG_FIFO_ADDR_PTR, offset)
        return self.spi.xfer([regs.REG_FIFO] + [0 for _ in range(255)])[1:]

lora = LoRa()

while True:
    if (not lora.listen()):
        sys.stderr.write('Timeout reached!\n')
    buff = lora.read_fifo()
    #for char in buff:
    #    print(ord(char), end='')
    
    sys.stderr.write(bytes(buff).hex())
    sys.stderr.write('\n')
    time.sleep(1)

GPIO.cleanup()

