import network
import uasyncio as asyncio
from machine import Pin
import robot
import html

SSID = "WARPSTAR-AC6D64"   # Wi-FiのSSIDを入力
PASSWORD = "435C37A1AD1BE" # Wi-Fiのパスワードを入力

#led = Pin('LED', Pin.OUT)

# Wi-Fi接続関数
async def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        await asyncio.sleep(1)
    print("Connected to Wi-Fi!")
    print("IP Address:", wlan.ifconfig()[0])

# HTMLページの生成
def webpage():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Pico W LED Control</title>
    <script>
        async function sendCommand(command) {
            try {
                // Fetch APIでサーバーにリクエストを送信
                const response = await fetch(`/${command}`);
            } catch (error) {
                console.error('Error sending command:', error);
            }
        }
    </script>
    </head>
    <body>
    <h1>Raspberry Pi Pico W</h1>
    <h2>LED Control</h2>
    <button id="nbtn" onclick="sendCommand('led/on')">Turn ON</button>
    <button id="fbtn" onclick="sendCommand('led/off')">Turn OFF</button>
    </body>
    </html>
    """
    return html

# クライアントリクエストの処理関数
async def serve_client(reader, writer):
    request_line = await reader.readline()
    print("Request:", request_line)
    while await reader.readline() != b"\r\n":
        pass

    request = request_line.decode().split(" ")[1]
    print("Path:", request)
    """if request == "/led/on":
        led.value(1)  # LEDをON
    elif request == "/led/off":
        led.value(0)  # LEDをOFF"""
    robot.set_action(request[1])
    response = html.html #webpage()
    writer.write(response.encode("utf-8"))
    await writer.drain()
    await writer.aclose()

# メイン処理
async def main():
    await connect_to_wifi()
    server = await asyncio.start_server(serve_client, "0.0.0.0", 80)
    print("Server is running on port 80")

    while True:
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped.")
