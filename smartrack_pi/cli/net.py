from typing import Annotated

import typer

from smartrack_pi.net import adaptor

app = typer.Typer()

adaptor_address = adaptor.Address()


@app.command()
def dhcp():
    print("Warning: You will need to reconnect")
    print("Setting Net Mode to DHCP")
    adaptor_address.set_adaptor_dhcp()


@app.command()
def static(
    ip_address: Annotated[
        str, typer.Option(help="please enter ip with bit mask i.e. '192.168.1.241/24'")
    ] = "192.168.1.241/24",
    gateway: Annotated[str, typer.Option(help="Please enter gateway")] = "192.168.1.1",
):
    print("Warning: You will need to reconnect")
    print(f"Setting Net Mode to Static Ip: {ip_address} and Gateway: {gateway}")
    adaptor_address.set_adaptor_static(ip_address, gateway)


if __name__ == "__main__":
    app()
