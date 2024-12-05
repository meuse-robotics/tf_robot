import uasyncio as asyncio
from machine import Pin
from sys import stdin
from select import poll, POLLIN

# GPIO 25 (Picoの内蔵LED) を制御するためのピン設定
led = Pin('LED', Pin.OUT)
poll = poll()
poll.register(stdin, POLLIN)
sleep_time = 0.5

async def blink_led():
    #LEDを定期的に点滅させる非同期タスク
    while True:
        led.value(1)  # LED ON
        await asyncio.sleep(sleep_time)  # sleep_time秒待機
        led.value(0)  # LED OFF
        await asyncio.sleep(sleep_time)  # sleep_time秒待機

async def handle_commands():  
    #シリアル入力からコマンドを受け付けて処理する非同期タスク
    global sleep_time
    print("Ready to receive commands.")
    while True:
        # sys.stdinのデータ有無を確認し、入力があれば処理
        if poll.poll(10):
            command = stdin.read(1)  # 1文字だけ読み取る
            if command == "1":  # "1" を受信したらLEDを点灯
                sleep_time += 0.1
                print("Command received: LED ON")
            elif command == "0":  # "0" を受信したらLEDを消灯
                sleep_time -= 0.1
                print("Command received: LED OFF")
            else:
                print(f"Unknown command: {command}")
        await asyncio.sleep(0.1)  # 他のタスクに制御を譲る

async def main():
    #メインタスクでblink_ledとhandle_commandsを並行実行
    await asyncio.gather(blink_led(), handle_commands())

# asyncioのイベントループを開始
asyncio.run(main())

