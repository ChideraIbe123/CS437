from gpiozero import Device
from gpiozero.pins.native import NativeFactory
import time
from robot_hat import reset_mcu

# Set pin factory
Device.pin_factory = NativeFactory()

# Force close specific pin 23
try:
    pin23 = Device.pin_factory.pin(23)
    if pin23:
        pin23.close()
except:
    pass

# Force close all pins
for pin in list(Device.pin_factory.pins.values()):
    try:
        pin.close()
    except:
        pass

# Reset MCU
reset_mcu()
time.sleep(1)
