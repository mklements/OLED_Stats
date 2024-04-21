from signal import pause
from time import sleep

from gpiozero import Button
from net.adaptor import Address
from settings.software import factory_reset

from smartrack_pi.display import show

WAS_HELD = False


def released():
    global WAS_HELD
    print("released")
    if not WAS_HELD:
        adaptor = Address()
        if adaptor.config.get("mode") == "D":
            print("Setting to Static")
            show.text("Setting Net Mode to Static...")
            print(adaptor.set_adaptor_static())
        else:
            print("Setting to DHCP")
            show.text("Setting Net Mode to DHCP...")
            print(adaptor.set_adaptor_dhcp())
        sleep(5)
        show.stats()
    WAS_HELD = False


def held():
    global WAS_HELD
    WAS_HELD = True
    adaptor = Address()
    show.text("Factory Resetting Net Adaptors....")
    adaptor.factory_reset()
    sleep(5)
    factory_reset()


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
