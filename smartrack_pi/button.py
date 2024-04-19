from signal import pause
from time import sleep

from display import change_display
from gpiozero import Button
from net.set_adaptor import Adaptor
from settings.software import factory_reset

WAS_HELD = False


def released():
    global WAS_HELD
    print("released")
    if not WAS_HELD:
        adaptor = Adaptor()
        if adaptor.config.get("mode") == "D":
            print("Setting to Static")
            change_display.display_text("Setting Net Mode", "to Static...")
            print(adaptor.set_adaptor_static())
        else:
            print("Setting to DHCP")
            change_display.display_text("Setting Net Mode", "to DHCP...")
            print(adaptor.set_adaptor_dhcp())
        sleep(5)
        change_display.stats_status()
    WAS_HELD = False


def held():
    global WAS_HELD
    WAS_HELD = True
    adaptor = Adaptor()
    change_display.display_text("Factory Resetting", "Net Adaptors....")
    adaptor.factory_reset()
    sleep(5)
    factory_reset()


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
