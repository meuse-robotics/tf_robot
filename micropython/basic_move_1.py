from machine import Pin, PWM, I2C
import time

PCA9685_ADDR = 0x40
FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 4096.0 # 周期内の分割数
MIN_PULSE = 400  # 最小パルス幅　msec at 0°
MAX_PULSE = 2400  # 最大パルス幅  msec at 180°
MAX_DUTY_G = 65025.0 # 周期内の分割数
MIN_PULSE_G = 600  # 最小パルス幅　msec at 0°
MAX_PULSE_G = 2400  # 最大パルス幅  msec at 180°

i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=100000)
data = bytearray(4)
servos = [PWM(Pin(6)),PWM(Pin(7)),PWM(Pin(8)),PWM(Pin(9)),PWM(Pin(10))]
angles = [[45,135,90, 90,90,90,140,90, 90,40,90,90,90, 90,45,135, 90,90,170,90,90],
          [90,135,90, 90,90,90,140,90, 90,40,90,90,90, 90,45,135, 90,90,170,90,90]]
correct = [0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0,0,0]
keyFrame = 0

def reg_write(i2c, addr, reg, data, length):
    msg = bytearray()
    for i in range(length):
        msg.append(data[i])
    i2c.writeto_mem(addr, reg, msg)
    
data[0] = 0b00010001
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)
data[0] = 121
reg_write(i2c, PCA9685_ADDR, 0xFE, data, 1)
data[0] = 0b00100001
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)

while True:
    for i in range(16):
        if angles[keyFrame][i] < 0:
            width = 0
        else:
            width = MAX_DUTY\
            * (MIN_PULSE + (MAX_PULSE - MIN_PULSE) / 180 * (angles[keyFrame][i] + correct[i]))\
            * FREQ / 1000000
        data[0] = 0x00
        data[1] = 0x00
        data[2] = 0x00ff & int(width)
        data[3] = (0xff00 & int(width))>>8
        reg_write(i2c, PCA9685_ADDR, 0x06+i*4, data, 4)
        
    for i in range(16,21):
        servos[i-16].freq(50)
        if angles[keyFrame][i]<0:
            servos[i-16].duty_u16(0)
        else:
            width = MAX_DUTY_G\
            * (MIN_PULSE_G + (MAX_PULSE_G - MIN_PULSE_G) / 180 * (angles[keyFrame][i] + correct[i]))\
            * FREQ / 1000000
            servos[i-16].duty_u16(int(width))
    
    keyFrame+=1
    if keyFrame > 1:
        keyFrame = 0
    time.sleep(1)
