import time
import RPi.GPIO as GPIO
import spidev
import lora_reg as regs

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
        self.spi.max_speed_hz = 5000000

        self.irq_seen = True
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

    def isr(self): 
        # Read irq_data register
        self.irq_data = self.read_reg(regs.REG_IRQFLAGS)

        # Clear IRQ flag. Needs to be done twice for some reason (hw errata?)
        self.write_reg(regs.REG_IRQFLAGS, 0xFF)
        self.write_reg(regs.REG_IRQFLAGS, 0xFF)

        self.irq_seen = False

    def write_reg(self, reg, val):
        self.spi.xfer([reg | regs.WRITE_MASK, val])

    def read_reg(self, reg):
        return self.spi.xfer([reg, 0])[1]

    def listen():
        self.write_reg(regs.REG_DIO_MAPPING_1, 0x00)
        self.write_reg(regs.LORA_REG_OP_MODE, regs.MODE_LORA | regs.MODE_RXCON)

        self.irq_seen = False

    def transmit():
        self.write_reg(regs.REG_DIO_MAPPING_1, 0x40)
        self.write_reg(regs.LORA_REG_OP_MODE, regs.MODE_LORA | regs.MODE_TX)

        reg0 = read.reg(regs.LORA_REG_OP_MODE)
        reg1 = read.reg(0x12)

        while (self.irq_seen == True):
            pass

        ret = self.irq_data == MASK_IRQFLAGS_TXDONE
        self.irq_seen = True

        return ret


lora = LoRa()

GPIO.cleanup()

