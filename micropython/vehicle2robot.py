from machine import Pin, PWM, I2C, Timer

PCA9685_ADDR = 0x40
FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 4096.0 # 周期内の分割数
MIN_PULSE = 400  # 最小パルス幅　msec at 0°
MAX_PULSE = 2400  # 最大パルス幅  msec at 180°
MAX_DUTY_G = 65025.0 # 周期内の分割数
MIN_PULSE_G = 600  # 最小パルス幅　msec at 0°
MAX_PULSE_G = 2400  # 最大パルス幅  msec at 180°
TIM_FREQ = 30

i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=100000)
data = bytearray(4)
servos = [PWM(Pin(6)),PWM(Pin(7)),PWM(Pin(8)),PWM(Pin(9)),PWM(Pin(10))]
angles = [
    [177, 90, 90,  90, 45,175,175, 90,  90,  5,  5,135, 90,  90, 90,  3, 90,90,77,90,90, 30],
    [177, 90, 90,  90, 45,175,175, 90,  90,  5,  5,135, 90,  90, 90,  3, 90,90,77,90,90,100],
    [ 25, 90,150,  90, 45,175,175, 90,  90,  5,  5,135, 90,  30, 90,155, 90,90,77,90,90, 30],
    [  5, 85,155,  90, 45, 45,175, 90,  90,  5,135,135, 90,  25, 95,175, 90,90,77,90,90, 30],
    [  5, 85,155,  90,160,160,175, 90,  90,  5, 20, 20, 90,  25, 95,175, 90,90,77,90,90, 30],
    [  5, 95,175,  90,150,170,175, 90,  90,  5, 10, 30, 90,   5, 85,175, 90,90,77,90,90, 30],
    [ 45,135, 90,  90, 90, 90,140, 90,  90, 40, 90, 90, 90,  90, 45,135, 90,90,177,90,90, 30],
    [ 45,135, 90,  90, 90, 90,140, 90,  90, 40, 90, 90, 90,  90, 45,135, 90,90,177,90,90, 30]
    ]

    
correct = [0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0,0,0]
keyFrame = 0
nextKeyFrame = 1
divCount = 0

servoFlag = False
tim = Timer()

def tick(timer):
    global servoFlag
    servoFlag = True
    
tim.init(freq=TIM_FREQ, mode=Timer.PERIODIC, callback=tick)

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

for i in range(5):
    servos[i].freq(50)

while True:
    if servoFlag == True:
        servoFlag = False
        
        divCount+=1
        if divCount > angles[nextKeyFrame][21]:
            divCount = 0
            keyFrame = nextKeyFrame
            nextKeyFrame+=1
            if nextKeyFrame > 7:
                nextKeyFrame = 6
        for i in range(16):
            if angles[nextKeyFrame][i] < 0:
                width = 0
            else:
                angle = angles[keyFrame][i] + (angles[nextKeyFrame][i] - angles[keyFrame][i]) * divCount / angles[nextKeyFrame][21] + correct[i]
                width = MAX_DUTY\
            * (MIN_PULSE + (MAX_PULSE - MIN_PULSE) / 180 * angle)\
            * FREQ / 1000000
            data[0] = 0x00
            data[1] = 0x00
            data[2] = 0x00ff & int(width)
            data[3] = (0xff00 & int(width))>>8
            reg_write(i2c, PCA9685_ADDR, 0x06+i*4, data, 4)
            
        for i in range(16,21):
                        
            if angles[keyFrame][i]<0:
                servos[i-16].duty_u16(0)
            else:
                angle = angles[keyFrame][i] + (angles[nextKeyFrame][i] - angles[keyFrame][i]) * divCount / angles[nextKeyFrame][21] + correct[i]
                width = MAX_DUTY_G\
            * (MIN_PULSE_G + (MAX_PULSE_G - MIN_PULSE_G) / 180 * angle)\
            * FREQ / 1000000
                servos[i-16].duty_u16(int(width))
    
        
