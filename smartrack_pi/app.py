import json
import os
from ipaddress import IPv4Network
from time import sleep

import streamlit as st
from netaddr import IPAddress
from streamlit_js_eval import get_page_location

from ip.set_adaptor import Adaptor
from settings import software


def get_mask(mask_bit):
    return IPv4Network(f"0.0.0.0/{mask_bit}").netmask


dir_path = os.path.dirname(os.path.realpath(__file__))


def main():
    st.set_page_config(
        initial_sidebar_state="collapsed",
        page_title="Smartrack Settings",
        page_icon=f"{dir_path}/app/static/4. CT Mark - Colour PNG.png",
    )
    with open(f"{dir_path}/app/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    adaptor = Adaptor()
    current_cidr = adaptor.config.get("static_ip")
    current_ip = current_cidr.split("/")[0]
    current_mask_bit = int(current_cidr.split("/")[1])

    st.image(
        f"{dir_path}/app/static/1. Super Landscape - Without Box - Colour With Black Text - PNG.png"
    )

    page_loc = get_page_location()
    sleep(0.2)

    link = f"{page_loc.get('origin')}:8000"
    st.markdown(
        """
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<a class="big-font" href="{link}" target="_self">Go To Companion</a>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.header("Static IP", divider="grey")
    st.write("Sets unit to static IP address, for DHCP press button on the unit")

    mask_bit = st.sidebar.slider("Subnet Calculator", 0, 32, value=current_mask_bit)
    mask = get_mask(mask_bit)
    st.sidebar.write(f"The subnet mask is {mask}")

    with st.form(key="my-form"):
        ip = st.text_input("Enter the static ip address", value=current_ip)
        mask = st.text_input(
            "Enter the subnet mask (Click the Arrow in the Top Left for Bit Mask Calculator)",
            value=mask,
        )
        gateway = st.text_input(
            "Enter the gateway", value=adaptor.config.get("gateway", "192.168.1.1")
        )
        submit = st.form_submit_button("Set to Static IP")

    if submit:
        mask_bit = IPAddress(mask).netmask_bits()
        st.write("Changing IP!! Please use the following links... (Takes 5-10 Seconds)")
        st.page_link(
            f"http://{ip}:8000", label="Click to Open Companion at New Address"
        )
        st.page_link(f"http://{ip}", label="Click to Open This page at New Address")
        sleep(5)
        adaptor.set_adaptor_static(f"{ip}/{mask_bit}", gateway)

    st.header("Recall Default Files", divider="grey")
    st.write("Will replace entire companion config with the folowing")
    with st.form(key="default-file"):
        select = st.selectbox("File Name", ["default", "more_pearls"])
        def_form_submit = st.form_submit_button("Overwrite config and restart")
    if def_form_submit:
        st.write(f"Selected: {select}! Restarting!")
        software.restore_companion_file(select)

    st.header("Update Software", divider="grey")
    st.write("Will not overwrite an companion configs")
    with st.form(key="update"):
        update_submit = st.form_submit_button("Update")
    if update_submit:
        st.write("Updating!")
        software.update()


main()
