import typer
from typing import Annotated
from smartrack_pi.net import Adaptor

app = typer.Typer()

adaptor = Adaptor()


def _get_config():
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", encoding="utf-8"
    ) as f:
        return json.load(f)


def _set_config(key, value):
    config = _get_config()
    config[key] = value
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", "w", encoding="utf-8"
    ) as f:
        json.dump(config, f)


@app.command()
def dhcp():
    print("Warning: You will need to reconnect")
    print("Setting Net Mode to DHCP")
    adaptor.set_adaptor_dhcp()

@app.command()
def static(ip_address: Annotated[str, typer.Option(help="please enter ip with bit mask i.e. '192.168.1.241/24'")]='192.168.1.241/24', gateway: Annotated[str, typer.Option(help="Please enter gateway")]="192.168.1.1"):
    print("Warning: You will need to reconnect")
    print(f"Setting Net Mode to Static Ip: {ip_address} and Gateway: {gateway}")
    adaptor.set_adaptor_static(ip_address, gateway)


if __name__ == "__main__":
    app()