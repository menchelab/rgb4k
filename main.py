# main.py -- put your code here!

import micropython
from config import *
from wifi import setup_ap
from web_server import serve_rgb_webpage
from led_control import LEDController
from MicroDNSSrv import MicroDNSSrv

def main():
    print('init ledcontroller')
    led_controller = LEDController(WS2811_PIN, TOTAL_PIXELS, DEFAULT_RGB)
    led_controller.initialize_led_strip()

    print('start wifi')
    ap = setup_ap(WIFI_SSID, WIFI_PASSWORD)

    print('start webserver')
    while True:
        print(".")
        led_controller.update_led_strip((NUM_PIXELS_PER_STRIP, NUM_STRIPS))
        serve_rgb_webpage(SERVER_PORT, led_controller.set_rgb)

"""
  if MicroDNSSrv.Create( {
    "*"   : "192.168.4.1",
    "www.site.*" : "192.168.4.1" } ) :
    print("MicroDNSSrv started.")
  else :
    print("Error to starts MicroDNSSrv...")
"""
    

if __name__ == "__main__":
    main()
