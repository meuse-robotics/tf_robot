import uasyncio as asyncio
from sys import stdin
from select import poll, POLLIN
import robot

poll_obj = poll()
poll_obj.register(stdin, POLLIN)

async def handle_commands():  
    #シリアル入力からコマンドを受け付けて処理する非同期タスク
    global sleep_time
    print("Ready to receive commands.")
    while True:
        # sys.stdinのデータ有無を確認し、入力があれば処理
        if poll_obj.poll(10):
            command = stdin.read(1)  # 1文字だけ読み取る
            robot.set_action(command)
        await asyncio.sleep(0.1)  # 他のタスクに制御を譲る

async def main():
    #メインタスクでblink_ledとhandle_commandsを並行実行
    asyncio.create_task(handle_commands())
    while True:
        robot.set_frames()
        
        await asyncio.sleep(0.03)
# asyncioのイベントループを開始
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
