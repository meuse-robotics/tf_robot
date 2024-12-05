from machine import Pin, PWM, I2C, Timer
import motion_data

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
angles = []
correct = [0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0, 0,0,0,0,0]

machineMode = 'VEHICLE_MODE'
actionState = 'STOP'
maxRows = 0
keyFrame = 0
nextKeyFrame = 1
divCount = 0

def reg_write(i2c, addr, reg, data, length):
    msg = bytearray()
    for i in range(length):
        msg.append(data[i])
    i2c.writeto_mem(addr, reg, msg)
    
def set_action(c):
    global divCount
    global keyFrame
    global nextKeyFrame
    global angles
    global maxRows
    global actionState
    print(c)
    if machineMode == 'VEHICLE_MODE':
        if c == 'r':
            actionState = 'VEHICLE2ROBOT'
            angles.clear()
            angles = motion_data.vehicle2robot.copy()
            maxRows = len(motion_data.vehicle2robot)
        elif c == 'w':
            actionState = 'FWRD'
            angles.clear()
            angles = motion_data.fwrd.copy()
            set_angles(machineMode, actionState)
        elif c == 'q':
            actionState = 'LEFT'
            angles.clear()
            angles = motion_data.left.copy()
            set_angles(machineMode, actionState)
        elif c == 'e':
            actionState = 'RIGHT'
            angles.clear()
            angles = motion_data.right.copy()
            set_angles(machineMode, actionState)
        elif c == 'x':
            actionState = 'BWRD'
            angles.clear()
            angles = motion_data.bwrd.copy()
            set_angles(machineMode, actionState)
        elif c == 's':
            actionState = 'STOP'
            angles.clear()
            angles = motion_data.vehicle.copy()
            set_angles(machineMode, actionState)
    elif machineMode == 'ROBOT_MODE':
        if c == 'v':
            actionState = 'ROBOT2VEHICLE'
            angles.clear()
            angles = motion_data.robot2vehicle.copy()
            maxRows = len(motion_data.robot2vehicle)
        elif c == 'w':
            actionState = 'WALK'
            angles.clear()
            angles = motion_data.walk.copy()
            maxRows = len(motion_data.walk)
        elif c == 's':
            actionState = 'STOP'
            angles.clear()
            angles = motion_data.robot.copy()
            set_angles(machineMode, actionState)
    divCount = 0
    keyFrame = 0
    nextKeyFrame = 1

def set_angles(mode, state):
    global keyFrame
    global nextKeyFrame
    global angles
    global servos
    if state != 'ROBOT2VEHICLE' and state != 'VEHICLE2ROBOT' and state != 'WALK':
        keyFrame = 0
        nextKeyFrame = 0
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
            width = 0
        else:
            angle = angles[keyFrame][i] + (angles[nextKeyFrame][i] - angles[keyFrame][i]) * divCount / angles[nextKeyFrame][21] + correct[i]
            width = MAX_DUTY_G\
            * (MIN_PULSE_G + (MAX_PULSE_G - MIN_PULSE_G) / 180 * angle)\
            * FREQ / 1000000
        servos[i-16].duty_u16(int(width))

data[0] = 0b00010001
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)
data[0] = 121
reg_write(i2c, PCA9685_ADDR, 0xFE, data, 1)
data[0] = 0b00100001
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)

for i in range(5):
    servos[i].freq(50)

machineMode = 'VEHICLE_MODE'
actionState = 'STOP'
angles = motion_data.vehicle.copy()
set_angles(machineMode, actionState)

def set_frames():
    global divCount
    global keyFrame
    global nextKeyFrame
    global machineMode
    global actionState
    global angles
    if actionState == 'VEHICLE2ROBOT' or actionState == 'ROBOT2VEHICLE' or actionState == 'WALK':
        divCount += 1
        if divCount > angles[nextKeyFrame][21]:
            divCount = 0
            keyFrame = nextKeyFrame
            nextKeyFrame += 1
            if nextKeyFrame > maxRows - 1:
                if actionState == 'WALK':
                    nextKeyFrame = 0
                else:
                    keyFrame = 0
                    nextKeyFrame = 1
                    if actionState == 'ROBOT2VEHICLE':
                        machineMode = 'VEHICLE_MODE'
                        angles.clear()
                        angles = motion_data.vehicle.copy()
                    else:
                        machineMode = 'ROBOT_MODE'
                        angles.clear()
                        angles = motion_data.robot.copy()
                    actionState = 'STOP'
        set_angles(machineMode, actionState)
                
            
        
        
