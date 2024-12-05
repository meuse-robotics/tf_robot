from machine import Pin, PWM

FREQ = 50.0  # サーボ信号周波数
MAX_DUTY_G = 65025.0 # 周期内の分割数
MIN_PULSE_G = 600  # 最小パルス幅　msec at 0°
MAX_PULSE_G = 2400  # 最大パルス幅  msec at 180°

angles = [90,90,90,90,90]
correct = [0,0,0,0,0]
servos = [PWM(Pin(6)),PWM(Pin(7)),PWM(Pin(8)),PWM(Pin(9)),PWM(Pin(10))]

for i in range(5):
    servos[i].freq(50)
    if angles[i]<0:
        servos[i].duty_u16(0)
    else:
        width = MAX_DUTY_G \
            * (MIN_PULSE_G + (MAX_PULSE_G - MIN_PULSE_G) / 180 * (angles[i]+correct[i]))\
            * FREQ / 1000000
        servos[i].duty_u16(int(width))
   
