from machine import Pin, Timer
led = Pin('LED', Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq = 1, mode = Timer.PERIODIC, callback = blink)