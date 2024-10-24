from machine import SPI, Pin
import tinypico as TinyPICO
import neopixel
from micropython_dotstar import DotStar
import time

class LEDController:
    def __init__(self, ws2811_pin, total_pixels, default_rgb):
        # Setup onboard RGB
        print('init led controller')
        spi = SPI(sck=Pin(TinyPICO.DOTSTAR_CLK), mosi=Pin(TinyPICO.DOTSTAR_DATA), miso=Pin(TinyPICO.SPI_MISO))
        self.dotstar = DotStar(spi, 1, brightness=0.5)
        TinyPICO.set_dotstar_power(True)
        self.dotstar[0] = (0, 255, 0, 0.5)

        # Setup LED strip
        print('setup striup')
        self.ws2811_pin = Pin(ws2811_pin, Pin.OUT)
        self.ws2811_strip = neopixel.NeoPixel(self.ws2811_pin, total_pixels)
        self.total_pixels = total_pixels
        self.rgb_values = default_rgb

    def set_rgb(self, rgb):
        print('set rgb')
        self.rgb_values = rgb
        self.dotstar[0] = (rgb[0], rgb[1], rgb[2], 0.5)
        print('RGB vals set:', rgb)

    def initialize_led_strip(self):
        print('init strip')
        for i in range(self.total_pixels):
            self.ws2811_strip[i] = (0, 0, 0)
        self.ws2811_strip.write()

    def update_led_strip(self, args):
        num_pixels_per_strip, num_strips = args
        time.sleep_ms(10)

        for j in range(num_strips):
            base_index = j * num_pixels_per_strip 
            for i in range(num_pixels_per_strip):
                pixel_index = base_index + (i if j % 2 == 0 else (num_pixels_per_strip - 1 - i))
                if 0 <= pixel_index < len(self.ws2811_strip):
                    self.ws2811_strip[pixel_index] = self.rgb_values
                mirrored_index = -1 - pixel_index + (j * 2)
                if 0 <= mirrored_index < len(self.ws2811_strip):
                    self.ws2811_strip[mirrored_index] = (0, 0, 0)

        self.ws2811_strip.write()




