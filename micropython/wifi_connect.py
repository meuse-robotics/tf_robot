import network
import time

# Wi-FiのSSIDとパスワードを設定
SSID = "your-SSID"         # Wi-FiのSSIDを入力
PASSWORD = "your-PASSWORD" # Wi-Fiのパスワードを入力

# Wi-Fiに接続する関数
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)  # STA_IFはStationモード
    wlan.active(True)  # Wi-Fiを有効化
    wlan.config(pm = 0xa11140)  # Wi-Fiの省電力をオフ
    wlan.connect(SSID, PASSWORD)  # Wi-Fiネットワークに接続

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():  # 接続が完了するまで待機
        print(".", end="")
        time.sleep(1)

    print("\nConnected!")
    print("IP Address:", wlan.ifconfig()[0])  # IPアドレスを表示

# メイン処理
connect_to_wifi()
