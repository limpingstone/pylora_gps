PACKET_SIZE = 255

WRITE_MASK  =0x80

REG_FIFO = 0x00
REG_OP_MODE = 0x01
MODE_LORA  = 0x80
MODE_SLEEP = 0x0
MODE_STDBY = 0x1
MODE_FSTX  = 0x2
MODE_TX    = 0x3
MODE_FSRX  = 0x4
MODE_RXCON = 0x5
MODE_CAD   = 0x7

REG_FR_MSB = 0x6
REG_FR_MID = 0x7
REG_FR_LSB = 0x8
REG_PA_CONFIG = 0x9
REG_PA_RAMP = 0xA
REG_OCP = 0xB
REG_LNA  = 0xC
REG_FIFO_ADDR_PTR  = 0xD
REG_FIFO_TX_BASE_ADDR  = 0xE
REG_FIFO_RX_BASE_ADDR  = 0xF
REG_FIFO_RX_CUR_ADDR  = 0x10

REG_IRQFLAGS  = 0x12
MASK_IRQFLAGS_RXTIMEOUT  = 0b10000000
MASK_IRQFLAGS_RXDONE  = 0b01000000
MASK_IRQFLAGS_PAYLOADCRCERROR  = 0b00100000
MASK_IRQFLAGS_VALIDHEADER  = 0b00010000
MASK_IRQFLAGS_TXDONE  = 0b00001000
MASK_IRQFLAGS_CADDONE  = 0b00000100
MASK_IRQFLAGS_FHSSCHANGECHANNEL  = 0b00000010
MASK_IRQFLAGS_CADDETECTED  = 0b00000001

REG_MODEMSTAT  = 0x18
MASK_MODEMSTAT_CLEAR  = 0b00010000
MASK_MODEMSTAT_VALIDHEADER  = 0b00001000
MASK_MODEMSTAT_RXONGOING  = 0b00000100
MASK_MODEMSTAT_SYNCHRYONIZED  = 0b00000010
MASK_MODEMSTAT_DETECTED = 0b00000001

REG_MODEM_CONFIG_1  = 0x1D
REG_MODEM_CONFIG_2  = 0x1E
REG_SYMB_TIMEOUT    = 0x1F
REG_PREAMBLE_MSB    = 0x20
REG_PREAMBLE_LSB    = 0x21
REG_PAYLOAD_LENGTH  = 0x22
REG_MAX_PAYLOAD_LENGTH  = 0x23
REG_HOP_PERIOD = 0x24

REG_RSSI_WIDEBAND = 0x2C

REG_DETECT_OPTIMIZE = 0x31

REG_DETECTION_THRESHOLD = 0x37

REG_DIO_MAPPING_1 = 0x40
REG_DIO_MAPPING_2 = 0x41
REG_PA_DAC = 0x4D
FXOSC = 32000000

#define FREQ_TO_REG(in_freq) ((uint32_t)(( ((uint64_t)in_freq) << 19) / FXOSC))
def freq_to_reg(in_freq):
    return (in_freq << 19) // FXOSC

#define REG_TO_FREQ(in_reg) ((uint32_t)((FXOSC*in_reg) >> 19))
def reg_to_freq(in_reg):
    return (FXOSC * in_reg) >> 19

DEFAULT_MODEM_CONFIG = [
    # Configure PA_BOOST with max power
    (REG_PA_CONFIG, 0x8f),

    # Enable overload current protection with max trim
    (REG_OCP, 0x3f),

    # Set RegPaDac to 0x87 (requried for SF=6)
    (REG_PA_DAC, 0x87),

    # Set the FIFO RX/TX pointers to 0
    (REG_FIFO_TX_BASE_ADDR, 0x00),
    (REG_FIFO_RX_BASE_ADDR, 0x00),

    # Set RegModemConfig1 as follows:
    # Bw = 0b1001 (500kHz)
    # CodingRate = 0b001 (4/5)
    # ImplicitHeader = 1
    (REG_MODEM_CONFIG_1, 0x93),

    # Set RegModemConfig2 as follows:
    # SpreadingFactor = 6
    # TxContinuousMode = 0
    # RxPayloadCrcOn = 1
    (REG_MODEM_CONFIG_2, 0x64),

    # Set preamble length to 8
    (REG_PREAMBLE_MSB, 0x00),
    (REG_PREAMBLE_LSB, 0x08),

    # Set payload length and max length to 255
    #(REG_PAYLOAD_LENGTH, 0x0f),
    #(REG_MAX_PAYLOAD_LENGTH, 0x0f),

    # Disable frequency hopping
    (REG_HOP_PERIOD, 0x00),

    # Set DetectionThreshold to 0xC (for SF = 6)
    (REG_DETECTION_THRESHOLD, 0x0c),

    # Set DetectionOptimize to 0x5 (for SF = 6)
    (REG_DETECT_OPTIMIZE, 0x05),

    # Set the frequency to 915MHz
    # We can use FREQ_TO_REG() here because it is declared as `constexpr`
    # and can therefore be evaluated at compile-time
    (REG_FR_MSB, (freq_to_reg(915000000) >> 16) & 0b11111111),
    (REG_FR_MID, (freq_to_reg(915000000) >> 8) & 0b11111111),
    (REG_FR_LSB, freq_to_reg(915000000) & 0b11111111),
]

