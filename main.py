
import micropython
from config import *
from wifi import setup_ap
from web_server import serve_rgb_webpage, handle_web
from led_control import LEDController
from MicroDNSSrv import MicroDNSSrv

def main():
    print('init ledcontroller')
    led_controller = LEDController(WS2811_PIN, TOTAL_PIXELS, DEFAULT_RGB)
    led_controller.initialize_led_strip()

    print('start wifi')
    ap = setup_ap(WIFI_SSID, WIFI_PASSWORD)

    print('start webserver')
    sock = serve_rgb_webpage(SERVER_PORT, led_controller.set_rgb, led_controller.set_mode)

    while True:
#        print(".")
        led_controller.update_led_strip((NUM_PIXELS_PER_STRIP, NUM_STRIPS))

        handle_web(sock, led_controller.set_rgb, led_controller.set_mode)

# using threads fucks everything up because stuff is not written properly threadsafe
# so we ditch the followiing dns server w/ catch all, also handle http handling & led controller
# not as cool async as we wanted. F.

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
