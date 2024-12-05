from machine import Pin, I2C # machine.I2Cをインポート

FREQ = 50.0  # サーボ信号周波数
MAX_DUTY = 4096.0 # 周期内の分割数
MIN_PULSE = 400  # 最小パルス幅　msec at 0°
MAX_PULSE = 2400  # 最大パルス幅  msec at 180°

PCA9685_ADDR = 0x40 # PCA9685のI2Cアドレス

# I2C設定 machine.I2C(id, sclピン, sdaピン, 最大周波数)
i2c = I2C(0,scl=Pin(1),sda=Pin(0),freq=100000)

data = bytearray(4) # 送信するデータ　4byte準備

# I2C通信する関数
def reg_write(i2c, addr, reg, data, length):
    # i2c:I2Cオブジェクト
    # addr:デバイスアドレス
    # reg:レジスタアドレス
    # data:送信データ
    # length:送信データバイト数
    msg = bytearray() # 送信用バッファ
    for i in range(length):
        msg.append(data[i]) #バッファに送信データを追加
    i2c.writeto_mem(addr, reg, msg) # 書き込み

# PCA9685(I2C)初期設定
data[0] = 0b00010001 # MODE1レジスタ（0x00）のSLEEPビット（4 bit）を1
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)
data[0] = 121 # PRE_SCALEレジスタ（0xFE）値を121に設定
reg_write(i2c, PCA9685_ADDR, 0xFE, data, 1)
# MODE1レジスタのSLEEPビット（4 bit）を0 、Auto-Increment enabledを1
data[0] = 0b00100001
reg_write(i2c, PCA9685_ADDR, 0x00, data, 1)

# パルス幅設定
width = MAX_DUTY*(MIN_PULSE+(MAX_PULSE-MIN_PULSE)/180*90)*FREQ/1000000
data[0] = 0x00 # LED_ON_L
data[1] = 0x00 # LED_ON_H
data[2] = 0x00ff & int(width) # LED_OFF_L
data[3] = (0xff00 & int(width))>>8 # LED_OFF_H
reg_write(i2c, PCA9685_ADDR, 0x06, data, 4)